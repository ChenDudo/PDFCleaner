# !/usr/bin/env python3
# -*-coding:utf-8 -*-
# @Author  : Chen Do

import configparser
from  PyPDF2 import PdfFileReader
from  PyPDF2 import PdfWriter
import os
import time
import sys
import io
import datetime

global NanjingAuthor
global NanjingProducer
global NanjingCreator

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
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.terminal = sys.stdout
        self.log = open(os.path.join(path, filename), "a", encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def handle_doc(outputfilepath, filepath, filename):
    global handle_num
    global NanjingAuthor
    global NanjingProducer
    global NanjingCreator

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

    if (meta.producer == NanjingProducer) and (meta.author == NanjingAuthor) and (meta.creator == NanjingCreator):
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
        print('[INFO]\t'+'\"'+filename+"\" Done! "+'*'*36)

    # decoder handle number
    handle_num = handle_num + 1
    output_file.append(outputfilepath)


''' (config.ini) file module:
[global]
NanjingAuthor   = 'Firmware Development Group'
NanjingProducer = 'MindMotion Nanjing Ecosystem'
NanjingCreator  = 'Chen Do'
'''
def read_config_file(filepath):
    global NanjingAuthor
    global NanjingProducer
    global NanjingCreator
    conf_file = filepath + "\\config.ini"

    conf = configparser.ConfigParser()
    
    if os.path.exists(conf_file):
        conf.read(conf_file)
        if not "global" in conf:
            print("[WARN]\tNo global section in config file")
            pass
        else:
            if 'NanjingAuthor' in conf['global']:
                NanjingAuthor   = eval(conf.get("global", "NanjingAuthor"))
            if 'NanjingProducer' in conf["global"]:
                NanjingProducer = eval(conf.get("global", "NanjingProducer"))
            if 'NanjingCreator' in conf["global"]:
                NanjingCreator  = eval(conf.get("global", "NanjingCreator"))
    else:
        print("[ERROR]\tNo Config files, Use default config")
        # NanjingAuthor   = "Firmware Development Group"
        # NanjingProducer = "MindMotion Nanjing Ecosystem"
        # NanjingCreator  = "Chen Do"
    print("[info]\tNow Use following Config :")
    print("\t[Author]: " + NanjingAuthor)
    print("\t[Producer]: " + NanjingProducer)
    print("\t[Creator]: " + NanjingCreator)


if __name__ == "__main__":
    # parameter init
    path_files = os.getcwd()
    output_filepath = path_files + '\\output'
    log_filepath = path_files + '\\log'
    i = 0

    # get begin time
    time_start = time.time()
    
    # configure Log file
    if not os.path.exists(log_filepath):
        os.makedirs(log_filepath)
    sys.stdout = Logger('PdfCleaner_' + create_detail_day() + '.log', path=log_filepath)
    print(create_detail_day().center(60,'*'))

    # read config.ini file
    read_config_file(path_files)

    # get current file path
    # path_files = os.path.dirname(os.path.abspath(__file__))+'\\doc'
    # path_files = os.path.dirname(os.path.abspath(__file__))

    # configure Output file
    if not os.path.exists(output_filepath):
        print("[WARN]\tLack of output files dir, Doing...")
        os.makedirs(output_filepath)
    print('[INFO]\tOutput Dir: ' + output_filepath)

    # Handle PDF files
    for filepath, dirnames, filenames in os.walk(path_files):
        for filename in filenames:
            if filename.endswith(".pdf"):
                handle_doc(output_filepath, filepath, filename)

    # get finish time
    time_end = time.time()
    time_sum = time_end - time_start

    # other handle
    print("[INFO]\tTotal Speed Time: %.2f s; Handle PDF: %d file(s)" %(time_sum, handle_num))
    if handle_num == 0:
        os.rmdir(output_filepath)
        print("[ERROR]\t Delete Output DIR(NULL)")
    else:
        for printList in output_file:
            i += 1
            print('\t[%02d]:  ' %i+printList)