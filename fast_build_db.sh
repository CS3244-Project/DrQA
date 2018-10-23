rm saved_db/*
python scripts/retriever/build_db.py data/datasets/ln_dev.json saved_db/ln_dev.db --preprocess scripts/retriever/prep_lecture_note.py
python scripts/retriever/build_db.py data/datasets/ln.json saved_db/ln.db --preprocess scripts/retriever/prep_lecture_note.py
# python scripts/retriever/build_db.py data/datasets/SQuAD.json saved_db/squad.db --preprocess scripts/retriever/prep_lecture_note.py
