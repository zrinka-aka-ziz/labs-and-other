from torch.utils.data import Dataset
from collections import defaultdict
from random import choice
import torchvision


class MNISTMetricDataset(Dataset):
    def __init__(self, root="/tmp/mnist/", split='train', remove_class=None):
        super().__init__()
        assert split in ['train', 'test', 'traineval']
        self.root = root
        self.split = split
        mnist_ds = torchvision.datasets.MNIST(self.root, train='train' in split, download=True)
        self.images, self.targets = mnist_ds.data.float() / 255., mnist_ds.targets
        self.classes = list(range(10))

        if remove_class is not None: #remove class
            self.classes.remove(remove_class)
            remove = self.targets == remove_class #ako je ciljna ista kao ona za ukloniti, remove = True
            self.targets = self.targets[remove != True]
            self.images = self.images[remove != True]



        self.target2indices = defaultdict(list)
        for i in range(len(self.images)):
            self.target2indices[self.targets[i].item()] += [i]

    def _sample_negative(self, index): #razlicito od sidra/pozitivnog
        c = None
        con = True
        while con is True:
            c = choice(self.classes)
            if c != index:
                con = False
        return choice(self.target2indices[self.targets[c].item()])

    def _sample_positive(self, index): #isto kao sidro
        return choice(self.target2indices[self.targets[index].item()])

    def __getitem__(self, index):
        anchor = self.images[index].unsqueeze(0)
        target_id = self.targets[index].item()
        if self.split in ['traineval', 'val', 'test']:
            return anchor, target_id
        else:
            positive = self._sample_positive(index)
            negative = self._sample_negative(index)
            positive = self.images[positive]
            negative = self.images[negative]
            return anchor, positive.unsqueeze(0), negative.unsqueeze(0), target_id

    def __len__(self):
        return len(self.images)

if __name__ == '__main__':
    data = MNISTMetricDataset()
    print(data._sample_positive(0))
    print(data._sample_negative(0))
