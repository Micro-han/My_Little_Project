import os
import torch.utils.data as data
from PIL import Image
import torch
import torchvision.transforms as transforms

IMAGE_SIZE = 200

dataTransform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.CenterCrop((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])


class PetsDataset(data.Dataset):
    def __init__(self, mode, path):
        self.mode = mode
        self.path = path
        self.list_img = []
        self.list_label = []
        self.data_size = 0
        self.transform = dataTransform
        self.cat_dir = ''
        self.dog_dir = ''
        # /archive/PetImages/Cat
        # /archive/PetImage/Dog
        if self.mode == 'train':
            self.cat_dir = self.path + '/Cat/'
            self.dog_dir = self.path + '/Dog/'
            for file in os.listdir(self.cat_dir):
                if file == '.DS_Store':
                    continue
                self.list_img.append(self.cat_dir + file)
                self.data_size += 1
                self.list_label.append(0)
            for file in os.listdir(self.dog_dir):
                if file == '.DS_Store':
                    continue
                self.list_img.append(self.dog_dir + file)
                self.data_size += 1
                self.list_label.append(1)
        elif self.mode == 'test':
            self.test_dir = self.path
            for file in os.listdir(self.test_dir):
                if file == '.DS_Store':
                    continue
                self.list_img.append(self.test_dir + file)
                self.data_size += 1
                self.list_label.append(-1)

    def __getitem__(self, item):
        if self.mode == 'train':
            img = Image.open(self.list_img[item]).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGB')
            label = self.list_label[item]
            return self.transform(img), torch.LongTensor([label])
        elif self.mode == 'test':
            img = Image.open(self.list_img[item]).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGB')
            return self.transform(img)

    def __len__(self):
        return self.data_size
