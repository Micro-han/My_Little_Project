import os
from PIL import Image
import matplotlib.pyplot as plt
import getdata

from getdata import PetsDataset as PetsDataset
from torch.utils.data import DataLoader as DataLoader
from network import Net
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F


dataset_dir = './archive/PetImages'
model_cp = './model/'
workers = 10
batch_size = 16
lr = 0.0001
n_epoch = 2
model_file = './model/model.pth'
test_dir = './test/'
IMAGE_SIZE = 200


def train():
    data_file = PetsDataset('train', dataset_dir)
    data_loader = DataLoader(data_file, batch_size=batch_size, shuffle=True, num_workers=0, drop_last=True)

    model = Net()
    if torch.cuda.is_available():
        model = model.cuda()
    model = nn.DataParallel(model)
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    cnt = 0
    for epoch in range(n_epoch):
        for img, label in data_loader:
            if torch.cuda.is_available():
                img, label = Variable(img).cuda(), Variable(label).cuda()
            else:
                img, label = Variable(img).cpu(), Variable(label).cpu()
            out = model(img)
            loss = criterion(out, label.squeeze())
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            cnt += 1
            print('Epoch: {0}, Frame: {1}, train_loss: {2}'.format(epoch, cnt * batch_size, loss / batch_size))
    torch.save(model.state_dict(), '{0}model.pth'.format(model_cp))


def test():
    model = Net()
    if torch.cuda.is_available():
        model = model.cuda()
    model = nn.DataParallel(model)
    model.load_state_dict(torch.load(model_file))
    model.eval()

    files = []
    imgs = []
    imgs_data = []
    for file in os.listdir(test_dir):
        if file == '.DS_Store':
            continue
        files.append(file)
        img = Image.open(test_dir + file).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGB')
        img_data = getdata.dataTransform(img)

        imgs.append(img)
        imgs_data.append(img_data)

    imgs_data = torch.stack(imgs_data)

    out = model(imgs_data)
    out = F.softmax(out, dim=1)
    out = out.data.cpu().numpy()

    for idx in range(len(files)):
        print(files[idx], out[idx, 0], out[idx, 1])
        plt.figure()
        if out[idx, 0] > out[idx, 1]:
            plt.suptitle('cat: {:.1%}, dog: {:.1%}'.format(out[idx, 0], out[idx, 1]))
        else:
            plt.suptitle('dog: {:.1%}, cat: {:.1%}'.format(out[idx, 1], out[idx, 0]))
        plt.imshow(imgs[idx])
    plt.show()


if __name__ == '__main__':
    mode = input()
    if mode == 'train':
        train()
    else:
        test()
