for i in {0..19}
# do
# 	python scripts/notes/annotation.py depts/dept_$i.csv depts/dept_$i.json
# 	python scripts/retriever/build_db.py depts/dept_$i.json depts/db/dept_$i.db --preprocess scripts/retriever/prep_lecture_note.py
# 	python scripts/retriever/build_tfidf.py depts/db/dept_$i.db depts/tfidf/
# 	python scripts/convert/squad.py depts/dept_$i.json depts/dept_$i.txt
# done

python scripts/notes/eval_multi.py depts/dept_{}.txt --model depts/tfidf/dept_{}-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db depts/db/dept_{}.db --n-docs 1

python scripts/notes/load_dataset.py
python scripts/notes/annotation.py depts/full.csv depts/full.json
python scripts/retriever/build_db.py depts/full.json depts/db/full.db --preprocess scripts/retriever/prep_lecture_note.py
python scripts/retriever/build_tfidf.py depts/db/full.db depts/tfidf/
python scripts/convert/squad.py depts/full.json depts/full.txt
python scripts/retriever/eval.py depts/full.txt --model depts/tfidf/full-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db depts/db/full.db --n-docs 1

