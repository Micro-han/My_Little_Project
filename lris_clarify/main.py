import torch
import torch.nn as nn
from sklearn import datasets
from sklearn.model_selection import train_test_split


lr = 0.0001
n_epochs = 10


class Net(nn.Module):
    def __init__(self, input_num, output_num, hidden_num):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_num, hidden_num)
        self.fc2 = nn.Linear(hidden_num, output_num)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


def train(x_train, x_test, y_train, y_test):
    model = Net(4, 10, 3)
    model = model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    for epoch in range(n_epochs):
        for i in range(10000):
            out = model.forward(x_train)
            loss = criterion(out, y_train)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print('epoch%d step%d: loss= % .4f' % (epoch, i, loss.item()))
        acc = 0.0
        sum = 0
        output = model(x_test)
        pred_y = torch.max(output, 1)[1].numpy()
        for i in range(len(y_test)):
            if pred_y[i] == y_test[i]:
                sum += 1
        acc = float(sum / len(y_test))
        print('epoch%d: accuracy = %d%%' % (epoch, acc * 100))

    torch.save(model, 'Iris_model.pkl')
    print(model)


def test(data, label):
    model = torch.load('Iris_model.pkl')
    output = model(data)
    pred_y = torch.max(output, 1)[1].numpy()
    sum = 0
    for i in range(len(label)):
        if pred_y[i] == label[i]:
            sum += 1
    acc = float(sum / len(label))
    print('model accuracy = %d%%' % (acc * 100))


if __name__ == '__main__':
    dataset = datasets.load_iris()
    data = torch.FloatTensor(dataset['data'])
    label = torch.LongTensor(dataset['target'])
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.2)
    mode = input()
    if mode == 'train':
        train(x_train, x_test, y_train, y_test)
    else:
        test(data, label)