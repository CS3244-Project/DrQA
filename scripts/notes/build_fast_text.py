import pickle
import random
import re

def paragraph_tokenize(paragraph):
	return re.split(r' *[\.\?!][\'"\)\]]* *', paragraph)

input_ln = "ln.p"
output_fast_text = "ln_dept.txt"
output_train = "ln_train.txt"
output_test = "ln_test.txt"

with open(input_ln, "rb") as f:
	dataset = pickle.load(f)

fast_text_format = "__label__{} {}"
contexts = []
fast_text = []
ssplit = []

train, test = [], []

for ln in dataset:
	c, q, d = ln[1], ln[2], ln[4]
	if c not in contexts:
		sents = paragraph_tokenize(c)
		for s in sents:
			s = s.rstrip().lstrip()	
			if len(s.split(" ")) > 3:
				ssplit.append(s.split(" "))		
				fast_text.append(fast_text_format.format(d, s))
				train.append(fast_text_format.format(d, s))
		contexts.append(c)
	fast_text.append(fast_text_format.format(d, q))
	test.append(fast_text_format.format(d, q))

random.shuffle(fast_text)

with open(output_fast_text, "w") as f:
	for line in fast_text:
		f.write(line + "\n")

with open(output_train, "w") as f:
        for line in train:
                f.write(line + "\n")

with open(output_test, "w") as f:
        for line in test:
                f.write(line + "\n")
