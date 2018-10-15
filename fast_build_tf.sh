rm saved_tfidf/*
python scripts/retriever/build_tfidf.py saved_db/ln_dev.db saved_tfidf/
python scripts/retriever/build_tfidf.py saved_db/ln.db saved_tfidf/
python scripts/retriever/build_tfidf.py saved_db/squad.db saved_tfidf/
