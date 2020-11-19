python main.py --dataset isic --noise_type symmetric --noise_rate 0.2 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/sn_0.2 --lr 5e-3
python main.py --dataset isic --noise_type symmetric --noise_rate 0.4 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/sn_0.4 --lr 5e-3
python main.py --dataset isic --noise_type symmetric --noise_rate 0.8 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/sn_0.8 --lr 5e-3

python main.py --dataset isic --noise_type pairflip --noise_rate 0.2 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/pair_0.2 --lr 5e-3
python main.py --dataset isic --noise_type pairflip --noise_rate 0.45 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/pair_0.45 --lr 5e-3