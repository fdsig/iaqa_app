import torch
import cv2
import albumentations as A
from albumentations import pytorch
import torch.nn.functional as F
import torch.nn as nn
import timm


class Convit:
    def __init__(self):
        self.model_name = 'convit_tiny'
        self.model, self.device = self.load()
        self.preprocess = A.Compose([
            A.augmentations.geometric.resize.LongestMaxSize(max_size=224),
            A.augmentations.transforms.PadIfNeeded(224, 224),
            A.augmentations.transforms.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225),
                max_pixel_value=255.0, p=1.0),
            A.pytorch.transforms.ToTensorV2(transpose_mask=False, p=1.0)]
        )
        self.device = torch.device('cpu')
        

    def load(self):
        device = torch.device('cpu')
        weights = torch.load('convit_tiny.pth', map_location=device)
        weights = weights['model']
        model = timm.create_model(self.model_name, pretrained=True)
        model.head = nn.Linear(model.head.in_features, 2, bias=True)
        model.load_state_dict(weights)
        return model, device

    def read(self, img): return cv2.cvtColor(
        cv2.imread(img), cv2.COLOR_BGR2RGB)

    def infer(self, img):
        img = self.read(img)
        img_normalized = self.preprocess(image=img)['image'].float()
        img_normalized = img_normalized.unsqueeze_(0)
        # input = Variable(image_tensor)
        img_normalized = img_normalized.to(self.device)
        # print(img_normalized.shape)
        with torch.no_grad():
            self.model.eval()
            output = self.model(img_normalized)
            sm = torch.nn.Softmax(dim=1)
            return sm(output)
