# !/usr/bin/env python3
# -*-coding:utf-8 -*-
# @Author  : Chen Do

from  PyPDF2 import PdfFileReader
from  PyPDF2 import PdfWriter
import os
import time

global handle_num
output_file = []

handle_num = 0;

def handle_doc(outputfilepath, filepath, filename):
    NanjingProducer = "MindMotion Nanjing Ecosystem"
    
    global handle_num
    readfilepath = filepath + '\\' + filename
    outputfilepath = outputfilepath + '\\' + filename

    if not filename.endswith('.pdf'):
        print("[Error]\t\""+filename+'\" is not *.Pdf files!')
        return

    # reader & writer
    reader = PdfFileReader(readfilepath)
    writer = PdfWriter()

    # read meta
    meta = reader.metadata

    l_creation_data_raw = str(meta.creation_date_raw)
    l_modification_date_raw = str(meta.modification_date_raw)

    if (meta.producer == NanjingProducer):
        print("[Warning]\t\""+filename+'\" needn\'t to change!')
        return

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Add the metadata
    writer.add_metadata(
        {
            "/Author": "Firmware Development Group",
            "/Creator": "Chen Do",
            "/Producer": NanjingProducer,
            "/CreationDate": l_creation_data_raw,
            "/ModDate": l_modification_date_raw
        }
    )

    handle_num = handle_num + 1
    output_file.append(outputfilepath)

    # Save the new PDF to a file
    with open(outputfilepath, "wb") as f:
        writer.write(f)
        print('[info]'+'*'*12+'\t\"'+filename+"\" Done!\t"+'*'*12)

if __name__ == "__main__":

    print("-------Begin-------")
    time_start = time.time()  # 记录开始时间
    
    # get current file path
    # path_files = os.path.dirname(os.path.abspath(__file__))+'\\doc'
    path_files = os.path.dirname(os.path.abspath(__file__))

    # output file path
    output_filepath = os.path.dirname(os.path.abspath(__file__))+'\\output'
    if not os.path.exists(output_filepath):
        print("[info]\tNow is making output files dir!")
        os.makedirs(output_filepath)
    print('[NOTE]\tOutput Dir: ' + output_filepath)

    for filepath, dirnames, filenames in os.walk(path_files):
        for filename in filenames:
            handle_doc(output_filepath, filepath, filename)

    time_end = time.time()
    time_sum = time_end - time_start
    print("[info]\tTotal Speed Time: %.2f s, Handle: %d files" %(time_sum,handle_num))
    for printList in output_file:
        print('\t'+printList)