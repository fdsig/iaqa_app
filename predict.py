import torch
import cv2
import albumentations as A
from albumentations import pytorch
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F
import torch.nn as nn
import timm


def load():
    device = torch.device('cpu')
    weights = torch.load('convit_tiny.pth', map_location=device)
    weights = weights['model']
    model_name = 'convit_tiny'
    model = timm.create_model(model_name , pretrained=True)
    model.head = nn.Linear(model.head.in_features,2,bias=True)
    model.load_state_dict(weights)
    return model, device

a_test_transform = A.Compose([
            A.augmentations.geometric.resize.LongestMaxSize(max_size=224),
            A.augmentations.transforms.PadIfNeeded(224,224),
            A.augmentations.transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), 
                                                max_pixel_value=255.0, p=1.0),
                            A.pytorch.transforms.ToTensorV2(transpose_mask=False, p=1.0) ]
                            )
def read(img):return cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
fid = '730394.jpg'
img = read(fid)


model,device = load()
img_normalized = a_test_transform(image=img)['image'].float()
img_normalized = img_normalized.unsqueeze_(0)
   # input = Variable(image_tensor)
img_normalized = img_normalized.to(device)
   # print(img_normalized.shape)
with torch.no_grad():
    model.eval()  
    output = model(img_normalized)
    sm = torch.nn.Softmax(dim=1)
    print(sm(output))

