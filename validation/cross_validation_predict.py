import sys
import subprocess
import os
import re
import utils

def predict(model_fold_dir, data_dir, fold_num, cmd, verbose=True):
	pred_python = "scripts/reader/predict.py"
	for model_data in os.listdir(model_fold_dir):
		print(model_data)
		m_model = re.match(r".*\.mdl$", model_data)
		if m_model:
			data = utils.get_data(data_dir, "dev", fold_num)
			model_path = os.path.join(model_fold_dir, model_data)
			dev_path = os.path.join(data_dir, data)
			predict_cmd_format = "python {} {} {} --model {} --out-dir {}"
			predict_cmd = predict_cmd_format.format(pred_python, dev_path, cmd, model_path, model_fold_dir)
			if verbose:
				print(predict_cmd)
			subprocess.call(["bash", "-c", predict_cmd])
			return
	raise Exception("Cannot find model file in {}".format(model_fold_dir))


if __name__ == "__main__":
	args = sys.argv
	cmd = " ".join(args[1:-2])
	data_dir, model_dir = args[-2], args[-1]

	for fold_dir in os.listdir(model_dir):	
		model_fold_dir = os.path.join(model_dir, fold_dir)
		fold_num = utils.get_fold_num(fold_dir)
		try:
			predict(model_fold_dir, data_dir, fold_num, cmd)
		except Exception as e:
			print(str(e))
			print("Skip prediction of fold {}".format(fold_dir))
