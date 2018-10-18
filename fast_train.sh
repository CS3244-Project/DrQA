rm models/csQA_single/*
#rm models/csQA_multitask/*
rm models/wsQA_single/*
#rm models/wsQA_multitask/*
python scripts/reader/train.py --embedding-file glove.840B.300d.txt --tune-partial 1000 --model-dir models/csQA_single/ --model-name csQA_single --train-file ln_train-processed-corenlp.txt --dev-file ln_dev-processed-corenlp.txt --dev-json ln_dev.json
# python scripts/reader/train.py --embedding-file glove.840B.300d.txt --tune-partial 1000 --model-dir models/csQA_multi/ --model csQA_multitask --train-file ln_train-processed-corenlp.txt --dev-file ln_dev-processed-corenlp.txt --dev-json ln_dev.json
python scripts/reader/train.py --embedding-file glove.840B.300d.txt --tune-partial 1000 --model-dir models/wsQA_single/ --model-name wsQA_single --train-file ln_train-processed-corenlp.txt --dev-file ln_dev-processed-corenlp.txt --dev-json ln_dev.json --pretrained models/pre_trained_single/single.mdl
# python scripts/reader/train.py --embedding-file glove.840B.300d.txt --tune-partial 1000 --model-dir models/wsQA_multi/ --model wsQA_multitask --train-file ln_train-processed-corenlp.txt --dev-file ln_dev-processed-corenlp.txt --dev-json ln_dev.json --pretrained models/pre_trained_single/multi.mdl
