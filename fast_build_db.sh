rm saved_db/*
python scripts/retriever/build_db.py data/datasets/Combined-SQuAD-LNQA.json saved_db/Combined-SQuAD-LNQA.db --preprocess scripts/retriever/prep_lecture_note.py

