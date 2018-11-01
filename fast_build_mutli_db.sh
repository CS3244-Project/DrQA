for i in {0..19}
do
	#python scripts/notes/annotation.py depts/dept_$i.csv depts/dept_$i.json
	#python scripts/retriever/build_db.py depts/dept_$i.json depts/db/dept_$i.db --preprocess scripts/retriever/prep_lecture_note.py
	#python scripts/retriever/build_tfidf.py depts/db/dept_$i.db depts/tfidf/
	#python scripts/convert/squad.py depts/dept_$i.json depts/dept_$i.txt
	python scripts/retriever/eval.py depts/dept_$i.txt --model depts/tfidf/dept_$i-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db depts/db/dept_$i.db --n-docs 1
done
