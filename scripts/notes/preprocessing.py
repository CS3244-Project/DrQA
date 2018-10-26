import argparse
import os
import subprocess
import re
import utils

def build_pp_cmd(input_dir, output_dir, file_name):
	m = re.search('^(.+?)\.json$', file_name)
	name = m.group(1) if m else 'default'
	cmd_format = 'python scripts/reader/preprocess.py {} {} --split {}'
	cmd = cmd_format.format(input_dir, output_dir, name)
	return cmd

def build_convert_cmd(input_dir, output_dir, file_name):
	m = re.search('^(.+?)\.json$', file_name)
	name = m.group(1) if m else 'default'
	cmd_format = 'python scripts/convert/squad.py {} {}'
	input_path = os.path.join(input_dir, file_name)
	output_path = os.path.join(output_dir, name)
	cmd = cmd_format.format(input_path, output_path)
	return cmd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input_dir', type=str)
	parser.add_argument('output_dir', type=str)
	args = parser.parse_args()

	for file_name in os.listdir(args.input_dir):
		if re.match(r".*\.json$", file_name):
			pp_cmd = build_pp_cmd(args.input_dir, args.output_dir, file_name)
			utils.run_cmd(pp_cmd)
			convert_cmd = build_convert_cmd(args.input_dir, args.output_dir, file_name)
			utils.run_cmd(convert_cmd)
