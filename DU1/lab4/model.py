import torch
import torch.nn as nn
import torch.nn.functional as F


class _BNReluConv(nn.Sequential): 
    def __init__(self, num_maps_in, num_maps_out, k=3, bias=True):
        super(_BNReluConv, self).__init__()
        self.model = nn.Sequential(
            nn.BatchNorm2d(num_maps_in),
            nn.ReLU(),
            nn.Conv2d(num_maps_in,num_maps_out, kernel_size=k, bias=bias)
        )

class SimpleMetricEmbedding(nn.Module): #base model for training
    def __init__(self, input_channels, emb_size=32):
        super().__init__()
        self.emb_size = emb_size
        self.bnreluconv1 = _BNReluConv(input_channels, emb_size, 3)
        self.maxpool = nn.MaxPool2d(3, 2)
        self.bnreluconv2 = _BNReluConv(emb_size, emb_size, 3)
        self.bnreluconv3 = _BNReluConv(emb_size, emb_size, 3)
        self.avgpool = nn.AvgPool2d(2)




    def get_features(self, img): 
        # Returns tensor with dimensions BATCH_SIZE, EMB_SIZE
        x = self.bnreluconv1(img)
        x = self.maxpool(x)
        x = self.bnreluconv2(x)
        x = self.maxpool(x)
        x = self.bnreluconv3(x)
        x = self.avgpool(x)
        x = torch.squeeze(x)
        return x

    def loss(self, anchor, positive, negative): #triplet margin loss
        a_x = self.get_features(anchor)
        p_x = self.get_features(positive)
        n_x = self.get_features(negative)
        loss = torch.mean(torch.relu(torch.linalg.norm((a_x - p_x), dim=1) - torch.linalg.norm((a_x - n_x), dim=1) + 1)) #from pytorch
        return loss


class IdentityModel(nn.Module):
    def __init__(self):
        super(IdentityModel, self).__init__()

    def get_features(self, img): #no training, validation/testing only
        feats = torch.flatten(img)
        return feats
