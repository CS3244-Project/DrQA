import sys
import subprocess
import numpy as np
#### Last two argument should be number of pre_name (mturk_self) and nfold (10)

hide_output = True
args = sys.argv
cmd = " ".join(args[1:-2])

model_dir
n_fold = int(args[-1])
pre_name = args[-2]

scores = np.zeros((n_fold,11))

header = ["F1_dev","EM_dev","S_Dev","E_Dev","Ex_Dev",
	  "F1_tr","EM_tr","S_tr","E_tr","Ex_tr","T_Loss"]
with open("validation/cross_validation_result.txt",'w') as saveFile:
	saveFile.write(",".join(header)+'\n')
for i in range(1,n_fold+1):
	CMD ="python script/reader/train.py " + cmd +" "
	CMD += "--train-file folds/" + pre_name + "_train_"+ str(i)+"-processed-corenlp.txt "
	CMD += "--dev-file folds/" + pre_name +"_dev_"+str(i)+"-processed-corenlp.txt "
	CMD += "--dev-json folds/" + pre_name +"_dev_"+str(i)+".json"
        #if hide_output:
        #        CMD = CMD +" &> /dev/null"

	subprocess.call(['bash','-c',CMD])
	with open("validation/log_cross_validation.txt",'r') as log:
		line = log.readline().split(" ")[1:]
		scores[i-1,:] = list(map(lambda x:round(float(x),2),line))
		with open('validation/cross_validation_result.txt','a') as saveFile:
			saveFile.write(",".join(
				list(map(lambda x:str(round(float(x),2)),line)))+"\n")
print("Scores: ")
print("F1_dev","EM_dev","S_Dev","E_Dev","Ex_Dev",
      "F1_tr","EM_tr","S_tr","E_tr","Ex_tr","T_Loss")

print(scores)
print("Average Score: ")
print(np.mean(scores,axis=0))
with open('validation/cross_validation_result.txt','a') as saveFile:
	saveFile.write("Average :\n")
	saveFile.write(",".join([str(round(i,2)) for i in np.mean(scores,axis=0)]))	
	
