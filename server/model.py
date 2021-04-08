from resnet import resnet50
from torch import nn


class Deep_Net(nn.Module):
    def __init__(self, num_class = 1, load_pretrain_for_train = True):
        super(Deep_Net, self).__init__()
        self.inchannel = 3
        resnet_pretrained = resnet50(pretrained = load_pretrain_for_train, progress = True,
                                     num_classes = 1000,
                                     inchannel = self.inchannel)
        layers_resnet = list(resnet_pretrained.children())
        # print(layers_resnet)
        keep_layers = layers_resnet[:-1]
        self.pre_CNN = nn.Sequential(*keep_layers)
        self.fc = nn.Linear(2048, 1)

        self.loss_func = nn.BCEWithLogitsLoss()

    def forward(self, x, label = None):
        x = self.pre_CNN(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc(x)

        if (self.training):
            # print()
            # print('x shape:{}'.format(x.shape))
            # print('label shape:{}'.format(label.shape))
            assert x.shape == label.shape
            loss = self.loss_func(x, label)
            return loss
        else:
            pred_score = x.sigmoid()
            return pred_score
