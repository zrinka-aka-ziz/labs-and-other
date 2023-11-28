import os
import math
import numpy as np
import skimage as ski
import skimage.io
import torch
from torch import nn
import torch.optim as optim
from pathlib import Path
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

DATA_DIR = Path(__file__).parent / 'datasets' / 'MNIST'
SAVE_DIR = Path(__file__).parent / 'out_z3001'

config = {}
config['max_epochs'] = 2
config['batch_size'] = 50
config['save_dir'] = SAVE_DIR
config['lr_policy'] = {1: {'lr': 1e-1}, 3: {'lr': 1e-2}, 5: {'lr': 1e-3}, 7: {'lr': 1e-4}}

class ConvolutionalModel(nn.Module):
    def __init__(self, in_channels, conv1_width, conv2_width, fc1_width, class_count):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, conv1_width, kernel_size=5, stride=1, padding=2, bias=True)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(conv1_width, conv2_width, kernel_size=5, padding=2)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        # potpuno povezani slojevi
        self.fc1 = nn.Linear(conv2_width * 7 * 7, fc1_width, bias=True)
        self.fc_logits = nn.Linear(fc1_width, class_count, bias=True)

        # parametri su već inicijalizirani pozivima Conv2d i Linear
        # možemo ih drugačije inicijalizirati
        self.reset_parameters()

    def reset_parameters(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear) and m is not self.fc_logits:
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
                nn.init.constant_(m.bias, 0)
        self.fc_logits.reset_parameters()

    def forward(self, x):
        h = self.conv1(x)
        h = self.pool1(h)
        h = torch.relu(h)  # može i h.relu() ili nn.functional.relu(h)
        h = self.conv2(h)
        h = self.pool2(h)
        h = torch.relu(h)
        h = h.view(h.shape[0], -1)
        h = self.fc1(h)
        h = torch.relu(h)
        logits = self.fc_logits(h)
        return logits


def draw_conv_filters(epoch, step, layer, save_dir):
    w = layer.weight.cpu().detach().numpy().copy()
    C = w.shape[1]
    num_filters = w.shape[0]
    k = int(w.shape[2])
    w = w.reshape(num_filters, C, k, k)
    w -= w.min()
    w /= w.max()
    border = 1
    cols = 8
    rows = math.ceil(num_filters / cols)
    width = cols * k + (cols - 1) * border
    height = rows * k + (rows - 1) * border
    # for i in range(C):
    for i in range(1):
        img = np.zeros([height, width])
        for j in range(num_filters):
            r = int(j / cols) * (k + border)
            c = int(j % cols) * (k + border)
            img[r:r + k, c:c + k] = w[j, i]
        filename = '%s_epoch_%02d_step_%06d_input_%03d.png' % ('conv1', epoch, step, i)
        img = img_as_ubyte(img)
        ski.io.imsave(os.path.join(save_dir, filename), img)


if __name__ == '__main__':
    print("Using device", device)
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5), (0.5))])
    ds_train, ds_test = MNIST(DATA_DIR, train=True, download=True, transform=transform), MNIST(DATA_DIR, train=False,
                                                                                               transform=transform)

    trainloader = torch.utils.data.DataLoader(ds_train, batch_size=config['batch_size'],
                                              shuffle=True, num_workers=2)

    testloader = torch.utils.data.DataLoader(ds_test, batch_size=config['batch_size'],
                                             shuffle=False, num_workers=2)

    net = ConvolutionalModel(in_channels=1, conv1_width=16, conv2_width=32, fc1_width=512, class_count=10).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9, weight_decay=0.001)
    epoch_step = []
    #epoch_num =[1, 2]
    loss_e_step = []
    for epoch in range(config['max_epochs']):  # loop over the dataset

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data[0].to(device), data[1].to(device)
            #print(inputs.shape)
            #exit(1)
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print stats
            running_loss += loss.item()
            if i % 100 == 0:  # print every 100 mini-batches
                if i != 0:
                    running_loss = running_loss / 100
                print(f"[{epoch}, {i*config['batch_size']:5d}] loss: {running_loss:.3f}")
                draw_conv_filters(epoch, i * config['batch_size'], net.conv1, SAVE_DIR)
                epoch_step.append(epoch * 10000 + i)
                loss_e_step.append(running_loss)
                running_loss = 0.0
            #loss_e_step.append(running_loss)

    print('Finished Training')
    plt.figure()
    plt.plot(epoch_step, loss_e_step)
    plt.savefig("reg001.jpg")
    #plt.show()

    correct = 0.
    total = 0.
    # not training, no need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in testloader:
            images, labels = data[0].to(device), data[1].to(device)
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy = prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy on 10000 test images: {100 * correct // total} %')
