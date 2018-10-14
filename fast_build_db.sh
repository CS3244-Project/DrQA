rm saved_db/*
python scripts/retriever/build_db.py data/datasets/SQuAD-v1.1-train.json saved_db/SQuAD-v1.1-train.db --preprocess scripts/retriever/prep_lecture_note.py
python scripts/retriever/build_db.py data/datasets/ln_train.json saved_db/ln_train.db --preprocess scripts/retriever/prep_lecture_note.py
python scripts/retriever/build_db.py data/datasets/Combined-SQuAD-LNQA.json.json saved_db/Combined-SQuAD-LNQA.json.db --preprocess scripts/retriever/prep_lecture_note.py


