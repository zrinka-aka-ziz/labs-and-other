import os
import pickle
import numpy as np
import math
import skimage as ski
import skimage.io
import torch
from torch import nn
from pathlib import Path
from torch.optim.lr_scheduler import ExponentialLR
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
from torch.utils.data import random_split, DataLoader
from torchvision.datasets import CIFAR10
from torchvision.transforms import ToTensor
import torchvision.transforms as transforms

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

SAVE_DIR = Path(__file__).parent / 'out_z4'
config = {'max_epochs': 8, 'batch_size': 50, 'save_dir': SAVE_DIR,
          'lr_policy': {1: {'lr': 1e-1}, 3: {'lr': 1e-2}, 5: {'lr': 1e-3}, 7: {'lr': 1e-4}}}


class ConvolutionalModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=5)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5)
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc_logits = nn.Linear(128, 10)

    def forward(self, x):
        h = self.conv1(x)
        h = torch.relu(h)
        h = self.pool1(h)
        h = self.conv2(h)
        h = torch.relu(h)
        h = self.pool1(h)
        h = torch.flatten(h, 1)
        h = self.fc1(h)
        h = torch.relu(h)
        h = self.fc2(h)
        h = torch.relu(h)
        logits = self.fc_logits(h)
        return logits


def plot_training_progress(save_dir, data):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 8))

    linewidth = 2
    legend_size = 10
    train_color = 'm'
    val_color = 'c'

    num_points = len(data['train_loss'])
    x_data = np.linspace(1, num_points, num_points)
    ax1.set_title('Cross-entropy loss')
    ax1.plot(x_data, data['train_loss'], marker='o', color=train_color,
             linewidth=linewidth, linestyle='-', label='train')
    ax1.plot(x_data, data['valid_loss'], marker='o', color=val_color,
             linewidth=linewidth, linestyle='-', label='validation')
    ax1.legend(loc='upper right', fontsize=legend_size)
    ax2.set_title('Average class accuracy')
    ax2.plot(x_data, data['train_acc'], marker='o', color=train_color,
             linewidth=linewidth, linestyle='-', label='train')
    ax2.plot(x_data, data['valid_acc'], marker='o', color=val_color,
             linewidth=linewidth, linestyle='-', label='validation')
    ax2.legend(loc='upper left', fontsize=legend_size)
    ax3.set_title('Learning rate')
    ax3.plot(x_data, data['lr'], marker='o', color=train_color,
             linewidth=linewidth, linestyle='-', label='learning_rate')
    ax3.legend(loc='upper left', fontsize=legend_size)

    save_path = os.path.join(save_dir, 'training_plot.png')
    print('Plotting in: ', save_path)
    plt.savefig(save_path)


def draw_conv_filters(epoch, step, weights, save_dir):
    w = weights.copy()
    num_filters = w.shape[0]
    num_channels = w.shape[1]
    k = w.shape[2]
    assert w.shape[3] == w.shape[2]
    w = w.transpose(2, 3, 1, 0)
    w -= w.min()
    w /= w.max()
    border = 1
    cols = 8
    rows = math.ceil(num_filters / cols)
    width = cols * k + (cols - 1) * border
    height = rows * k + (rows - 1) * border
    img = np.zeros([height, width, num_channels])
    for i in range(num_filters):
        r = int(i / cols) * (k + border)
        c = int(i % cols) * (k + border)
        img[r:r + k, c:c + k, :] = w[:, :, :, i]
    filename = 'epoch_%02d_step_%06d.png' % (epoch, step)
    img = img_as_ubyte(img)
    ski.io.imsave(os.path.join(save_dir, filename), img)


crit = nn.CrossEntropyLoss()

def evaluate(model, loader):
    outputs = []
    for batch in loader:
        images, labels = batch[0].to(device), batch[1].to(device)
        out = model.forward(images)  # Generate predictions
        loss = crit(out, labels)  # Calculate loss
        _, preds = torch.max(out, dim=1)
        acc = torch.tensor(torch.sum(preds == labels).item() / len(preds))  # Calculate accuracy
        outputs.append({'loss': loss.detach(), 'acc': acc})


    batch_losses = [x['loss'] for x in outputs]
    epoch_loss = torch.stack(batch_losses).mean()  # Combine losses
    batch_accs = [x['acc'] for x in outputs]
    epoch_acc = torch.stack(batch_accs).mean()  # Combine accuracies
    return epoch_loss.cpu().numpy(), epoch_acc.cpu().numpy()


if __name__ == '__main__':
    print("Using device", device)
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    dataset = CIFAR10(root='data/', download=True, transform=transform)
    test_dataset = CIFAR10(root='data/', train=False, transform=transform)
    classes = dataset.classes

    val_size = 5000
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    bsz = 16

    train_loader = DataLoader(train_ds, bsz, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_ds, bsz * 2, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_dataset, bsz * 2, num_workers=4, pin_memory=True)

    net = ConvolutionalModel().to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.CrossEntropyLoss()
    scheduler = ExponentialLR(optimizer, gamma=0.9)
    plot_data = {'train_loss': [], 'valid_loss': [], 'train_acc': [], 'valid_acc': [], 'lr': []}

    num_epochs = config['max_epochs']
    for epoch in range(num_epochs):

        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            images, labels = data[0].to(device), data[1].to(device)

            optimizer.zero_grad()
            output = net.forward(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 100 == 99:
                print("epoch: {}, step: {}, batch_loss: {:4f}".format(epoch, i + 1, running_loss / 100))
                running_loss = 0.0
            if i % 200 == 0:
                draw_conv_filters(epoch, i, net.conv1.weight.detach().cpu().numpy(), SAVE_DIR)

        train_loss, train_acc = evaluate(net, train_loader)
        val_loss, val_acc = evaluate(net, val_loader)

        plot_data['train_loss'] += [train_loss]
        plot_data['valid_loss'] += [val_loss]
        plot_data['train_acc'] += [train_acc]
        plot_data['valid_acc'] += [val_acc]
        plot_data['lr'] += [scheduler.get_last_lr()]
        scheduler.step()

    plot_training_progress(SAVE_DIR, plot_data)
