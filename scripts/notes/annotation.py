import argparse
import constants
import csv
import json
import utils

def parse_annotation(file_path, start_row=1, verbose=True, version='1.1'):
	if verbose:
		print("Parsing annotation", file_path)

	csv_file_in = open(file_path, 'rt')
	csv_reader = csv.reader(csv_file_in, delimiter=',')

	data = {'data': [], 'version': version}

	for i, row in enumerate(csv_reader):
		if verbose and i % 10 == 0:
			print("Read row", str(i))
		if i >= start_row:
			title, context, question, answer, dept, chapter = row[:6]
			if len(question) == 0:
				continue
			has_added_title = False
			found_doc = None
			for doc in data['data']:
				if utils.is_similar_str(doc["title"], title):
					has_added_title = True
					found_doc = doc
			if not has_added_title:
				found_doc = {
					'paragraphs': [],
					'title': title,
					'department': dept,
					'chapter': chapter
				}
				data['data'].append(found_doc)
			has_added_context = False
			found_paragraph = None
			for paragraph in found_doc["paragraphs"]:
				if utils.is_similar_str(paragraph["context"], context):
					has_added_context = True
					found_paragraph = paragraph
			if not has_added_context:
				found_paragraph = {
					'context':context,
					'qas': []
				}
				found_doc["paragraphs"].append(found_paragraph)
			answer_start = context.lower().find(answer.lower())
			qa = {
				'answers': [{
				'answer_start': answer_start,
				'text': answer
				}],
				'question': question,
				'id': utils.get_uuid()
			}
			found_paragraph['qas'].append(qa)

	csv_file_in.close()
	return data

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input', type=str)
	parser.add_argument('output', type=str)
	args = parser.parse_args()

	parsed = parse_annotation(args.input)
	with open(args.output, 'w') as f:
		json.dump(parsed, f)
