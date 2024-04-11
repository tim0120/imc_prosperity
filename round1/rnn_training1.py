import pandas as pd
from pytorch_lightning import LightningModule
from pytorch_lightning import Trainer
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

class TimeSeriesDataset(Dataset):
    def __init__(self, data, window_size):
        self.data = torch.tensor(data).to(torch.float32)
        self.window_size = window_size

    def __len__(self):
        return len(self.data) - self.window_size

    def __getitem__(self, idx):
        x = self.data[idx:idx+self.window_size]
        y = self.data[idx+self.window_size]
        return x, y

class RNN(LightningModule):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        _, h = self.rnn(x)
        out = self.fc(h.squeeze(0))
        return out

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.MSELoss()(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=0.001)

data = pd.read_csv('starfruit_all_trades.csv')
data = data['price']

window_size = 20
dataset = TimeSeriesDataset(data, window_size=20)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

model = RNN(input_size=window_size, hidden_size=32, output_size=1)
trainer = Trainer(max_epochs=10)
trainer.fit(model, dataloader)

param_names = { 'rnn.weight_ih_l0': 'W_ih_l0', 'rnn.weight_hh_l0': 'W_hh_l0', 'rnn.bias_ih_l0': 'b_ih_l0', 'rnn.bias_hh_l0': 'b_hh_l0', 'fc.weight': 'fc_W', 'fc.bias': 'fc_b' }

def export_weights_to_txt(model, filename):
    with open(filename, 'w') as f:
        for name, param in model.state_dict().items():
            # Write the parameter name
            f.write(f'\t{param_names[name]} = [')
            # Convert the parameter tensor to a numpy array and write it to the file
            weight_array = param.cpu().numpy()
            length = len(weight_array)
            for i, row in enumerate(weight_array):
                if weight_array.ndim > 1:  # Check if the parameter is multi-dimensional
                    if i > 0:
                        f.write('\t')
                    f.write('[' + ', '.join(f'{w:.4f}' for w in row) + '],')
                    if i < length - 1:
                        f.write('\n')
                else:
                    f.write(f'[{row:.4f}],')
            f.write(']\n')

export_weights_to_txt(model, 'rnn_params.txt')