# -*- coding: utf-8 -*-

"""
Created on Mon Jul 31 20:56:06 2017

@author: She
"""

import os 
from PIL import Image
import numpy as np


#origin_images = 'D:\Project\Conda\Car_data\image'
origin_images = 'D:\Project\Conda\VOC_Mkae_Project\Kakou_cars'
name_number = 0
name_length = 6

if not os.path.exists('JPEGImages'):
    os.mkdir('JPEGImages')
    print('mkdir done')

files_list = os.listdir(origin_images)
imgs_list = []
for name in files_list:
    if name.endswith('.jpg'):
        imgs_list.append(name)
total_name = len(imgs_list)
for num in imgs_list:
    new_name_str = (name_length - len(str(name_number)))*'0'+str(name_number)+'.jpg'
    image = Image.open(os.path.join(origin_images,num))
    img_size = list(image.size) #tuple转为list,因为image.size为tuple型
    ratio = 800/img_size[0]
    imgResize_h = int(np.round(ratio*img_size[1]))
    imgResize_w = 800
    Resize_image = image.resize(tuple([imgResize_w,imgResize_h]))
    Resize_image.save(os.path.join('JPEGImages',new_name_str),'JPEG')
    name_number=name_number+1
    
#for name in files_list:
#    new_name_str =  (name_length - len(str(name_number)))*'0'+str(name_number)+'.jpg'
#    src = os.path.join(os.path.abspath(origin_images),name)
#    dst = os.path.join(os.path.abspath(origin_images),new_name_str)
#    os.rename(src,dst)
#    print ('converting %s to %s ...' % (src, dst))
#    name_number=name_number+1
print ('total %d to rename & converted %d jpeg' % (total_name, name_number))

#%%
'''
另外一种写法
'''
#%%
from __future__ import division
import os
import glob
import numpy as np
from PIL import Image

origin_images = 'D:\Project\Conda\VOC_Mkae_Project\Kakou_cars'
name_number = 0
name_length = 6

if not os.path.exists('JPEGImages'):
    os.mkdir('JPEGImages')
    print('mkdir done')

imgs_list = glob.glob(os.path.join(origin_images,'*.jpg'))
total_imgs = len(imgs_list)
for num in imgs_list:
    global name_number
    new_name_str = (name_length-len(str(name_number)))*'0'+str(name_number)+'.jpg'
    image = Image.open(num)
    img_size = list(image.size) #tuple转为list,因为image.size为tuple型
    ratio = 800/img_size[0]
    imgResize_h = int(np.round(ratio*img_size[1]))
    imgResize_w = 800
    Resize_image = image.resize(tuple([imgResize_w,imgResize_h]))
    Resize_image.save(os.path.join('JPEGImages',new_name_str),'JPEG')
    name_number = name_number+1

print ('total %d to rename & converted %d jpeg' % (total_imgs, name_number))