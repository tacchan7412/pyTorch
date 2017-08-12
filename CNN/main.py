# imports
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim

# Network Definition
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(20, 50, 5)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.dense = nn.Linear(4*4*50, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = self.flatten(x)
        x = F.softmax(self.dense(x))
        return x

    def flatten(self, x):
        # 4 dimension -> 2 dimension
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return x.view(-1, num_features)

net = Net()

# loading MNIST datasets
transform = transforms.Compose(
    [transforms.ToTensor(), # PILImage to Tensor
     transforms.Normalize((0.1307,), (0.3081,)) # Normalization
     ])

trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=100, shuffle=True)

testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

# Train
n_epochs = 10
for epoch in range(n_epochs):
    print('EPOCH: %d' %epoch)
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(trainloader):
        inputs = Variable(inputs)
        labels = Variable(labels)

        optimizer.zero_grad()

        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.data[0]

        if i % 100 == 99:
            print(i + 1)
            print('loss: %f' %(running_loss / 100))
            running_loss = 0.0

# Test
correct = 0
total = 0
for (images, labels) in testloader:
    outputs = net(Variable(images))
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum()

print('Accuracy: %f' %(correct / total))
