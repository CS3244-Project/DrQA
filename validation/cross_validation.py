import sys
import subprocess
import numpy as np
#### Last two argument should be number of pre_name (mturk_self) and nfold (10)

hide_output = True
args = sys.argv
cmd = " ".join(args[1:-2])

n_fold = int(args[-1])
pre_name = args[-2]

scores = np.zeros((n_fold,11))
for i in range(1,n_fold+1):
	CMD ="python script/reader/train.py " + cmd +" "
	CMD += "--train-file " + pre_name + "_train_"+ str(i)+"-processed-corenlp.txt "
	CMD += "--dev-file " + pre_name +"_dev_"+str(i)+"-processed-corenlp.txt "
	CMD += "--dev-json " + pre_name +"_dev_"+str(i)+".json"
        if hide_output:
                CMD = CMD +" &> /dev/null"

	subprocess('bash','-c',CMD)
	with open("validation/log_validation.txt",'r') as log:
		scores[i-1,:] = list(map(lambda x:round(float(x),2),log.readline().split(" ")))
print("Scores: ")
print("F1_dev","EM_dev","F1_tr","EM_tr",
            "S_Dev","E_Dev","Ex_Dev",
            "S_tr","E_tr","Ex_tr","T_Loss")

print(scores)
print("Average Score: ")
print(np.mean(scores,axis=0))
	
	
