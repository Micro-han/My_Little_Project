import torch
import torch.nn as nn
import torch.utils.data
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.c1 = torch.nn.Conv2d(3, 16, 3, padding=1)
        self.c2 = torch.nn.Conv2d(16, 16, 3, padding=1)
        self.fc1 = nn.Linear(50 * 50 * 16, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 2)
        
    def forward(self, x):
        x = self.c1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = self.c2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        y = self.fc3(x)

        return y
