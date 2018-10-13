import argparse
import constants
import csv
import os
import pdf_reader
import utils

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

	csv_file_out = open(output, 'wt')
	csv_writer = csv.writer(csv_file_out, delimiter=',', lineterminator='\n')
	csv_writer.writerow(constants.note_tsv_header)

	for url in pdf_urls:
		file_name = utils.path_leaf(url)
		file_path = data_dir + file_name
		_, paragraphs = pdf_reader.read_pdf(file_path)

		pdf_info = mturk_source_data[url]
		print(pdf_info["dept"])
		title, dept = pdf_info["title"], pdf_info["dept"]

		for qa in mturk_response_data[url]:
			page, question, answer = qa["page"], qa["question"], qa["answer"]
			paragraph = paragraphs[int(page)-1]
			# assert answer in paragraphs
			csv_writer.writerow([title, paragraphs[int(page)-1], question, answer, dept])

	csv_file_out.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('mturk_source', type=str)
	parser.add_argument('mturk_response', type=str)
	parser.add_argument('data_dir', type=str)
	parser.add_argument('output', type=str)
	args = parser.parse_args()

	build_lecture_note_dataset(args.mturk_source, args.mturk_response, args.data_dir, args.output)
