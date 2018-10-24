import itertools
import os
import subprocess
import numpy as np
import time
import datetime
from hyperopt import hp
import pandas as pd
HomeDir = os.environ.get('HOME')
# os.chdir(os.path.join(HomeDir,"CS3244/DrQA"))
os.chdir(os.path.join(HomeDir,"DrQA"))
# print(os.getcwd())

top10_result = "validation/top10_result.csv"
hide_output = False
MAX_EVALS = 1
#### Fixed Parameters ##
fixed_params ={
"--num-epoch" : 1,
"--embedding-file": "glove.6B.200d.txt",
"--model-name": "",
"--model-dir": "",
"--train-file": "ln_train-processed-corenlp.txt",
"--dev-file": "ln_dev-processed-corenlp.txt",
"--dev-json": "ln_dev.json",
"--train-json": "ln_train.json",
"--pretrained": "models/pre_trained_single/64_2_no_concat_200.mdl"
}



#### Hyper parameters ###
params = {
"--batch-size" : hp.choice('--batch-size',[32]),
"--model-type" : hp.choice('--model-type',['rnn']),
"--hidden-size": hp.choice('--hidden-size',[64]),
"--doc-layers" : hp.choice('--doc-layers',[2]),
"--question-layers" :hp.choice('--question-layers',[2]),
"--rnn-type" :hp.choice('--rnn-type',['LSTM']),
"--concat-rnn-layers" : hp.choice('--concat-rnn-layers',[False]),
"--question-merge" :hp.choice('--question-merge',['self_attn']),
"--dropout-emb" :hp.uniform('--dropout-emb',0,1),
"--dropout-rnn" :hp.uniform('--dropout-rnn',0,1),
"--dropout-rnn-output" :hp.choice('--dropout-rnn-output',[True,False]),
"--grad-clipping" :hp.choice('--grad-clipping',[10]),
"--weight-decay" :hp.uniform('--weight-decay',0,1),
"--momentum" :hp.uniform('--momentum',0,1),
"--fix-embedding" :hp.choice('--fix-embedding',[True,False]),
"--tune-partial" : hp.choice('--tune-partial',[1000]),
"--rnn-padding" :hp.choice('--rnn-padding',[True, False]),
"--max-len" : hp.choice('--max-len',[15])}

def objective(param):
	start = time.time()
	CMD ="python scripts/reader/train.py"
	model_name = "_".join(list(map(lambda x: str(x),param.values())))
	model_dir = "models/val_models/" + model_name + "/"
	fixed_params["--model-name"] = model_name
	fixed_params["--model-dir"] = model_dir

	for name,value in fixed_params.items():
		CMD += " " + name + " " + str(value)
	for name,value in param.items():
		CMD = CMD + " " +  name + " " + str(value)
	if hide_output:
		CMD = CMD +" &> /dev/null"
	os.system("bash -c \"" + CMD+"\"")
	with open(model_dir + model_name+"_best.txt",'r') as log:
		log_ = log.readline().split(',')
	F1 = -float(log_[1])
	end = time.time()
	time_elapsed = end -start
	print("Comb: " + str(ith[0]))
	print("F1: "+ str(log_[1]) +" EM: " + str(log_[2]))
	print("Time Elapsed: " + str(datetime.timedelta(seconds = time_elapsed)))
	print("Time Remaining: " + str(datetime.timedelta(seconds = time_elapsed*(MAX_EVALS -ith[0]))))
	print("_"*100)
	ith[0] = ith[0]+1
	results = {'loss':F1,'status': STATUS_OK, 'x': param, 'time':time_elapsed}

	return results

from hyperopt import Trials
from hyperopt import fmin
from hyperopt import rand, tpe
from hyperopt import STATUS_OK

ith = [1]
tpe_algo = tpe.suggest
tpe_trials = Trials()
best = fmin(fn = objective,space = params,algo=tpe_algo, trials= tpe_trials,
	    max_evals = MAX_EVALS,rstate = np.random.RandomState(50))

print('Minimum loss attained with TPE:    {:.4f}'.format(tpe_trials.best_trial['result']['loss']))
print(len(tpe_trials.results))
results = tpe_trials.results
results_df = pd.DataFrame({'loss': [x['loss'] for x in results],
                           'x': [x['x'] for x in results] })
results_df = results_df.sort_values('loss', ascending = True)
results_df.to_csv('validation/data_frame_result.csv',sep =",")

result = open(top10_result,'w')
header = ",".join(['epoch_best','F1_Dev_best','EM_Dev_best','S_Dev_best','E_Dev_best','Exact_Dev_best','F1_Train','EM_train','S_Train','E_Train','Exact_Train','Loss_Train'])
result.write(header+"\n")
if len(results)>=10:
	top_10 = int(len(results)/20)
else:
	top_10 = 1
for i in range(top_10):
	param  = results[i]['x']
	CMD ="python scripts/reader/train.py"
	model_name = "_".join(list(map(lambda x: str(x),param.values())))
	model_dir = "models/val_models/" + model_name + "/"
	fixed_params["--model-name"] = model_name
	fixed_params["--model-dir"] = model_dir
	fixed_params["--num-epoch"] = 1

	for name,value in fixed_params.items():
		CMD += " " + name + " " + str(value)
	for name,value in param.items():
		CMD = CMD + " " +  name + " " + str(value)
	if hide_output:
		CMD = CMD +" &> /dev/null"

	os.system("bash -c \"" + CMD+"\"")
	log_result =[]
	with open(model_dir + model_name+"_best.txt",'r') as log:
		log_ = log.readline().split(' ')
	log_result.extend(log_)
	result.write(",".join(log_result)+"\n")
result.close()
