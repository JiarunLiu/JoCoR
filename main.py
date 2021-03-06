# -*- coding:utf-8 -*-
import os
import torch
import torchvision
import torchvision.transforms as transforms
from data.cifar import CIFAR10, CIFAR100
from data.mnist import MNIST
import argparse, sys
import datetime
from algorithm.jocor import JoCoR

import json
from data.ISIC import ISIC

parser = argparse.ArgumentParser()
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--result_dir', type=str, help='dir to save result json files', default='results')
parser.add_argument('--noise_rate', type=float, help='corruption rate, should be less than 1', default=0.2)
parser.add_argument('--forget_rate', type=float, help='forget rate', default=None)
parser.add_argument('--noise_type', type=str, help='[pairflip, symmetric, asymmetric]', default='pairflip')
parser.add_argument('--num_gradual', type=int, default=10,
                    help='how many epochs for linear drop rate, can be 5, 10, 15. This parameter is equal to Tk for R(T) in Co-teaching paper.')
parser.add_argument('--exponent', type=float, default=1,
                    help='exponent of the forget rate, can be 0.5, 1, 2. This parameter is equal to c in Tc for R(T) in Co-teaching paper.')
parser.add_argument('--dataset', type=str, help='mnist, cifar10, or cifar100', default='mnist')
parser.add_argument('--n_epoch', type=int, default=320)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--print_freq', type=int, default=50)
parser.add_argument('--num_workers', type=int, default=4, help='how many subprocesses to use for data loading')
parser.add_argument('--num_iter_per_epoch', type=int, default=400)
parser.add_argument('--epoch_decay_start', type=int, default=80)
parser.add_argument('--gpu', type=int, default=None)
parser.add_argument('--co_lambda', type=float, default=0.1)
parser.add_argument('--adjust_lr', type=int, default=1)
parser.add_argument('--model_type', type=str, help='[mlp,cnn]', default='cnn')
parser.add_argument('--save_model', type=str, help='save model?', default="False")
parser.add_argument('--save_result', type=str, help='save result?', default="True")
parser.add_argument('--optimizer', type=str, help='SGD or Adam?', default="SGD")
parser.add_argument('--batch-size', dest='batch_size', type=int, help='batch size?', default=128)

args = parser.parse_args()

# Seed
torch.manual_seed(args.seed)
if args.gpu is not None:
    device = torch.device('cuda:{}'.format(args.gpu))
    torch.cuda.manual_seed(args.seed)

else:
    device = torch.device('cpu')
    torch.manual_seed(args.seed)

# Hyper Parameters
batch_size = args.batch_size
learning_rate = args.lr

# load dataset
if args.dataset == 'mnist':
    input_channel = 1
    num_classes = 10
    init_epoch = 0
    filter_outlier = True
    args.epoch_decay_start = 80
    args.model_type = "mlp"
    # args.n_epoch = 200
    transform1 = torchvision.transforms.Compose([
        # torchvision.transforms.RandomPerspective(),
        # torchvision.transforms.ColorJitter(0.2, 0.75, 0.25, 0.04),
        torchvision.transforms.ToTensor(),
    ])
    train_dataset = MNIST(root='./../Co-correcting_plus/data/mnist/',
                          download=False,
                          train=True,
                          transform=transform1,
                          noise_type=args.noise_type,
                          noise_rate=args.noise_rate
                          )

    test_dataset = MNIST(root='./../Co-correcting_plus/data/mnist/',
                         download=False,
                         train=False,
                         transform=transforms.ToTensor(),
                         noise_type=args.noise_type,
                         noise_rate=args.noise_rate
                         )
    # train_dataset = MNIST(root='./../../dataset/MNIST/',
    #                       download=False,
    #                       train=True,
    #                       transform=transforms.ToTensor(),
    #                       noise_type=args.noise_type,
    #                       noise_rate=args.noise_rate
    #                       )
    #
    # test_dataset = MNIST(root='./../../dataset/MNIST/',
    #                      download=False,
    #                      train=False,
    #                      transform=transforms.ToTensor(),
    #                      noise_type=args.noise_type,
    #                      noise_rate=args.noise_rate
    #                      )

if args.dataset == 'cifar10':
    input_channel = 3
    num_classes = 10
    init_epoch = 20
    args.epoch_decay_start = 80
    filter_outlier = True
    args.model_type = "cnn"
    # args.n_epoch = 200
    transform1 = torchvision.transforms.Compose([
        # torchvision.transforms.RandomHorizontalFlip(),
        # torchvision.transforms.RandomCrop(32, 4),
        torchvision.transforms.ToTensor(),
    ])
    train_dataset = CIFAR10(root='./../Co-correcting_plus/data/cifar10/',
                            download=False,
                            train=True,
                            transform=transform1,
                            noise_type=args.noise_type,
                            noise_rate=args.noise_rate
                            )

    test_dataset = CIFAR10(root='./../Co-correcting_plus/data/cifar10/',
                           download=False,
                           train=False,
                           transform=transforms.ToTensor(),
                           noise_type=args.noise_type,
                           noise_rate=args.noise_rate
                           )

