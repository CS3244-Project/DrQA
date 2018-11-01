import constants
import pickle
import utils

with open("ln.p", "rb") as f:
	dataset = pickle.load(f)

utils.write2csv(dataset, "depts/full.csv", constants.note_tsv_header)
