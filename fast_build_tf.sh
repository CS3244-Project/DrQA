rm saved_tfidf/*
python scripts/retriever/build_tfidf.py saved_db/ln_train.db saved_tfidf/
python scripts/retriever/build_tfidf.py saved_db/SQuAD-v1.1-train.db saved_tfidf/ 
python scripts/retriever/build_tfidf.py saved_db/Combined-SQuAD-LNQA.db saved_tfidf/
