import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision.datasets
import matplotlib.pyplot as plt
import os
import cv2

from myCNN import CNN


n_epochs = 10
BATCH_SIZE = 50
LR = 0.001

train_data = torchvision.datasets.MNIST(root='./data', train=True, transform=torchvision.transforms.ToTensor(), download=True)
train_loader = Data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)
test_data = torchvision.datasets.MNIST(root='./data', train=False)
# torch.unsqueeze(a) 是用来对数据维度进行扩充，这样shape就从(2000,28,28)->(2000,1,28,28)
test_x = torch.unsqueeze(test_data.train_data, dim=1).type(torch.FloatTensor)[:2000] / 255
test_y = test_data.test_labels[:2000]


def train():
    cnn = CNN()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()
    for epoch in range(n_epochs):
        for step, (b_x, b_y) in enumerate(train_loader):
            y = cnn(b_x)
            loss = criterion(y, b_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if step % 50 == 0:
                test_out = cnn(test_x)
                pred_y = torch.max(test_out, 1)[1].data.numpy()
                acc = float((pred_y == test_y.data.numpy()).astype(int).sum()) / float(test_y.size(0))
                print('epoch:', epoch, 'train loss:', loss.data.numpy(), 'acc:', acc)
    torch.save(cnn.state_dict(), 'model.pkl')


def test():
    cnn = CNN()
    cnn.load_state_dict(torch.load('network/model.pkl'))
    cnn.eval()
    inputs = test_x[:1]

    outputs = cnn(inputs)
    print(inputs.shape[3])
    pred_y = torch.max(outputs, 1)[1].data.numpy()
    print(pred_y)


if __name__ == '__main__':
    mode = input()
    if mode == "train":
        train()
    else:
        test()