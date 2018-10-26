import argparse
import os
import re
import sys

from drqa.reader.official_eval import evaluate

def fold_evaluate(model_fold_dir, data_fold_dir):
	for model_data in os.listdir(model_fold_dir):
		m_preds = re.match(r".*\.preds$", model_data)
		if m_preds:
			for data in data_fold_dir:
				m_dev = re.match(r".*_dev\.json", data)
				if m_dev:
					preds_path = os.path.join(model_fold_dir, model_data)
					dev_path = os.path.join(data_fold_dir, data)
					with open(dev_path) as dataset_file:
				        dataset_json = json.load(dataset_file)
				        if (dataset_json['version'] != expected_version):
				            print('Evaluation expects v-' + expected_version +
				                  ', but got dataset with v-' + dataset_json['version'],
				                  file=sys.stderr)
				        dataset = dataset_json['data']
				    with open(preds_path) as prediction_file:
				        predictions = json.load(prediction_file)
				    return evaluate(dataset, predictions))
			raise Exception("Cannot find dev dataset in {}".format(data_fold_dir))
	raise Exception("Cannot find prediction file in {}".format(model_fold_dir))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('model_dir', type=str)
	parser.add_argument('data_dir', type=str)
	args = parser.parse_args()
	exact_match_results, f1_score_results = [], []

	for fold_dir in os.listdir(args.model_dir):
		data_fold_dir = os.path.join(data_dir, fold_dir)
		model_fold_dir = os.path.join(model_dir, fold_dir)
		try:
			fold_eval_result = fold_evaluate(model_fold_dir, data_fold_dir)
			exact_match_results += fold_eval_result["exact_match"]
			f1_score_results += fold_eval_result["f1"]
		except Exception as e:
			print(str(e))
			print("Skip evaluation of fold {}".format(fold_dir))
	print("Official evaluation of {} folds".format(len(f1_score_results)))
	print("Exact match: {}".format(sum(exact_match_results) / len(exact_match_results)))
	print("F1 score: {}".format(sum(f1_score_results) / len(f1_score_results)))