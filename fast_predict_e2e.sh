python scripts/predict_e2e.py data/datasets/ln_dev.json --reader-model models/wsQA_single/wsQA_single.mdl  --embedding-file data/embeddings/glove.840B.300d.txt --official --out-dir models/wsQA_single/ --retriever-model saved_tfidf/ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln_dev.db --n-docs 1
# python scripts/predict_e2e.py data/datasets/ln_dev.json --reader-model models/csQA_single/csQA_single.mdl  --embedding-file data/embeddings/glove.840B.300d.txt --official --out-dir models/csQA_single/ --retriever-model saved_tfidf/ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln_dev.db --n-docs 1
python scripts/predict_e2e.py data/datasets/ln_dev.json --reader-model models/pre_trained_single/single.mdl  --embedding-file data/embeddings/glove.840B.300d.txt --official --out-dir models/pretrained_single/ --retriever-model saved_tfidf/ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz  --doc-db saved_db/ln_dev.db --n-docs 1
