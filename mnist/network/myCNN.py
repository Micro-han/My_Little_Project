import torch
import torch.nn as nn


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        """
            卷积(Conv2d)-> 激励函数(ReLU)->池化(MaxPooling)
            对于第一个卷积核：输入图像为灰度图，输入图像大小为(1,28,28)，输出图像为(16,28,28)；经过下采样后为(16,14,14)
            对于第二个卷积核：输入图像大小为(16,28,28)，输出图像为(32,14,14)；经过下采样后为(32,7,7)
            全连接层就为32 * 7 * 7，然后10分类输出
            
            把每一个批次的每一个输入都拉成一个维度，即(batch_size,32*7*7)
            因为pytorch里特征的形式是[bs,channel,h,w]，所以x.size(0)就是batchsize
            view就是把x弄成batchsize行个tensor
        """
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.out = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        y = self.out(x)
        return y