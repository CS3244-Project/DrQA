import pickle
import re

def paragraph_tokenize(paragraph):
	return re.split(r' *[\.\?!][\'"\)\]]* *', paragraph)

input_ln = "ln.p"
output_fast_text = "ln_dept.txt"

with open(input_ln, "rb") as f:
	dataset = pickle.load(f)

fast_text_format = "__label__{} {}"
contexts = []
fast_text = []

for data in dataset:
	c, q, d = ln[1], ln[2], ln[4]
	if c not in contexts:
		sents = paragraph_tokenize(c)
		for s in sents:
			fast_text.append(fast_text_format.format(d, s))
		contexts.append(c)
	fast_text.append(fast_text_format.format(d, s))

with open(output_fast_text, "w") as f:
	for line in fast_text:
		f.write(line + "\n")