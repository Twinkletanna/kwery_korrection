#!/bin/sh

#python preprocess.py -train_src train_600k_val_60k/data/src-train_incorrect.txt -train_tgt train_600k_val_60k/data/tgt-train_correct.txt -valid_src train_600k_val_60k/data/src-val_incorrect.txt -valid_tgt train_600k_val_60k/data/tgt-val_correct.txt -save_data train_600k_val_60k/correct_sample
echo "Preprocessing Done..."
#python train.py -data train_600k_val_60k/correct_sample -save_model train_600k_val_60k/models/correct_sample-model -train_steps 200000 -save_checkpoint_steps 5000 -world_size 1 -gpu_ranks 0
echo "Training Done..."
python translate.py -model train_600k_val_60k/models/correct_sample-model_step_200000.pt -src train_600k_val_60k/data/src-test_incorrect.txt -output train_600k_val_60k/predictions/pred_sample_incorrect.txt -replace_unk
echo "Translation DOne..."
python calculatebleu.py "train_600k_val_60k/predictions/pred_sample_incorrect.txt" "train_600k_val_60k/data/tgt-test_correct.txt"
echo "Script Done..."

#python preprocess.py -train_src data/src-train_incorrect.txt -train_tgt data/tgt-train_correct.txt -valid_src data/src-val_incorrect.txt -valid_tgt data/tgt-val_correct.txt -save_data data/correct_sample
#echo "Preprocessing Done..."
#python train.py -data data/correct_sample -save_model models_nmt/correct_sample-model -train_steps 100000 -save_checkpoint_steps 5000 -world_size 1 -gpu_ranks 0
#echo "Training Done..."
#python translate.py -model models_nmt/correct_sample-model_step_100000.pt -src data/src-test_incorrect.txt -output predictions_nmt/pred_sample_incorrect.txt -replace_unk -verbose
#echo "Translation DOne..."
#python calculatebleu.py "predictions_nmt/pred_sample_incorrect.txt" "data/tgt-test_correct.txt"
#echo "Script Done..."

