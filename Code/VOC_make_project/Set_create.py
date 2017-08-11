# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:58:33 2017

@author: She
"""

import os
import glob

imageDir = os.path.join('.', 'JPEGImages')
imageList = glob.glob(os.path.join(imageDir, '*.jpg'))
imageSetDir = os.path.join('.', 'ImageSets')
MainDir = os.path.join(imageSetDir, 'Main')
print (len(imageList))
if len(imageList) != 0:
	if not os.path.exists(imageSetDir):
		os.mkdir(imageSetDir)
	if not os.path.exists(MainDir):
		os.mkdir(MainDir)
	f_test = open(os.path.join(MainDir, 'test.txt'), 'w')
	f_train = open(os.path.join(MainDir, 'train.txt'), 'w')
	f_val = open(os.path.join(MainDir, 'val.txt'), 'w')
	f_trainval = open(os.path.join(MainDir, 'trainval.txt'), 'w')
	i = 0
	j = 0
	len_split = len(imageList) / 2
	len_tv = len_split / 2
	for image in imageList:
		imagename = os.path.split(image)[-1].split('.')[0]
		if i < len_split:
			f_test.write(imagename + '\n')
			i += 1
		else:
			if j < len_tv:
				f_train.write(imagename + '\n')
			else:
				f_val.write(imagename + '\n')
			f_trainval.write(imagename + '\n')
			j += 1
		#print imagename
	f_test.close()
	f_train.close()
	f_val.close()
f_trainval.close()