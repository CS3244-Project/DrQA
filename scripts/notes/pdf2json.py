import json
import pdf_reader
import utils
import os
import subprocess
def pdf2json(file_paths, json_out, squash=True, titles=None):
	data = {'data': [], 'version': '1.1'}

	for i, file_path in enumerate(file_paths):
		_, paragraphs = pdf_reader.read_pdf(file_path, squash)
		title = titles[i] if titles else utils.path_leaf(file_path)
		doc = {
			'paragraphs': [],
			'title': title,
			'department': '',
			'chapter': ''
		}
		for p in paragraphs:
			doc['paragraphs'].append({
					'context': p,
					'qas': []
				})
		data['data'].append(doc)

	with open(json_out, 'w') as f:
		json.dump(data, f)

if __name__ == "__main__":
	#pdf2json(["data/notes/Photosynthesis.pdf", "data/notes/Plant Physiology.pdf"], "out.json")
	pdfs = []
	for pdf in os.listdir("step_demo/pdfs/"):
		pdfs.append("step_demo/pdfs/"+pdf)
	pdf2json(pdfs,"step_demo/combined_pdfs/combined.json")
	subprocess.call(["bash","-c","rm step_demo/db/*"])
	subprocess.call(["bash","-c","python scripts/retriever/build_db.py step_demo/combined_pdfs/combined.json step_demo/db/LN.db --preprocess scripts/retriever/prep_lecture_note.py"])
	subprocess.call(["bash","-c","python scripts/retriever/build_tfidf.py step_demo/db/LN.db step_demo/retriever_model/"])
	subprocess.call(["bash","-c","python scripts/pipeline/interactive.py --reader-model step_demo/reader_model/STeP_LNQA.mdl --retriever-model step_demo/retriever_model/LN-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz --doc-db step_demo/db/LN.db"])

