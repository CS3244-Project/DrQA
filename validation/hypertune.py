import itertools 
import os
import subprocess
import numpy as np
import time
import datetime

HomeDir = os.environ.get('HOME')
# os.chdir(os.path.join(HomeDir,"CS3244/DrQA"))
os.chdir(os.path.join(HomeDir,"DrQA"))
# print(os.getcwd())


log_file = "validation/log_validation.txt"
csv_result = "validation/csv_result.csv"
hide_output = False

#### Fixed Parameters ##
fixed_params ={
"--num-epoch" : 2,
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
header.extend(["model_name",
	    "F1_dev","EM_dev","F1_train","EM_train",
	    "Start_Dev","End_Dev","Exact_Dev",
	    "Start_Train","End_Train","Exact_Train","Train_Loss"])
header = ",".join(header)
result.write(header+"\n")

start_time = time.time()
for i,comb in enumerate(all_comb):
	## Record time
	start_train_time = time.time()	
	
	CMD ="python scripts/reader/train.py"
	#print(os.path.exists(CMD))
	
	model_name = "_".join(list(map(lambda x: str(x),comb)))
	model_dir = "models/" + model_name + "/"
	if os.path.isdir(model_dir):
		subprocess.call(["bash","-c","rm " +model_dir +"*"])
	else:
		subprocess.call(["bash", "-c", "mkdir " + model_dir])
	fixed_params["--model-name"] = model_name
	fixed_params["--model-dir"] = model_dir
	for name,value in fixed_params.items():
		CMD += " " + name + " " + str(value)
	for name,value in zip(list(params.keys()), list(comb)):
		CMD = CMD + " " +  name + " " + str(value)		
	if hide_output:
		CMD = CMD +" &> /dev/null"
	print("*" *100)
	print("Training on " + str(i+1) + "th combination")
	print("CMD: " + CMD)
	print("_"*100)
	os.system("bash -c \"" + CMD+"\"")
	
	log_result = [model_name]
	log_result.extend(list(map(lambda x:str(x),comb)))
	with open(log_file,'r') as log:
		log_ = log.readline().split(' ')
	log_result.extend(log_)
	result.write(",".join(log_result)+"\n")
	
	time_elapsed = datetime.timedelta(seconds = time.time() - start_time)
	time_remaining = datetime.timedelta(seconds =(time.time() -start_train_time)*(len(all_comb) - i-1))
	print("Time_Elapsed: " + str(time_elapsed))
	print("Time_Remaining: " + str(time_remaining))	
	print("Best F1_Dev: " + log_[0])
	print("Best EM: " + log_[1])
result.close()
	
	
