import torch
import cv2
device = torch.device('cpu')
model = torch.load('convit_tiny.pth', map_location=device)

