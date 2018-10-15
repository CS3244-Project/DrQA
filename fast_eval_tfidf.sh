python scripts/retriever/eval.py data/datasets/ln.txt --model saved_tfidf/ln-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln.db --n-docs 5
python scripts/retriever/eval.py data/datasets/ln.txt --model saved_tfidf/ln-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln.db --n-docs 1
python scripts/retriever/eval.py data/datasets/ln_dev.txt --model saved_tfidf/ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln_dev.db --n-docs 5
python scripts/retriever/eval.py data/datasets/ln_dev.txt --model saved_tfidf/ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln_dev.db --n-docs 1
python scripts/retriever/eval.py data/datasets/SQuAD.txt --model saved_tfidf/squad-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/squad.db --n-docs 5
python scripts/retriever/eval.py data/datasets/SQuAD.txt --model saved_tfidf/squad-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/squad.db --n-docs 1
