import torch
import torchvision

print(torch.__version__)         # Should show 2.3.1+cpu
print(torchvision.__version__)   # Should show 0.18.1+cpu
print(torch.cuda.is_available()) # Should be False