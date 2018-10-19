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


log_file = "validation/log_validation.txt"
csv_result = "validation/csv_result.csv"
hide_output = True
MAX_EVALS = 300
#### Fixed Parameters ##
fixed_params ={
"--num-epoch" : 10,
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
"--batch-size" : hp.choice('--batch-size',[32]),
"--model-type" : hp.choice('--model-type',['rnn']),
"--hidden-size": hp.choice('--hidden-size',[128]),
"--doc-layers" : hp.choice('--doc-layers',[3]),
"--question-layers" :hp.choice('--question-layers',[3]),
"--rnn-type" :hp.choice('--rnn-type',['LSTM']),
"--concat-rnn-layers" : hp.choice('--concat-rnn-layers',[True]),
"--question-merge" :hp.choice('--question-merge',['self_attn']),
"--dropout-emb" :hp.uniform('--dropout-emb',0,1),
"--dropout-rnn" :hp.uniform('--dropout-rnn',0,1),
"--dropout-rnn-output" :hp.choice('--dropout-rnn-output',[True,False]),
"--grad-clipping" :hp.choice('--grad-clipping',[10]),
"--weight-decay" :hp.uniform('--weight-decay',0.01,0.1),
"--momentum" :hp.choice('--momentum',[0]),
"--fix-embedding" :hp.choice('--fix-embedding',[True,False]),
"--tune-partial" : hp.randint('--tune-partial',2000),
"--rnn-padding" :hp.choice('--rnn-padding',[True, False]),
"--max-len" : hp.choice('--max-len',[15])}

def objective(param):
	start = time.time()
	CMD ="python scripts/reader/train.py"
	model_name = "_".join(list(map(lambda x: str(x),param.values())))
	model_dir = "models/" + model_name + "/"
	if os.path.isdir(model_dir):
		subprocess.call(["bash","-c","rm " +model_dir +"*"])
	else:
		subprocess.call(["bash", "-c", "mkdir " + model_dir])
	fixed_params["--model-name"] = model_name
	fixed_params["--model-dir"] = model_dir

	for name,value in fixed_params.items():
		CMD += " " + name + " " + str(value)
	for name,value in param.items():
		CMD = CMD + " " +  name + " " + str(value)
	if hide_output:
		CMD = CMD +" &> /dev/null"
	os.system("bash -c \"" + CMD+"\"")
	with open(log_file,'r') as log:
		log_ = log.readline().split(' ')
	F1 = -float(log_[0])
	end = time.time()
	time_elapsed = end -start
	print("Comb: " + str(ith[0]))
	print("F1: "+ str(log_[0]) +" EM: " + str(log_[1]))
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
results_df = pd.DataFrame({'time': [x['time'] for x in results], 
                           'loss': [x['loss'] for x in results],
                           'x': [x['x'] for x in results],
                            'iteration': list(range(len(results)))})
results_df = results_df.sort_values('loss', ascending = True)
results_df.to_csv('validation/data_frame_result.csv',sep =",")

