rm saved_db/*
python scripts/retriever/build_db.py data/datasets/ln.json saved_db/ln.db --preprocess scripts/retriever/prep_lecture_note.py

