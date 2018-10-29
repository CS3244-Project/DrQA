import matplotlib
matplotlib.use('agg')
import sys, getopt
import pylab as plt

def main(argv):
	inFile = ''
	outFile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:O:",["ifile=", "ofile="])
	except getopt.GetoptError:
		print ('usage :-i <inputfilename> -O <outputfilename>')
		sys.exit(2)
	for opt, args in opts:
		if opt in ("-i", "--ifile"):
			inFile = args
		elif opt in ("-O", "--ofile"):
			outFile = args
	
	xList = [];
	yTrainF1 = [];
	yTrainEM = [];
	yDevF1 = [];
	yDevEM = [];
	epoch = 0;
	with open(inFile, 'r', encoding="utf-8") as inFileObj:		
		for line in inFileObj:
			val = line.split(" ")
			yDevF1.append(float(val[0]))
			yDevEM.append(float(val[1]))
			yTrainF1.append(float(val[2]))
			yTrainEM.append(float(val[3]))
			xList.append([epoch])
			epoch = epoch + 1
	
	fig, ax = plt.subplots()
	ax.plot(xList, yTrainF1, color='b', label='Train F1')
	ax.plot(xList, yDevF1, color='k', label='Dev F1')
	ax.plot(xList, yTrainEM, 'k--', color='b', label='Train EM')
	ax.plot(xList, yDevEM, 'k--', color='k', label ='Dev EM')
	ax.legend()
	for opt, args in opts:
		if opt in ("-O", "--ofile"):
			plt.savefig(outFile)
		else:
			plt.savefig('Plot')				
main(sys.argv[1:])

