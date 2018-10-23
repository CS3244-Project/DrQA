rm saved_tfidf/*
#python scripts/retriever/build_tfidf.py --ngram 3 saved_db/ln_dev.db saved_tfidf/
#python scripts/retriever/build_tfidf.py --ngram 3 saved_db/ln.db saved_tfidf/
#python scripts/retriever/build_tfidf.py --ngram 3 saved_db/squad.db saved_tfidf/

python scripts/retriever/build_tfidf.py --ngram 2 saved_db/ln_dev.db saved_tfidf/
python scripts/retriever/build_tfidf.py --ngram 2 saved_db/ln.db saved_tfidf/
#python scripts/retriever/build_tfidf.py --ngram 2 saved_db/squad.db saved_tfidf/
