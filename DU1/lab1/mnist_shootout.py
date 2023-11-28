import numpy as np
import torch
import torchvision
from matplotlib import pyplot as plt
import pt_deep
import data
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

dataset_root = './tmp/mnist'  # change this to your preference
mnist_train = torchvision.datasets.MNIST(dataset_root, train=True, download=True)
mnist_test = torchvision.datasets.MNIST(dataset_root, train=False, download=True)

x_train, y_train = mnist_train.data, mnist_train.targets
x_test, y_test = mnist_test.data, mnist_test.targets
x_train, x_test = x_train.float().div_(255.0), x_test.float().div_(255.0)

N = x_train.shape[0]
D = x_train.shape[1] * x_train.shape[2]
C = y_train.max().add_(1).item()

print(N, D, C)
print(x_train.shape)
print(x_test.shape)

#plt.imshow(x_train[0], cmap=plt.get_cmap('gray'))
#plt.show()

x_train_reshaped = torch.from_numpy(x_train.numpy().reshape(60000, 784)).float().to(device)
x_test_reshaped = torch.from_numpy(x_test.numpy().reshape(10000, 784)).float().to(device)
deep = pt_deep.PTDeep([784, 10]).to(device)
yoh_train = torch.from_numpy(data.class_to_onehot(y_train)).float().to(device)

pt_deep.train(deep, x_train_reshaped, yoh_train, param_niter=4000, param_delta=0.1, param_lambda=1e-4) # malo iteracija jer se dugo vrti

y = pt_deep.eval(deep, x_test_reshaped.detach().cpu().numpy())

accuracy, recall, precision = data.eval_perf_multi(y, y_test)
print(recall)
print(precision)
