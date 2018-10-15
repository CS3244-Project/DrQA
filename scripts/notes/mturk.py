import argparse
import constants
import csv
import os
import pdf_reader
import utils

from sklearn.model_selection import train_test_split

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
				"dept": dept
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

def download_pdf(pdf_urls, dest_path):
	for url in pdf_urls:
		download_script = "wget " + url
		move_script = "mv " + utils.path_leaf(url) + " " + dest_path
		os.system(download_script)
		os.system(move_script)

def build_lecture_note_dataset(mturk_source, mturk_response, data_dir, output, squash=True, verbose=True):
	mturk_source_data = read_mturk_source(mturk_source)
	mturk_response_data = read_mturk_response(mturk_response)

	pdf_urls = mturk_response_data.keys()
	download_pdf(pdf_urls, data_dir)

	lecture_note_dataset = []
	unique_questions = []
	not_found = []

	for url in pdf_urls:
		file_name = utils.path_leaf(url)
		file_path = data_dir + file_name
		_, paragraphs = pdf_reader.read_pdf(file_path)

		pdf_info = mturk_source_data[url]	
		title, dept = pdf_info["title"], pdf_info["dept"]

		for qa in mturk_response_data[url]:
			page, question, answer = qa["page"], qa["question"], qa["answer"]
			if question not in unique_questions:			
				answer = utils.normalize(answer)
				annotated_p = utils.normalize(paragraphs[int(page)-1])
				if answer in annotated_p:
					lecture_note_dataset.append([title, annotated_p, question, answer, dept])
					unique_questions.append(question)
				else:
					for p in paragraphs:
						p = utils.normalize(p)	
						if answer in p:	
							lecture_note_dataset.append([title, p, question, answer, dept])
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
	parser.add_argument('data_dir', type=str)
	parser.add_argument('output', type=str)
	parser.add_argument('train_output', type=str)
	parser.add_argument('dev_output', type=str)
	parser.add_argument('dev_size', type=float)
	args = parser.parse_args()

	lecture_note_dataset = build_lecture_note_dataset(args.mturk_source, args.mturk_response, args.data_dir, args.output)
	train_dataset, dev_dataset = train_test_split(lecture_note_dataset, test_size=args.dev_size)
	utils.write2csv(lecture_note_dataset, args.output, constants.note_tsv_header)
	utils.write2csv(train_dataset, args.train_output, constants.note_tsv_header)
	utils.write2csv(dev_dataset, args.dev_output, constants.note_tsv_header)
