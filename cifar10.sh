for seed in 1 2 3 4 5
do
  python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.2/trail_${seed} --lr 5e-3 --optimizer Adam --seed ${seed}
  python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.4 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.4/trail_${seed} --lr 5e-3 --optimizer Adam --seed ${seed}
  python main.py --dataset cifar10 --noise_type symmetric --noise_rate 0.8 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/sn_0.8/trail_${seed} --lr 5e-3 --optimizer Adam --seed ${seed}

  python main.py --dataset cifar10 --noise_type pairflip --noise_rate 0.2 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/pair_0.2/trail_${seed} --lr 5e-3 --optimizer Adam --seed ${seed}
  python main.py --dataset cifar10 --noise_type pairflip --noise_rate 0.45 --n_epoch 320 --co_lambda 0.95 --gpu 0 --result_dir ./results/cifar10/pair_0.45/trail_${seed} --lr 5e-3 --optimizer Adam --seed ${seed}
done