import argparse
import os
import re
import sys
import utils
import json

from scripts.reader.official_eval import evaluate

def fold_evaluate(model_fold_dir, data_fold_dir, fold_num):
	print(model_fold_dir, data_fold_dir)
	for model_data in os.listdir(model_fold_dir):
		m_preds = re.match(r".*\.preds$", model_data)
		if m_preds:
			data = utils.get_data(data_fold_dir, "dev", fold_num)
			preds_path = os.path.join(model_fold_dir, model_data)
			dev_path = os.path.join(data_fold_dir, data)
			with open(dev_path) as dataset_file:
			        dataset_json = json.load(dataset_file)
			        dataset = dataset_json['data']
			with open(preds_path) as prediction_file:
			        predictions = json.load(prediction_file)
			return evaluate(dataset, predictions)
	raise Exception("Cannot find prediction file in {}".format(model_fold_dir))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('model_dir', type=str)
	parser.add_argument('data_dir', type=str)
	args = parser.parse_args()
	exact_match_results, f1_score_results = [], []

	for fold_dir in os.listdir(args.model_dir):
		model_fold_dir = os.path.join(args.model_dir, fold_dir)
		fold_num = utils.get_fold_num(fold_dir)
		try:
			fold_eval_result = fold_evaluate(model_fold_dir, args.data_dir, fold_num)
			exact_match_results.append(fold_eval_result["exact_match"])
			f1_score_results.append(fold_eval_result["f1"])
		except Exception as e:
			print(str(e))
			print("Skip evaluation of fold {}".format(fold_dir))
	print("Official evaluation of {} folds".format(len(f1_score_results)))
	print("Exact match: {}".format(sum(exact_match_results) / len(exact_match_results)))
	print("F1 score: {}".format(sum(f1_score_results) / len(f1_score_results)))
