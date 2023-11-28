import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt

import data

class PTLogreg(nn.Module):
    def __init__(self, D, C):
        """Arguments:
           - D: dimensions of each datapoint
           - C: number of classes
        """
        super().__init__()
        # inicijalizirati parametre (koristite nn.Parameter):
        self.weights = nn.Parameter(torch.randn((D, C), dtype=torch.double))
        self.bias = nn.Parameter(torch.zeros(C))

    def forward(self, X):
        # unaprijedni prolaz modela: izračunati vjerojatnosti
        # koristiti: torch.mm, torch.softmax
        logits = X.mm(self.weights) + self.bias
        probs = torch.softmax(logits, dim=1)

        return probs

    def get_loss(self, X, Yoh_):
        # formulacija gubitka
        # koristiti: torch.log, torch.mean, torch.sum
        output = self.forward(X)

        loss_log = torch.log(output + 1e-13) * Yoh_  # dodavanje 1e-13 zbog prevencije NaN 
        loss_sum = torch.sum(loss_log, dim=1)
        loss_mean = torch.mean(loss_sum)

        return -loss_mean


def train(model, X, Yoh_, param_niter, param_delta, param_lambda):
    """Arguments:
       - X: model inputs [NxD], type: torch.Tensor
       - Yoh_: ground truth [NxC], type: torch.Tensor
       - param_niter: number of training iterations
       - param_delta: learning rate
    """

    # inicijalizacija optimizatora
    # ...
    optimizer = optim.SGD(params=model.parameters(), lr=param_delta)
    # petlja učenja
    # ispisujte gubitak tijekom učenja
    # ...
    for i in range(param_niter):
        loss = model.get_loss(X, Yoh_) + param_lambda * torch.norm(model.weights)
        loss.backward()
        optimizer.step()

        if i % 1000 == 0:
            print("iteration {}: loss {}".format(i, loss))

        optimizer.zero_grad()


def eval(model, X):
    """Arguments:
       - model: type: PTLogreg
       - X: actual datapoints [NxD], type: np.array
    """
    # ulaz je potrebno pretvoriti u torch.Tensor
    # izlaze je potrebno pretvoriti u numpy.array
    # koristite torch.Tensor.detach() i torch.Tensor.numpy()

    X_tensor = torch.from_numpy(X)
    return np.argmax(model.forward(X_tensor).detach().cpu().numpy(), axis=1)


if __name__ == "__main__":
    # inicijaliziraj generatore slučajnih brojeva
    np.random.seed(100)

    # instanciraj podatke X i labele Yoh_
    X_np, Y_np = data.sample_gauss_2d(3, 100)
    Yoh_ = data.class_to_onehot(Y_np)
    X, Yoh_ = torch.from_numpy(X_np), torch.from_numpy(Yoh_)
    # definiraj model:
    ptlr = PTLogreg(X.shape[1], Yoh_.shape[1])

    # nauči parametre (X i Yoh_ moraju biti tipa torch.Tensor):
    train(ptlr, X, Yoh_, 7000, 0.5, 1e-4)


    # dohvati vjerojatnosti na skupu za učenje
    probs = eval(ptlr, X_np)
    # ispiši performansu (preciznost i odziv po razredima)
    accuracy, recall, precision = data.eval_perf_multi(probs, Y_np)
    print(recall, precision)
    print()
    # iscrtaj rezultate, decizijsku plohu
    decfun = lambda x: eval(ptlr, x)
    bbox = (np.min(X_np, axis=0), np.max(X_np, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)

    # graph the data points
    data.graph_data(X_np, Y_np, probs, special=[])
    # show the plot
    plt.savefig("logreg.jpg") #save bc plt.show doesn't work
    #plt.show()
