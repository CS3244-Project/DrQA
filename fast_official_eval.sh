python scripts/reader/official_eval.py data/datasets/ln_dev.json models/pre_trained_single/ln_dev-single.preds
python scripts/reader/official_eval.py data/datasets/ln_dev.json models/pre_trained_multi/ln_dev-multitask.preds
python scripts/reader/official_eval.py data/datasets/ln_dev.json models/csQA_single/ln_dev-csQA_single.preds
python scripts/reader/official_eval.py data/datasets/ln_dev.json models/wsQA_single/ln_dev-wsQA_single.preds
python scripts/reader/official_eval.py data/datasets/ln_dev.json models/wsQA_single/ln_dev-wsQA_single-ln_dev-tfidf-ngram=2-hash=16777216-tokenizer=simple-e2e.preds
python scripts/reader/official_eval.py data/datasets/ln_tokens_dev.json models/csQA_tokens_single/ln_tokens_dev-csQA_tokens_single.preds
python scripts/reader/official_eval.py data/datasets/ln_tokens_dev.json models/wsQA_tokens_single/ln_tokens_dev-wsQA_tokens_single.preds
