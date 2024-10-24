#encoder layer
#general encoder = n*encoder layer
from torch import nn
from MultiHeadAttn import MultiHeadAttention
from FeedForward import FeedForwardLayer
from helpers import clones

class Encoder(nn.Module):
    """Encoder Module of the Transformer"""
    def __init__(self,layers,encoder):
        super().__init__()
        assert isinstance(encoder,LayerEncoder)
        self.layers=layers
        self.encoder = encoder
        self.encoderlayers = clones(self.encoder,self.layers)
        self.norm = nn.LayerNorm(encoder.dmodel)

    def forward(self,x,mask):
        """Forward pass through all the encoder layers, depending
            on how many were specified."""
        src_tokens=x
        for encodinglayer in self.encoderlayers:
            src_tokens = encodinglayer(src_tokens,mask)
        return self.norm(src_tokens)

class LayerEncoder(nn.Module):
    """This is a single encoder layer.(no shit captain obvious....)"""

    def __init__(self, heads, dmodel):
        super().__init__()
        self.heads = heads
        self.dmodel = dmodel
        
        # Linear layers to transform inputs for attention
        
        # Multi-head attention layer
        self.mha = MultiHeadAttention(self.dmodel, self.heads)
        
        # Separate LayerNorm instances for attention and feed-forward parts
        self.norm1 = nn.LayerNorm(self.dmodel)  # For attention submodule
        self.norm2 = nn.LayerNorm(self.dmodel)  # For feed-forward submodule
        self.norm = nn.LayerNorm(self.dmodel)
        
        # Feed-forward layer
        self.ff = FeedForwardLayer(2048, self.dmodel)
        
        # Dropout for regularization
        self.dropout1 = nn.Dropout(p=0.1)
        self.dropout2 = nn.Dropout(p=0.1)

    def forward(self, x, src_mask):
        """Forward pass through a specific encoder layer."""
        #Encoder Block 1
        trb = self.norm(x)
        out_encoder = x + self.dropout1(self.mha(trb,trb,trb,mask=src_mask))
        #Encoder Block 2 
        output = out_encoder + self.dropout2(self.ff(self.norm2(out_encoder)))
        return output

