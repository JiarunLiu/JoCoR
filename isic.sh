echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.0 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/clean --lr 5e-3 --batch-size 32
echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.05 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/0.05 --lr 5e-3 --batch-size 32
echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.1 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/0.1 --lr 5e-3 --batch-size 32
echo `date`

echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.2 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/0.2 --lr 5e-3 --batch-size 32
echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.4 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/0.4 --lr 5e-3 --batch-size 32
echo `date`
python main.py --dataset isic --noise_type symmetric --noise_rate 0.5 --n_epoch 320 --co_lambda 0.9 --gpu 0 --result_dir ./results/isic/0.5 --lr 5e-3 --batch-size 32
echo `date`
