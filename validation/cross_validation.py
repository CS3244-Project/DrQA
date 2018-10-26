import sys
import subprocess
import numpy as np
import os
#### Last two argument should be number of pre_name (mturk_self) and nfold (10)

hide_output = True
args = sys.argv
cmd = " ".join(args[1:-3])
print(cmd)

n_fold = int(args[-1])
pre_name = args[-2]
model_dir = args[-3]

scores = np.zeros((n_fold,11))

header = ["F1_dev","EM_dev","S_Dev","E_Dev","Ex_Dev",
	  "F1_tr","EM_tr","S_tr","E_tr","Ex_tr","T_Loss"]
with open("validation/cross_validation_result.txt",'w') as saveFile:
	saveFile.write(",".join(header)+'\n')
for i in range(1,n_fold+1):
	subprocess.call(['bash', '-c', "mkdir " + model_dir + "fold_{}".format(i)])
	CMD ="python scripts/reader/train.py " + cmd +" "
	CMD += "--train-file folds/" + pre_name + "_train_"+ str(i)+"-processed-corenlp.txt "
	CMD += "--dev-file folds/" + pre_name +"_dev_"+str(i)+"-processed-corenlp.txt "
	CMD += "--train-json folds/" + pre_name +"_train_"+str(i)+".json "
	CMD += "--dev-json folds/" + pre_name +"_dev_"+str(i)+".json "
	CMD += "--model-dir " + model_dir + "fold_{}".format(i) + "/"
        #if hide_output:
        #        CMD = CMD +" &> /dev/null"
	print(CMD)
	subprocess.call(['bash','-c',CMD])
print("Scores: ")
print("F1_dev","EM_dev","S_Dev","E_Dev","Ex_Dev",
      "F1_tr","EM_tr","S_tr","E_tr","Ex_tr","T_Loss")

print(scores)
print("Average Score: ")
print(np.mean(scores,axis=0))
with open('validation/cross_validation_result.txt','a') as saveFile:
	saveFile.write("Average :\n")
	saveFile.write(",".join([str(round(i,2)) for i in np.mean(scores,axis=0)]))	
	
