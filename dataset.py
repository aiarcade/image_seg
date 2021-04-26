import os
import argparse
import random
import shutil
from shutil import copyfile
from misc import printProgressBar



def rm_mkdir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print('Remove path - %s'%dir_path)
    os.makedirs(dir_path)
    print('Create path - %s'%dir_path)

def main(config):

    rm_mkdir(config.train_path)
    rm_mkdir(config.train_GT_path)
    rm_mkdir(config.valid_path)
    rm_mkdir(config.valid_GT_path)
    rm_mkdir(config.test_path)
    rm_mkdir(config.test_GT_path)

    filenames = os.listdir(config.origin_data_path)
    data_list = []
    GT_list = []

    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext =='.jpg':
            filename = filename.split('_')[-1][:-len('.jpg')]
            data_list.append('ISIC_'+filename+'.jpg')
            GT_list.append('ISIC_'+filename+'_segmentation.png')

    num_total = len(data_list)
    num_train = int((config.train_ratio/(config.train_ratio+config.valid_ratio+config.test_ratio))*num_total)
    num_valid = int((config.valid_ratio/(config.train_ratio+config.valid_ratio+config.test_ratio))*num_total)
    num_test = num_total - num_train - num_valid

    print('\nNum of train set : ',num_train)
    print('\nNum of valid set : ',num_valid)
    print('\nNum of test set : ',num_test)

    Arange = list(range(num_total))
    random.shuffle(Arange)

    for i in range(num_train):
        idx = Arange.pop()
        
        src = os.path.join(config.origin_data_path, data_list[idx])
        dst = os.path.join(config.train_path,data_list[idx])
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.train_GT_path, GT_list[idx])
        copyfile(src, dst)

        printProgressBar(i + 1, num_train, prefix = 'Producing train set:', suffix = 'Complete', length = 50)
        

    for i in range(num_valid):
        idx = Arange.pop()

        src = os.path.join(config.origin_data_path, data_list[idx])
        dst = os.path.join(config.valid_path,data_list[idx])
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.valid_GT_path, GT_list[idx])
        copyfile(src, dst)

        printProgressBar(i + 1, num_valid, prefix = 'Producing valid set:', suffix = 'Complete', length = 50)

    for i in range(num_test):
        idx = Arange.pop()

        src = os.path.join(config.origin_data_path, data_list[idx])
        dst = os.path.join(config.test_path,data_list[idx])
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.test_GT_path, GT_list[idx])
        copyfile(src, dst)


        printProgressBar(i + 1, num_test, prefix = 'Producing test set:', suffix = 'Complete', length = 50)

class Map(dict):
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class CustomParser(object):
    def __init__(self):
        self.config={}
    def add_argument(self,flag,type,default):
        key=flag.replace("--","")
        if type==float:
            value=float(default)
        if type==str:
            value=str(default)
        if type==int:
            value=int(default)
        self.config[key]=value
    def parse_args(self):
        return Map(self.config)

parser = CustomParser()

# model hyper-parameters
parser.add_argument('--train_ratio', type=float, default=0.6)
parser.add_argument('--valid_ratio', type=float, default=0.2)
parser.add_argument('--test_ratio', type=float, default=0.2)
# data path
parser.add_argument('--origin_data_path', type=str, default='../ISIC2018_Task1-2_Training_Input')
parser.add_argument('--origin_GT_path', type=str, default='../ISIC2018_Task1_Training_GroundTruth')    
parser.add_argument('--train_path', type=str, default='./dataset/train/')
parser.add_argument('--train_GT_path', type=str, default='./dataset/train_GT/')
parser.add_argument('--valid_path', type=str, default='./dataset/valid/')
parser.add_argument('--valid_GT_path', type=str, default='./dataset/valid_GT/')
parser.add_argument('--test_path', type=str, default='./dataset/test/')
parser.add_argument('--test_GT_path', type=str, default='./dataset/test_GT/')

config = parser.parse_args()
print(config)
main(config)