import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup

import torchvision
from torchvision import transforms,datasets,models
import torch
from torch.utils.data import Dataset, DataLoader
#引入预训练模型
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
import matplotlib.patches as patches
import os 

#在 xml 中读取bbox
def generate_box(obj):
    xmin = int(obj.find('xmin').text)
    ymin = int(obj.find('ymin').text)
    xmax = int(obj.find('xmax').text)
    ymax = int(obj.find('ymax').text)
    return [xmin,ymin,xmax,ymax]

#在xml 读取label 二分类，为person
def generate_person_label(obj):
    #person 返回1 不是返回0
    return obj.find('name').text =='person'

def generate_target(image_id,file):
    with open(file,'r',encoding='utf-8') as f :
        data = f.read()
        soup  = BeautifulSoup(data,'lxml-xml')
        objs = soup.find_all('object')
        nums_objs = len(objs)
        boxes = []
        labels = []
        for i in objs:
            boxes.append(generate_box(i))
            labels.append(generate_person_label(i))
        #make data
        boxes = torch.as_tensor(boxes,dtype=torch.float32)
        labels = torch.as_tensor(labels,dtype=torch.int64)
        img_id = torch.tensor([image_id])
        target = {}
        target['boxes'] = boxes
        target['labels'] = labels
        target['image_id'] = img_id
        return target


#因为不对等 所以要把图片名字和xml文件名字对应起来
# labels = [img[:-4]+'.xml' for img in imgs]
labels = list(sorted(os.listdir('D:\\ML_data_sql\\human_detect\\annotations\\')))
imgs = [label[:-4]+'.jpg' for label in labels]
#使用一部分数据（0.2倍）
use_labels = labels[:int(len(labels)*0.2)]
use_imgs = imgs[:int(len(imgs)*0.2)]
test_imgs = imgs[int(len(imgs)*0.2):int(len(imgs)*0.21)]
test_labels = labels[int(len(labels)*0.2):int(len(labels)*0.21)]
# print(len(labels))
# print(len(imgs))
# print(imgs[0],labels[0])
#make dataset
class PersonDataset(object):
    def __init__(self,transforms,imgs,labels):
        self.transforms = transforms
        self.imgs = imgs
        self.labels = labels
        self.lens = len(imgs)
    
    def __getitem__(self,idx):
        #load images and masks
        img = Image.open('D:\\ML_data_sql\\human_detect\\JPEGImages\\'+self.imgs[idx])
        #label = generate_target(idx,'D:\\ML_data_sql\\human_detect\\annotations\\'+self.labels[idx])
        target = generate_target(idx,'D:\\ML_data_sql\\human_detect\\annotations\\'+self.labels[idx])
        #apply transforms
        if self.transforms is not None:
            img = self.transforms(img)
        return img,target
    
    def __len__(self):
        return len(self.imgs)

data_transform = transforms.Compose([
        transforms.ToTensor(), 
    ])   

from torch.utils.data.dataset import random_split
dataset = PersonDataset(data_transform,use_imgs,use_labels)
test_dataset =PersonDataset(data_transform,test_imgs,test_labels)
#因为dataset 有点大 爆显存 所以使用少量来训练
def collate_fn(batch):
    return tuple(zip(*batch))
traindata_loader = torch.utils.data.DataLoader(dataset, batch_size=4,collate_fn=collate_fn)
testdata_loader = torch.utils.data.DataLoader(test_dataset, batch_size=4,collate_fn=collate_fn)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
#test
def get_model_instance_segmentation(num_classes):
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model
#load the model
model = get_model_instance_segmentation(2)

plt_imgs = []
plt_pred = []
model.load_state_dict(torch.load('D:\\Machine_Learning_note\\CV\\model_final.pth'))
model.eval()
model.to(device)
for imgs, annotations in testdata_loader:
        imgs = list(img.to(device) for img in imgs)
        annotations = [{k: v.to(device) for k, v in t.items()} for t in annotations]
        plt_imgs.append(imgs)
        


pred = model(imgs)

def plot_img_bbox(img, target):
    fig, a = plt.subplots(1, 1)
    fig.set_size_inches(5, 5)
    a.imshow(img.T)
    for box in (target['boxes']):
        x, y, width, height = box[0], box[1], box[2] - box[0], box[3] - box[1]
        rect = patches.Rectangle((x, y),
                                 width, height,
                                 linewidth=2,
                                 edgecolor='white',
                                 facecolor='none')
        #rect.detach().numpy()
        a.add_patch(rect)
    plt.show()

def plot_image(img_tensor):
    fig,ax = plt.subplots(1)
    img = img_tensor.cpu().data
    # Display the image
    ax.imshow(img.permute(1, 2, 0))
    for box in pred["boxes"]:
        xmin=[]
        ymin=[]
        xmax=[]
        ymax=[]
        xmin.append(box[0])
        ymin.append(box[1])
        xmax.append(box[2])
        ymax.append(box[3])
        #xmin, ymin, xmax, ymax = [427.7730, 534.9896, 638.9386, 720.0000]
        # Create a Rectangle patch
    for i in range(len(xmin)):
        rect = patches.Rectangle((xmin[i], ymin[i]),
                                 xmax[i] - xmin[i],
                                 ymax[i] - ymin[i],
                                 linewidth=2,
                                 edgecolor='r',
                                 facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
    plt.show()
plot_image(imgs[0].cpu())
