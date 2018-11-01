import os
import re

def get_data(data_dir, type_name, fold_num):
	for file_name in os.listdir(data_dir):
		re_pattern = ".*_{}_{}\.json$".format(type_name, fold_num)
		m = re.match(re_pattern, file_name)
		if m:
			return file_name
	raise Exception('Cannot get data type: {}, fold: {}, in {}'.format(type_name, fold_num, data_dir))

def get_fold_num(fold_dir):
	m = re.search('fold_(\d+)$', fold_dir)
	if m:
		return m.group(1)
	raise Exception('Cannot get fold number of fold dir: {}'.format(fold_dir))	
