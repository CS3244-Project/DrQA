import json
import pdf_reader
import utils

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
	pdf2json(["data/notes/Photosynthesis.pdf", "data/notes/Plant Physiology.pdf"], "out.json")