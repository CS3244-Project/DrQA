import constants
import pickle
import utils

with open("ln.p", "rb") as f:
	dataset = pickle.load(f)

dataset_dict = {}

for data in dataset:
	title, annotated_p, question, answer, dept, chapter = data
	if dept not in dataset_dict:
		dataset_dict[dept] = []
	dataset_dict[dept].append(data)

for i, k in enumerate(dataset_dict.keys()):
	utils.write2csv(dataset_dict[k], "depts/dept_" + str(i)+ ".csv", constants.note_tsv_header)