if args.dataset == 'cifar100':
    input_channel = 3
    num_classes = 100
    init_epoch = 5
    args.epoch_decay_start = 100
    # args.n_epoch = 200
    filter_outlier = False
    args.model_type = "cnn"

    train_dataset = CIFAR100(root='./../Co-correcting_plus/data/cifar100/',
                             download=False,
                             train=True,
                             transform=transforms.ToTensor(),
                             noise_type=args.noise_type,
                             noise_rate=args.noise_rate
                             )

    test_dataset = CIFAR100(root='./../Co-correcting_plus/data/cifar100/',
                            download=False,
                            train=False,
                            transform=transforms.ToTensor(),
                            noise_type=args.noise_type,
                            noise_rate=args.noise_rate
                            )

if args.dataset == 'isic':
    input_channel = 3
    num_classes = 2
    init_epoch = 0
    args.epoch_decay_start = 80
    args.model_type = 'resnet50'

    transform = torchvision.transforms.Compose([
        torchvision.transforms.RandomHorizontalFlip(p=0.5),
        torchvision.transforms.RandomVerticalFlip(p=0.5),
        torchvision.transforms.RandomRotation(degrees=[-180, 180]),
        torchvision.transforms.Resize(224),
        torchvision.transforms.ToTensor(),
    ])
    transform1 = torchvision.transforms.Compose([
        torchvision.transforms.Resize(224),
        torchvision.transforms.ToTensor(),
    ])

    train_dataset = ISIC('/media/victoria/SSD-240G/JiarunLiu/datasets/ISIC-Archive-Downloader/NewData',
                         train=0,
                         transform=transform,
                         noise_type=args.noise_type,
                         noise_rate=args.noise_rate,
                         device=1,
                         redux=None,
                         image_size=224)
    test_dataset = ISIC('/media/victoria/SSD-240G/JiarunLiu/datasets/ISIC-Archive-Downloader/NewData',
                        train=1,
                        transform=transform1,
                        noise_type='clean',
                        noise_rate=0.0,
                        device=1,
                        redux=None,
                        image_size=224)


if args.forget_rate is None:
    forget_rate = args.noise_rate
else:
    forget_rate = args.forget_rate


def main():
    # Data Loader (Input Pipeline)
    print('loading dataset...')
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=batch_size,
                                               num_workers=args.num_workers,
                                               drop_last=True,
                                               shuffle=True)

    test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                              batch_size=batch_size,
                                              num_workers=args.num_workers,
                                              drop_last=True,
                                              shuffle=False)
    # Define models
    print('building model...')

    model = JoCoR(args, train_dataset, device, input_channel, num_classes)

    epoch = 0
    train_acc1 = 0
    train_acc2 = 0

    # evaluate models with random weights
    test_acc1, test_acc2 = model.evaluate(test_loader)

    print(
        'Epoch [%d/%d] Test Accuracy on the %s test images: Model1 %.4f %% Model2 %.4f ' % (
            epoch + 1, args.n_epoch, len(test_dataset), test_acc1, test_acc2))

    acc_list = []
    record_dict = {
        'train1': {'acc': []},
        'train2': {'acc': []},
        'test1': {'acc': []},
        'test2': {'acc': []},
        'val1': {'acc': []},
        'val2': {'acc': []},
    }
    os.makedirs(args.result_dir, exist_ok=True)
    # training
    for epoch in range(1, args.n_epoch):
        # train models
        train_acc1, train_acc2, pure_ratio_1_list, pure_ratio_2_list = model.train(train_loader, epoch)

        # evaluate models
        test_acc1, test_acc2 = model.evaluate(test_loader)

        # save results
        if pure_ratio_1_list is None or len(pure_ratio_1_list) == 0:
            print(
                'Epoch [%d/%d] Test Accuracy on the %s test images: Model1 %.4f %% Model2 %.4f' % (
                    epoch + 1, args.n_epoch, len(test_dataset), test_acc1, test_acc2))
        else:
            # save results
            mean_pure_ratio1 = sum(pure_ratio_1_list) / len(pure_ratio_1_list)
            mean_pure_ratio2 = sum(pure_ratio_2_list) / len(pure_ratio_2_list)
            print(
                'Epoch [%d/%d] Test Accuracy on the %s test images: Model1 %.4f %% Model2 %.4f %%, Pure Ratio 1 %.4f %%, Pure Ratio 2 %.4f %%' % (
                    epoch + 1, args.n_epoch, len(test_dataset), test_acc1, test_acc2, mean_pure_ratio1,
                    mean_pure_ratio2))

        if epoch >= 190:
            acc_list.extend([test_acc1, test_acc2])
        record_dict['train1']['acc'].append(train_acc1)
        record_dict['train2']['acc'].append(train_acc2)
        record_dict['val1']['acc'].append(test_acc1)
        record_dict['val2']['acc'].append(test_acc2)
        record_dict['test1']['acc'].append(test_acc1)
        record_dict['test2']['acc'].append(test_acc2)
        with open(os.path.join(args.result_dir, 'record.json'), 'w') as f:
            json.dump(record_dict, f, indent=4, sort_keys=True)

    avg_acc = sum(acc_list) / len(acc_list)
    print(len(acc_list))
    print("the average acc in last 10 epochs: {}".format(str(avg_acc)))


if __name__ == '__main__':
    main()
