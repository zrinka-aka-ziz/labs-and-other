import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt
import data

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class PTDeep(nn.Module):
    def __init__(self, config):
        """Arguments:
           - config: Network confuguration
        """
        super().__init__()
        # inicijalizirati parametre (koristite nn.Parameter):
        weights_list = []
        bias_list = []
        for i in range(len(config) - 1):
            layer_weights = nn.Parameter(torch.randn((config[i], config[i + 1]), dtype=torch.float))
            layer_bias = nn.Parameter(torch.zeros(config[i + 1]))

            weights_list.append(layer_weights)
            bias_list.append(layer_bias)

        self.weights = nn.ParameterList(weights_list)
        self.bias = nn.ParameterList(bias_list)

    def forward(self, X):
        # unaprijedni prolaz modela: izračunati vjerojatnosti
        # koristiti: torch.mm, torch.softmax
        for weights, bias in zip(self.weights, self.bias):
            X = X.mm(weights) + bias
            X = torch.relu(X)

        return torch.softmax(X, dim=1)

    def get_loss(self, X, Yoh_):
        # formulacija gubitka
        # koristiti: torch.log, torch.mean, torch.sum
        output = self.forward(X)

        loss_log = torch.log(output + 1e-13) * Yoh_  # dodavanje 1e-13 zbog NaN
        loss_sum = torch.sum(loss_log, dim=1)
        return -torch.mean(loss_sum)

    def count_params(self):
        params = []
        params_len = 0
        for name, param in self.named_parameters():
            params.append((name, param))
            params_len += np.prod(list(param.size()))
        return params, params_len

def train(model, X, Yoh_, param_niter, param_delta, param_lambda):
    """Arguments:
       - X: model inputs [NxD], type: torch.Tensor
       - Yoh_: ground truth [NxC], type: torch.Tensor
       - param_niter: number of training iterations
       - param_delta: learning rate
    """

    # inicijalizacija optimizatora
    # ...
    optimizer = optim.SGD(params=model.parameters(), lr=param_delta, weight_decay=param_lambda)
    # petlja učenja
    # ispisujte gubitak tijekom učenja
    # ...
    for i in range(int(param_niter) + 1):
        loss = model.get_loss(X, Yoh_)
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

    X_tensor = torch.from_numpy(X).float().to(device)
    return np.argmax(model.forward(X_tensor).detach().cpu().numpy(), axis=1)


if __name__ == "__main__":
    # inicijaliziraj generatore slučajnih brojeva
    np.random.seed(100)

    # instanciraj podatke X i labele Yoh_
    X_np, Y_np = data.sample_gmm_2d(6,2,10)
    Yoh_ = data.class_to_onehot(Y_np)
    X, Yoh_ = torch.from_numpy(X_np).float().to(device), torch.from_numpy(Yoh_).float().to(device)
    # definiraj model:
    ptlr = PTDeep([2, 10, 10, 2]).to(device)
    # nauči parametre (X i Yoh_ moraju biti tipa torch.Tensor):
    train(ptlr, X, Yoh_, 1e4, 0.1,1e-4)

    # dohvati vjerojatnosti na skupu za učenje
    probs = eval(ptlr, X_np)
    # ispiši performansu (preciznost i odziv po razredima)
    accuracy, recall, precision = data.eval_perf_multi(probs, Y_np)
    print(f'recall:{recall}')
    print(f'precision: {precision}')
    print(f'accuracy: {accuracy}')

    # iscrtaj rezultate, decizijsku plohu
    decfun = lambda x: eval(ptlr, x)
    bbox = (np.min(X_np, axis=0), np.max(X_np, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)

    # graph the data points
    data.graph_data(X_np, Y_np, probs, special=[])

    plt.savefig("deep_6210_210102.jpg")
    #plt.show()
