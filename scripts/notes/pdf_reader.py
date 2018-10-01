"""
A script to convert pdf to tsv file for annotation
title 			| paragraph
---------------------------
<pdf's name>	| p1
<pdf's name>	| p2
"""

import argparse
import constants
import csv
import io
import json
import os
import string
import utils

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser

def read_pdf(file_path):
	print("Reading", file_path)
	file_name = utils.path_leaf(file_path)
	if file_name[-4:] != ".pdf":
		raise TypeError("Expecting input of pdf file")

	paragraphs = []
	title = file_name[:-4]

	pdf_file_in = open(file_path, 'rb')
	rsrcmgr = PDFResourceManager()
	retstr = io.StringIO()
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	page_no = 0
	for pageNumber, page in enumerate(PDFPage.get_pages(pdf_file_in)):
		if pageNumber == page_no:
			if pageNumber % 10:
				print("Read page", str(pageNumber))
			interpreter.process_page(page)
			data = retstr.getvalue()
			data = ''.join(x for x in data if x in string.printable)
			if len(data) > 0:
				paragraphs.append(data)
			retstr.truncate(0)
			retstr.seek(0)
		page_no += 1

	pdf_file_in.close()

	return title, paragraphs

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input_dir', type=str)
	parser.add_argument('output', type=str)
	args = parser.parse_args()

	tsv_file_out = open(args.output, 'wt')
	tsv_writer = csv.writer(tsv_file_out, delimiter='\t', lineterminator='\n')
	tsv_writer.writerow(constants.note_tsv_header)

	for file_path in os.listdir(args.input_dir):
		file_path = args.input_dir + file_path
		try:
			title, paragraphs = read_pdf(file_path)
		except TypeError as e:
			print(e)
			continue

		total = len(paragraphs)
		read = 0.0

		for p in paragraphs:
			try:
				tsv_writer.writerow([title, p])
				read += 1
			except UnicodeEncodeError as e:
				print(e)
				continue
		print("Reading percentage of '{}': {}".format(title, read/total))

	tsv_file_out.close()
