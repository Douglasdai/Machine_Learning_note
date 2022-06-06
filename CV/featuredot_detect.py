import math
from shutil import register_unpack_format
import cv2
from cv2 import sort
import matplotlib.pyplot as plt
import numpy as np
import copy

img1 = cv2.imread('scene_l.bmp', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('scene_r.bmp', cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread('scene_r.bmp', cv2.IMREAD_GRAYSCALE)
def SIFT(img1,img2,feature_num):
    '''
    @param img: 输入图像
    @param feature_num: 希望特征点数量
    '''
    # 初始化SIFT算法
    #SIFT_create 参数 nfeatures 可以设置特征点的数量(保留效果最好的特征点数量,进行匹配)
    #SIFT_create 参数 nOctaveLayers 设置金字塔层数
    #SIFT_create 参数 contrastThreshold 设置阈值
    #SIFT_create 参数 edgeThreshold 设置边缘阈值
    #SIFT_create 参数 sigma 设置高斯核的标准差
    sift = cv2.SIFT_create(nfeatures=feature_num)
    #寻找关键点和描述子
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)
    #找到关键点的数量  希望为50以下 这样比较直观
    #print(len(keypoints))
    bf = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE)
    #匹配
    matches = bf.match(descriptors1,descriptors2)
    #画出关键点
    #sift_img = cv2.drawKeypoints(img, keypoints, None, (255, 0, 0), 4)
    #绘制
    matches = sorted(matches,key = lambda x: x.distance)
    result =cv2.drawMatches(img1,keypoints1,img2,keypoints2,matches[:feature_num],None)
    cv2.imshow('match',result)

    

def Harris(img1):
    #计算harris 矩阵 参数:输入图像，角点检测邻域的大小，sobel导数的孔径，harris检测器中的自由参数，返回值
    dst = cv2.cornerHarris(img1,2,3,0.04)
    #扩大标记的内容
    dst = cv2.dilate(dst,None)
    harris_img = copy.deepcopy(img1)
    harris_img[dst>0.01*dst.max()]=255
    cv2.imshow('harris_img ', harris_img)
SIFT(img1,img2,50)
Harris(img1)
cv2.waitKey(0)
cv2.destroyAllWindows()