# !/usr/bin/env python3
# -*-coding:utf-8 -*-
# @Author  : Chen Do

from  PyPDF2 import PdfFileReader
from  PyPDF2 import PdfWriter
import os
import time
import sys
import io
import datetime

NanjingAuthor   = "Firmware Development Group"
NanjingProducer = "MindMotion Nanjing Ecosystem"
NanjingCreator  = "Chen Do"

global handle_num
output_file = []
handle_num = 0


def create_detail_day():
    # day_time = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
    # hour_time = datetime.datetime.now().strftime('time' + "%H_%M_%S")
    detail_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return detail_time

class Logger(object):
    def __init__(self, filename="Default.log", path=".\\"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.terminal = sys.stdout
        self.log = open(os.path.join(path, filename), "a", encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def handle_doc(outputfilepath, filepath, filename):
    global handle_num
    readfilepath = filepath + '\\' + filename
    outputfilepath = outputfilepath + '\\' + filename

    if not filename.endswith('.pdf'):
        print("[ERROR]\t\""+filename+'\" is not *.Pdf files!')
        return

    # reader & writer
    reader = PdfFileReader(readfilepath)
    writer = PdfWriter()

    # read meta
    meta = reader.metadata
    l_creation_data_raw = str(meta.creation_date_raw)
    l_modification_date_raw = str(meta.modification_date_raw)

    if (meta.producer == NanjingProducer):
        print("[WARN]\t\""+filename+'\" needn\'t to change!')
        return

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Add the metadata
    writer.add_metadata(
        {
            "/Author": NanjingAuthor,
            "/Creator": NanjingCreator,
            "/Producer": NanjingProducer,
            "/CreationDate": l_creation_data_raw,
            "/ModDate": l_modification_date_raw
        }
    )

    # Save the new PDF to a file
    with open(outputfilepath, "wb") as f:
        writer.write(f)
        print('[INFO]\t'+'*'*12+'\t\"'+filename+"\" Done!\t"+'*'*12)

    # decoder handle number
    handle_num = handle_num + 1
    output_file.append(outputfilepath)


if __name__ == "__main__":
    path_files = os.getcwd()
    output_filepath = path_files + '\\output'
    log_filepath = path_files + '\\log'
    i = 0

    time_start = time.time()

    if not os.path.exists(log_filepath):
        os.makedirs(log_filepath)

    sys.stdout = Logger('PdfCleaner_' + create_detail_day() + '.log', path=log_filepath)
    print(create_detail_day().center(60,'*'))

    # get current file path
    # path_files = os.path.dirname(os.path.abspath(__file__))+'\\doc'
    # path_files = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(output_filepath):
        print("[WARN]\tLack of output files dir, Doing...")
        os.makedirs(output_filepath)

    print('[INFO]\tOutput Dir: ' + output_filepath)

    for filepath, dirnames, filenames in os.walk(path_files):
        for filename in filenames:
            handle_doc(output_filepath, filepath, filename)

    time_end = time.time()
    time_sum = time_end - time_start
    print("[INFO]\tTotal Speed Time: %.2f s; Handle PDF: %d file(s)" %(time_sum, handle_num))
    if handle_num == 0:
        os.rmdir(output_filepath)
        print("[ERROR]\t Delete Output DIR(NULL)")
    else:
        for printList in output_file:
            i += 1
            print('\t[%02d]:  ' %i+printList)