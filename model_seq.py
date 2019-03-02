import torch
from namedtensor import ntorch, NamedTensor

class EncoderS2S(ntorch.nn.Module):
  def __init__(self, hidden_dim = 512, num_layers = 2, dropout=0.5):
    super(EncoderS2S, self).__init__()
    
    self.embedding = ntorch.nn.Embedding(len(DE.vocab), hidden_dim).spec("srcSeqlen", "embedding")
    self.dropout = ntorch.nn.Dropout(dropout)
    self.LSTM = ntorch.nn.LSTM(hidden_dim, hidden_dim, num_layers, dropout=dropout).spec("embedding", "srcSeqlen", "hidden")
  
  def forward(self, input, hidden=None): 
    input = ntorch.tensor(torch.flip(input.values, (0,)),("srcSeqlen","batch")) #reverse input
    
    x = self.embedding(input) 
    x = self.dropout(x)
    x, hidden = self.LSTM(x)
    return x, hidden

class DecoderS2S(ntorch.nn.Module):
  def __init__(self, hidden_dim = 512, num_layers = 2, dropout = 0.5):
    super(DecoderS2S, self).__init__()
    
    self.embedding = ntorch.nn.Embedding(len(EN.vocab), hidden_dim).spec("trgSeqlen", "embedding")
    self.dropout = ntorch.nn.Dropout(dropout)
    self.LSTM = ntorch.nn.LSTM(hidden_dim, hidden_dim, num_layers, dropout=dropout).spec("embedding", "trgSeqlen", "hidden")
    self.out = ntorch.nn.Linear(hidden_dim, len(EN.vocab)).spec("hidden", "vocab")
    
  def forward(self, input, hidden=None):
    x = self.embedding(input)
    x = self.dropout(x)
    x, hidden = self.LSTM(x, hidden)
    x = self.dropout(x)
    y = self.out(x)
    # No softmax because cross-entropy
    return y, hidden