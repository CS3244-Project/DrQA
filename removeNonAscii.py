import sys, getopt

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

	with open(outFile, 'w') as outFileObj:
		with open(inFile, 'r', encoding="utf-8") as inFileObj:		
			for line in inFileObj:
					if all(ord(char) < 128 for char in line) :
						outFileObj.write(line)
						outFileObj.write('\n')
	
main(sys.argv[1:])

