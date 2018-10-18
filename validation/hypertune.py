import itertools 
import os
import subprocess
import numpy as np


HomeDir = os.environ.get('HOME')
# os.chdir(os.path.join(HomeDir,"CS3244/DrQA"))
os.chdir(os.path.join(HomeDir,"DrQA"))
# print(os.getcwd())


log_file = "validation/log_validation.txt"
csv_result = "validation/csv_result.csv"

#### Fixed Parameters ##
fixed_params ={
"--num-epoch" : 1,
"--embedding-file": "glove.840B.300d.txt",
"--model-name": "",
"--model-dir": "",
"--train-file": "ln_train-processed-corenlp.txt",
"--dev-file": "ln_dev-processed-corenlp.txt",
"--dev-json": "ln_dev.json",
"--train-json": "ln_train.json",
"--pretrained": "models/pre_trained_single/single.mdl"
}



#### Hyper parameters ###
params = {
"--batch-size" : [32],
"--model-type" : ['rnn'],
"--hidden-size" : [128],
"--doc-layers" : [3],
"--question-layers" :[3],
"--rnn-type" :['LSTM'],
"--concat-rnn-layers" : [True],
"--question-merge" :['self_attn'],
"--dropout-emb" :[0.4],
"--dropout-rnn" :[0.4],
"--dropout-rnn-output" :[True],
"--grad-clipping" :[10],
"--weight-decay" :[0],
"--momentum" :[0],
"--fix-embedding" :[True],
"--tune-partial" : [0],
"--rnn-padding" :[True, False],
"--max-len" : [15]}

all_comb = list(itertools.product(*params.values()))


result = open(csv_result,'w') 
header = list(params.keys())
header.extend(["best_F1","F1_dev","EM_dev","F1_train","EM_train",
	    "Train_Loss","Start_Train","End_Train","Exact_Train",
	    "Start_Dev","End_Dev","Exact_Dev"])
header = ",".join(header)
result.write(header+"\n")

for i,comb in enumerate(all_comb):
	CMD ="python scripts/reader/train.py"
	#print(os.path.exists(CMD))
	print( " ".join(list(map(lambda x: str(x),comb))))
	model_name = "_".join(list(map(lambda x: str(x),comb)))
	model_dir = "models/" + model_name + "/"
	subprocess.call(["bash", "-c", "mkdir " + model_dir])
	fixed_params["--model-name"] = model_name
	fixed_params["--model-dir"] = model_dir
	for name,value in fixed_params.items():
		CMD += " " + name + " " + str(value)
	for name,value in zip(list(params.keys()), list(comb)):
		CMD = CMD + " " +  name + " " + str(value)		
	print("*" *100)
	print("Training on " + str(i) + "th combination")
	print("CMD: " + CMD)
	print("_"*100)
	
	#os.system("bash -c \"" + CMD+"\"")
	subprocess.call(["bash","-c",CMD])
	log_result = list(map(lambda x:str(x),comb))
	with open(log_file,'r') as log:
		log_result.extend(log.readline().split(' '))
	result.write(",".join(log_result)+"\n")


result.close()
	
	
