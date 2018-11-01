import constants
import pickle
import utils

with open("ln.p") as f:
	dataset = pickle.load(f)

utils.write2csv(dataset_dict[k], "depts/full.csv", constants.note_tsv_header)
