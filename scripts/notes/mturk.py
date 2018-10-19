import argparse
import constants
import csv
import os
import pdf_reader
from random import shuffle
import re
import utils

from sklearn.model_selection import train_test_split

def read_self_annot(self_annot, start_row=1, verbose=True):
	if verbose:
		print("Reading self annotation", self_annot)

	csv_self_annot = open(self_annot, 'rt')
	csv_reader_self_annot = csv.reader(csv_self_annot, delimiter=',')

	self_annot_source_data = {}
	self_annot_response_data = {}

	for i, row in enumerate(csv_reader_self_annot):
		if verbose and i % 10 == 0:
			print("Read row", str(i))
		if i >= start_row:
			print(row)
			url, mod_name, chap_name, dept, page, question, answer = row[:7]
			if url not in self_annot_source_data:
				self_annot_source_data[url] = {
					"title": mod_name,
					"chapter": chap_name,
					"dept": dept
				}
			else:
				assert mod_name == self_annot_source_data[url]["title"]
				assert chap_name == self_annot_source_data[url]["chapter"]
				assert dept == self_annot_source_data[url]["dept"]
			if url not in self_annot_response_data:
				self_annot_response_data[url] = []
			self_annot_response_data[url].append({
					"page": page,
					"question": question,
					"answer": answer
				})
	csv_self_annot.close()

	return self_annot_source_data, self_annot_response_data

def read_mturk_source(mturk_source, start_row=1, verbose=True):
	if verbose:
		print("Reading mturk source", mturk_source)

	csv_mturk_source = open(mturk_source, 'rt')
	csv_reader_mturk_source = csv.reader(csv_mturk_source, delimiter=',')

	mturk_source_data = {}

	for i, row in enumerate(csv_reader_mturk_source):
		if verbose and i % 10 == 0:
			print("Read row", str(i))
		if i >= start_row:
			print(row)
			url, title, _, dept = row[:4]
			assert url not in mturk_source_data
			mturk_source_data[url] = {
				"title": title,
				"dept": dept,
				"chapter": ""
			}

	csv_mturk_source.close()
	return mturk_source_data

def read_mturk_response(mturk_response, start_row=1, verbose=True):
	if verbose:
		print("Reading mturk response", mturk_response)

	csv_mturk_response = open(mturk_response, 'rt')
	csv_reader_mturk_response = csv.reader(csv_mturk_response, delimiter=',')

	mturk_response_data = {}

	for i, row in enumerate(csv_reader_mturk_response):
		if verbose and i % 10 == 0:
			print("Read row", str(i))
		if i >= start_row:
			url, page, question, answer = row[:4]
			if url not in mturk_response_data:
				mturk_response_data[url] = []
			mturk_response_data[url].append({
					"page": page,
					"question": question,
					"answer": answer
				})

	csv_mturk_response.close()
	return mturk_response_data

def download_pdf(pdf_urls, dest_path, gdrive):
	if gdrive:
		for url in pdf_urls:
			m = re.search('https://drive.google.com/file/d/(.+?)/view\?usp=sharing', url)
			file_name = m.group(1) if m else "default"
			gdrive_id = file_name + ".pdf"
			utils.download_gdrive(gdrive_id, dest_path + gdrive_id + ".pdf")
	else:
		for url in pdf_urls:
			download_script = "wget " + url
			move_script = "mv " + utils.path_leaf(url) + " " + dest_path
			os.system(download_script)
			os.system(move_script)

def get_file_name(url, gdrive):
	if gdrive:
		m = re.search('https://drive.google.com/file/d/(.+?)/view\?usp=sharing', url)
		name = m.group(1) if m else "default"
		return name + ".pdf"
	return utils.path_leaf(url)

def build_lecture_note_dataset(mturk_source_data, mturk_response_data, data_dir, output, squash=True, gdrive=False, verbose=True):

	pdf_urls = mturk_response_data.keys()
	download_pdf(pdf_urls, data_dir, gdrive)

	lecture_note_dataset = []
	unique_questions = []
	not_found = []

	for url in pdf_urls:
		file_name = get_file_name(url, gdrive)
		file_path = data_dir + file_name
		_, paragraphs = pdf_reader.read_pdf(file_path)

		pdf_info = mturk_source_data[url]	
		title, dept, chapter = pdf_info["title"], pdf_info["dept"], pdf_info["chapter"]

		for qa in mturk_response_data[url]:
			page, question, answer = qa["page"], qa["question"], qa["answer"]
			if question not in unique_questions:			
				answer = utils.normalize(answer)
				annotated_p = utils.normalize(paragraphs[int(page)-1])
				if answer in annotated_p:
					lecture_note_dataset.append([title, annotated_p, question, answer, dept, chapter])
					unique_questions.append(question)
				else:
					for p in paragraphs:
						p = utils.normalize(p)	
						if answer in p:	
							lecture_note_dataset.append([title, p, question, answer, dept, chapter])
							unique_questions.append(question)
							break
					not_found.append([title, question, answer])
	for i in not_found[:5]:
		print(i)	
	raise Exception()
	return lecture_note_dataset

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('mturk_source', type=str)
	parser.add_argument('mturk_response', type=str)
	parser.add_argument('self_annot', type=str)
	parser.add_argument('data_dir', type=str)
	parser.add_argument('output', type=str)
	parser.add_argument('train_output', type=str)
	parser.add_argument('dev_output', type=str)
	parser.add_argument('dev_size', type=float)
	args = parser.parse_args()

	self_annot_source_data, self_annot_response_data = read_self_annot(args.self_annot)
	self_annot_dataset = build_lecture_note_dataset(self_annot_source_data, self_annot_response_data, args.data_dir, args.output, gdrive=True)
	mturk_source_data = read_mturk_source(args.mturk_source)
	mturk_response_data = read_mturk_response(args.mturk_response)
	mturk_dataset = build_lecture_note_dataset(mturk_source_data, mturk_response_data, args.data_dir, args.output)
	lecture_note_dataset = mturk_dataset + self_annot_dataset
	shuffle(lecture_note_dataset)
	train_dataset, dev_dataset = train_test_split(lecture_note_dataset, test_size=args.dev_size)
	utils.write2csv(lecture_note_dataset, args.output, constants.note_tsv_header)
	utils.write2csv(train_dataset, args.train_output, constants.note_tsv_header)
	utils.write2csv(dev_dataset, args.dev_output, constants.note_tsv_header)
