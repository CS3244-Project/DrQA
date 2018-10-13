from difflib import SequenceMatcher
import csv
import ntpath
import re
import uuid

def is_similar_str(str1, str2, threshold=0.8):
	str1 = re.sub(r'\W+', '', str1)
	str2 = re.sub(r'\W+', '', str2)
	score = SequenceMatcher(None, str1, str2).ratio()
	return score >= threshold

def get_uuid(str_len=24):
	return str(uuid.uuid4())[:str_len]

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def write2csv(data, out_path, header=None):
	csv_file_out = open(out_path, 'wt')
	csv_writer = csv.writer(csv_file_out, delimiter=',', lineterminator='\n')
	if header:
		csv_writer.writerow(header)

	for d in data:
		csv_writer.writerow(d)

	csv_file_out.close()
