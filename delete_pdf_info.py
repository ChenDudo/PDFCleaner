# !/usr/bin/env python3
# -*-coding:utf-8 -*-
# @Author  : Chen Do

from  PyPDF2 import PdfFileReader
from  PyPDF2 import PdfWriter


def handle_doc(filepath):

    # with open(filepath, 'rb') as f:
    reader = PdfFileReader(filepath)
    infor = reader.getDocumentInfo()
    print(infor)
    print("=========")
    meta = reader.metadata
    l_creation_data = str(meta.creation_date)
    l_creation_data_raw = str(meta.creation_date_raw)
    l_modification_date = str(meta.modification_date)
    l_modification_date_raw = str(meta.modification_date_raw)
    # print("author" + meta.author)
    # print("creator:" + meta.creator)
    print("producer" + meta.producer)
    print(meta.subject)
    print(meta.title)

    writer = PdfWriter()
    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Add the metadata
    writer.add_metadata(
        {
            "/Author": "Firmware Development Group",
            "/Creator": "Chen Do",
            "/Producer": "MindMotion Nanjing Ecosystem",
            "/CreationDate": l_creation_data_raw,
            "/ModDate": l_modification_date_raw
        }
    )

    # Save the new PDF to a file
    with open("./1_copy.pdf", "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    print("-------begin-------")
    filepath = "./doc/1.pdf"
    handle_doc(filepath)