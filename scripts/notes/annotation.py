import constants
import csv
import json
import utils

def parse_annotation(file_path, verbose=True):
	if verbose:
		print("Parsing", file_path)
	file_name = utils.path_leaf(file_path)
	if file_name[-4:] != ".csv":
		raise TypeError("Expecting input of csv file")

	csv_file_in = open(file_path, 'rt')
	csv_reader = csv.reader(csv_file_in, delimiter=',')

	has_started = False
	data = {'data': []}

	for i, row in enumerate(csv_reader):
		if verbose and i % 10 == 0:
			print("Read row", str(i))
		if has_started:
			title, context, question, answer = row
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
					'title': title
				}
				data['data'].append(found_doc)
			has_added_context = False
			found_paragraph = None
			for paragraph in found_doc["paragraph"]:
				if utils.is_similar_str(paragraph["context"], context):
					has_added_context = True
					found_paragraph = paragraph
			if not has_added_context:
				found_paragraph = {
					'context':context,
					'qas': []
				}
			qa = {
				'answers': [{
				'answer_start': context.find(answer),
				'text': answer
				}],
				'question': question,
				'id': utils.get_uuid()
			}
			found_paragraph['qas'].append(qa)
		if row == constants.note_tsv_header:
			has_started = True

	csv_file_in.close()
	return data

if __name__ = "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input', type=str)
	parser.add_argument('output', type=str)
	args = parser.parse_args()

	parsed = parse_annotation(args.input)
	with open(output, 'w') as f:
		json.dumps(parsed, f)
