import numpy as np
from matplotlib import pyplot as plt

import data

def fcann2_train(X, Y_, n_hidden_layer, param_niter, param_delta, param_lambda):
    N = len(X)
    input_size = len(X[0])
    n_classes = max(Y_) + 1
    W = [np.random.randn(input_size, n_hidden_layer), np.random.randn(n_hidden_layer, n_classes)]
    b = [np.zeros(n_hidden_layer), np.zeros(n_classes)]
    Yoh = data.class_to_onehot(Y_)

    for i in range(round(param_niter)):
        s1 = np.dot(X, W[0]) + b[0]
        h1 = np.maximum(s1, 0)
        s2 = np.dot(h1, W[1]) + b[1]
        expscores = np.exp(s2 - np.max(s2))  # N x C

        # softmax nazivnik
        sumexp = np.transpose([np.sum(expscores, axis=1)])  # N x 1
        # log vjerojatnosti razreda
        probs = expscores / sumexp  # N x C
        # loss
        loss = -np.sum(np.log(probs) * Yoh) / N  # scalar

        if i % 1000 == 0:
            print("iteration {}: loss {}".format(i, loss))

        # gradijenti
        dL_ds2 = np.subtract(probs, Yoh)
        dL_dW2 = np.dot(np.transpose(h1),dL_ds2)
        dL_db2 = np.sum(dL_ds2, axis=0)  # axis=1 sumira po retcima, a axis=0 sumira po stupcima
        dL_ds1 = np.dot(dL_ds2, np.transpose(W[1]))
        dL_ds1[s1 <= 0 ] = 0  # diag([[s1 > 0 ]]) postavljanje vrijedosti u nulu gdje  s1 <= 0
        dL_dW1 = np.dot(np.transpose(X), dL_ds1)
        dL_db1 = np.sum(dL_ds1, axis=0)

        # poboljšani parametri (backprop)
        W[1] += -param_delta * dL_dW2
        b[1] += -param_delta * dL_db2

        W[0] += -param_delta * dL_dW1
        b[0] += -param_delta * dL_db1

    return W, b

def fcann2_classify(X, W, b):
    s1 = np.dot(X, W[0]) + b[0]
    h1 = np.maximum(s1, 0)
    s2 = np.dot(h1, W[1]) + b[1]
    expscores = np.exp(s2 - np.max(s2))  # N x C

    # softmax naz
    sumexp = np.transpose([np.sum(expscores, axis=1)])  # N x 1
    # log vjerojatnosti razreda
    return np.argmax(expscores / sumexp, axis=1)


def fcann2_decfun(W, b):
    def classify(X):
        return fcann2_classify(X, W, b)
    return classify

if __name__ == '__main__':
    np.random.seed(100)

    # get the training dataset
    X, Y_ = data.sample_gmm_2d(6, 2, 10)

    # train the model
    W, b = fcann2_train(X, Y_, n_hidden_layer=20, param_niter=5000, param_delta=0.0005, param_lambda=1e-3)

    Y = fcann2_classify(X, W, b)
    # graph the decision surface
    decfun = fcann2_decfun(W, b)
    bbox = (np.min(X, axis=0), np.max(X, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)

    # graph the data points
    data.graph_data(X, Y_, Y, special=[])

    plt.savefig("fcann2.jpg") #save bc plt.show doesn't work
    #plt.show()
