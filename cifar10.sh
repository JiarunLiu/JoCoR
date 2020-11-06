
python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.2
python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.4 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.4
python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.8 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.8

python main.py --dataset cifar10 --noise_type pairflip --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/pair_0.2
python main.py --dataset cifar10 --noise_type pairflip --noise_rate 0.45 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/pair_0.45