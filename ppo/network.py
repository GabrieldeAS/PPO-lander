
import torch
from torch import nn
import torch.nn.functional as F
import numpy as np

# check if this standard size is ok
class FeedForwardNN(nn.Module):
    def __init__(self, in_dim, out_dim):

        super(FeedForwardNN, self).__init__()

        self.layer1 = nn.Linear(in_dim, 64)
        self.layer2 = nn.Linear(64, 64)
        self.layer3 = nn.Linear(64, 64) # 1 additional layer
        self.layer4 = nn.Linear(64, out_dim)

        #print(out_dim)

    def forward(self, obs):
        # Convert observation to tensor if it's a numpy array
        if isinstance(obs, np.ndarray):
            obs = torch.tensor(obs, dtype=torch.float)
        
        activation1 = F.relu(self.layer1(obs))
        activation2 = F.relu(self.layer2(activation1))
        activation3 = F.relu(self.layer3(activation2))
        output = self.layer4(activation3)

        return output
