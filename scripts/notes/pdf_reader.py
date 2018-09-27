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
import json
import os
import PyPDF2
import pdftotext
import utils

def read_pdf(file_path):
	file_name = utils.path_leaf(file_path)
	if file_name[-4:] != ".pdf":
		raise TypeError("Expecting input of pdf file")

	paragraphs = []
	title = file_name[:-4]

	pdf_file_in = open(file_path, 'rb')
	# pdf_reader = PyPDF2.PdfFileReader(pdf_file_in)
	# num_pages = pdf_reader.numPages
	pdf_reader = pdftotext.PDF(pdf_file_in)


	# for i in range(num_pages):
	# 	paragraphs.append(pdf_reader.getPage(i).extractText())
	for page in pdf_reader:
		paragraphs.append(page)

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
			continue
		for p in paragraphs:
			tsv_writer.writerow([title, p])
	tsv_file_out.close()