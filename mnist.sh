
python main.py --dataset mnist --noise_type symmetric --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/mnist_SGD/sn_0.2 --lr 1e-4 --optimizer SGD
python main.py --dataset mnist --noise_type symmetric --noise_rate 0.4 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/mnist_SGD/sn_0.4 --lr 1e-4 --optimizer SGD
python main.py --dataset mnist --noise_type symmetric --noise_rate 0.8 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/mnist_SGD/sn_0.8 --lr 1e-4 --optimizer SGD

python main.py --dataset mnist --noise_type pairflip --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/mnist_SGD/pair_0.2 --lr 1e-4 --optimizer SGD
python main.py --dataset mnist --noise_type pairflip --noiseupda_rate 0.45 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/mnist_SGD/pair_0.45 --lr 1e-4 --optimizer SGD