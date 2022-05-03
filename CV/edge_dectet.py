import cv2
import numpy as np

img =cv2.imread('Cameraman.tif', cv2.IMREAD_COLOR)
#由于原图过大，所以需要缩小图片
#img =cv2.resize(img,(400,400))
cv2.imshow('image', img)
def sobel(image):
    x= cv2.Sobel(image, cv2.CV_8U, 1, 0)    #8位无符号整型
    y= cv2.Sobel(image, cv2.CV_8U, 0, 1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return absX,absY,dst

def Laplace(image):
    dst = cv2.Laplacian(image, cv2.CV_8U)
    result =cv2.convertScaleAbs(dst)
    return result

def Simple_Canny(image):
    canny_img = cv2.Canny(image, 100, 200)
    return canny_img

def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(img,(3,3),0)
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
    cv2.imshow('change threshold',dst)

lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3
cv2.namedWindow('change threshold')
cv2.createTrackbar('Min threshold','change threshold',lowThreshold, max_lowThreshold, CannyThreshold)

sx_img,sy_img,sobel_img = sobel(img)
laplace_img = Laplace(img)
simple_canny_img = Simple_Canny(img)
# Gauss_Canny(img,0,3)

#可以进行3通道的sobel 边缘检测
cv2.imshow('sobel_all', sobel_img)
cv2.imshow('sobel_x', sx_img)
cv2.imshow('sobel_y', sy_img)
#laplace change
cv2.imshow('laplace_img', laplace_img)
cv2.imshow('simple_canny_img', simple_canny_img)
# cv2.imshow('gauss_img', gauss_img)
# cv2.imshow('canny_img', canny_img)

cv2.waitKey(0)
cv2.destroyAllWindows()

