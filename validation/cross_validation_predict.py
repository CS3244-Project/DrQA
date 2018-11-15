import sys
import subprocess
import os

def predict(model_fold_dir, data_fold_dir, cmd, verbose=True):
	for model_data in os.listdir(model_fold_dir):
		m_model = re.match(r".*\.mdl$", model_data)
		if m_model:
			for data in data_fold_dir:
				m_dev = re.match(r".*_dev\.json", data)
				if m_dev:
					model_path = os.path.join(model_fold_dir, model_data)
					dev_path = os.path.join(data_fold_dir, data)
					predict_cmd_format = "python {} {} --model {} --out-dir {}"
					predict_cmd = predict_cmd_format.format(dev_path, cmd, model_path, model_fold_dir)
					if verbose:
						print(predict_cmd)
					subprocess.call(["bash", "-c", predict_cmd])
			raise Exception("Cannot find dev dataset in {}".format(data_fold_dir))
	raise Exception("Cannot find model file in {}".format(model_fold_dir))


if __name__ == "__main__":
	args = sys.argv
	cmd = " ".join(args[1:-2])
	dataset, model_dir = args[-2], args[-1]

	for fold_dir in os.listdir(model_dir):
		data_fold_dir = os.path.join(data_dir, fold_dir)
		model_fold_dir = os.path.join(model_dir, fold_dir)
		try:
			predict(model_fold_dir, data_fold_dir, cmd)
		except Exception as e:
			print(str(e))
			print("Skip prediction of fold {}".format(fold_dir))
