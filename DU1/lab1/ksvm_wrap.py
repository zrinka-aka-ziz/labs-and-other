import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
import data

class KSVMWrap:
    def __init__(self, X, Y_, param_svm_c, param_svm_gamma):
        """
        X, Y_:           podatci i točni indeksi razreda
        param_svm_c:     relativni značaj podatkovne cijene
        param_svm_gamma: širina RBF jezgre
        """
        self.classifier = svm.SVC(C=param_svm_c, gamma=param_svm_gamma)
        self.classifier.fit(X, Y_)

    def predict(self, X):
        return self.classifier.predict(X) # korištenje classifiera

    def get_scores(self, X):
        return self.classifier.decision_function(X)

    def support(self):
        return self.classifier.support_


if __name__ == '__main__':
    # inicijaliziraj generatore slučajnih brojeva
    np.random.seed(100)

    # instanciraj podatke X i labele Yoh_
    X, Y_ = data.sample_gmm_2d(6, 2, 10)

    svm_ = KSVMWrap(X, Y_, param_svm_c=1, param_svm_gamma='auto')
    Y = svm_.predict(X)

    accuracy, recall, precision = data.eval_perf_multi(Y, Y_)
    print(f'recall:{recall}')
    print(f'precision: {precision}')
    print(f'accuracy: {accuracy}')

    decfun = lambda x: svm_.predict(x)
    bbox = (np.min(X, axis=0), np.max(X, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)

    # graph the data points
    data.graph_data(X, Y_, Y, special=svm_.support())
    # show the plot

    plt.savefig("svm.jpg")
    #plt.show()
    
