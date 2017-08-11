# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:04:03 2017

@author: She
"""
from __future__ import division
from tkinter import *
#import Tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import glob
import random
import numpy as np

# colors for the bboxes
COLORS = ['red', 'blue', 'yellow', 'green', 'black','pink']
# image sizes for the examples
SIZE = 256, 256

IMAGEPATH = 'JPEGImages'
LABELPATH = 'Labels'

#classLabels=['Sedan','Van','SUV','Wagons','Motorcycle','Audi','BenTian','BYD','BenZ','BUick','DaZhong','Toyota',
            # 'LingMu','XianDai','YiQi','black','white','red','blue']
CarTypeLabels=['Sedan','Van','SUV','Wagons','Motorcycle']
BrandLabels=['Audi','BenTian','BYD','BenZ','BUick','DaZhong','Toyota','LingMu','XianDai','YiQi']
Plate_Color_Labels=['plate','black','white','red','blue']


class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("LabelTool")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = False, height = False)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None
        self.currentClass = ''

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir: Annotations")
        self.label.grid(row = 0, column = 0, columnspan = 2, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = W+E)



        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Esc> to cancel current bbox
        self.mainPanel.grid(row = 1, column = 0, rowspan = 4, columnspan = 2, sticky = W+N)



        #self.scrl = Scrollbar(self.frame, orient=HORIZONTAL)
        #self.scrl.pack(side=RIGHT, fill=Y)
        #self.mainPanel.configure(yscrollcommand = self.scrl.set)
        #self.mainPanel.pack(side=LEFT, expand=True, fill=BOTH)
        #self.scrl['command'] = self.mainPanel.yview
		
        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 1, column = 2,  sticky = W+N)

        self.listbox = Listbox(self.frame, width = 28, height = 10)
        self.listbox.grid(row = 2, column = 2, sticky = N)

        self.btnDel = Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, sticky = W+E+N)

        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = W+E+N)

        self.save = Button(self.frame, text = "save", command = self.saveImage)
        self.save.grid(row = 5, column = 2, sticky = W+E+N)
        
        #select class type
        self.classPanel = Frame(self.frame)
        self.classPanel.grid(row = 5, column = 0,rowspan=3,columnspan = 5, sticky = W+N+S)
        label = Label(self.classPanel, text = 'class:')
        label.grid(row = 5, column = 0,  sticky = W+N+S)
        
        label_1= Label(self.classPanel,text='Type:')
        label_1.grid(row = 6,column = 0, sticky = W+N+S) 
        
        label_2= Label(self.classPanel,text='Plate_Color:')
        label_2.grid(row = 7,column = 0, sticky = W+N+S) 
        
        label_3= Label(self.classPanel,text='Brand:')
        label_3.grid(row = 8,column = 0, sticky = W+N+S) 
        self.classbox = Listbox(self.classPanel,  width = 14, height = 1)
        self.classbox.grid(row = 5,column = 1)
#        for each in range(len(classLabels)):
#            function = 'select' + classLabels[each]
#            print (classLabels[each])
#            btnMat = Button(self.classPanel, text = classLabels[each], command = getattr(self, function))
#            btnMat.grid(row = 5, column = each + 3)
        #%%
        # https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda
       
        #global each1
        #global each2
        #global each3
        
        for each1 in range(len(CarTypeLabels)): 
            print (CarTypeLabels[each1])
            btnMat = Button(self.classPanel, text = CarTypeLabels[each1], command =lambda each1=each1 : self.select_TypeClass(each1))
            btnMat.grid(row = 6, column = each1+1,sticky = W+N+E)
        
        for each2 in range(len(Plate_Color_Labels)):
            print(Plate_Color_Labels[each2])
            btnMat = Button(self.classPanel, text = Plate_Color_Labels[each2], command = lambda each2=each2 : self.select_Plate_ColorClass(each2))
            btnMat.grid(row = 7, column = each2+1,sticky = W+N+E)
        
        for each3 in range(len(BrandLabels)):
            print(BrandLabels[each3])
            btnMat = Button(self.classPanel, text = BrandLabels[each3], command = lambda each3 = each3 : self.select_BrandClass(each3))
            btnMat.grid(row = 8, column = each3+1,sticky = W+N+E)
        
            
        
        
        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 9, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(10, weight = 1)

    def loadDir(self, dbg = False):
        if not dbg:
            self.parent.focus()
        
        # get image list
        self.imageDir = os.path.join('.', IMAGEPATH) #图片根路径
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg')) #获取图片列表
        
        if len(self.imageList) == 0:
            print ('No .JPEG images found in the specified dir!')
            return

      # set up output dir
        self.outDir = os.path.join('.', 'Labels') #label输出路径
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        
        labeledPicList = glob.glob(os.path.join(LABELPATH, '*.txt')) #获取已存在的label
        
        for label in labeledPicList:
            data = open(label, 'r')
            if '0\n' == data.read():
                data.close()
                continue
            data.close()
            
        # default to the 1st image in the collection
        
        self.cur = 0
        self.total = len(self.imageList)

        print ('%d images loaded from %s' %(self.total, IMAGEPATH))
        self.loadImage()

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur] #图片路径
        self.img = Image.open(imagepath) #图片文件
        self.imgSize = self.img.size 
        
        self.tkimg = ImageTk.PhotoImage(self.img) #加载图片
        #self.mainPanel.config(width = self.tkimg.width(), height = self.tkimg.height()) #修改画布尺寸
        self.mainPanel.config(width = self.tkimg.width(), height = self.tkimg.height())
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW) #填充画布
        self.progLabel.config(text = "%04d/%04d" %(self.cur + 1, self.total)) #修改进度值

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0] #图片名 （去后缀）
        labelname = self.imagename + '.txt' #标签名
        self.labelfilename = os.path.join(LABELPATH, labelname) #完整标签相对路径
        bbox_cnt = 0
        if os.path.exists(self.labelfilename): #如果已存在标签
            with open(self.labelfilename) as f: #打开标签文件
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int(line.strip()) #获取标签数量
                        continue

                    tmp = [(t) for t in line.split()] #获取当前标签坐标
                	
                    self.bboxList.append(tuple(tmp)) #记录坐标列表
                    #绘制矩形框
                    tmpId = self.mainPanel.create_rectangle(int(tmp[1]), int(tmp[2]), \
                                                            int(tmp[3]), int(tmp[4]), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '%s: (%d, %d) -> (%d, %d)' %(tmp[0], int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4])))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print ('Image No. %d saved' %(self.cur))


    def mouseClick(self, event):
        if self.STATE['click'] == 0: #第一次点击
            self.STATE['x'], self.STATE['y'] = event.x, event.y
            #self.STATE['x'], self.STATE['y'] = self.imgSize[0], self.imgSize[1]
        else: #第二次点击
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            #越界判断
            if x2 > self.imgSize[0]:
                x2 = self.imgSize[0]
            if y2 > self.imgSize[1]:
                y2 = self.imgSize[1]
            self.bboxList.append((self.currentClass, x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '%s: (%d, %d) -> (%d, %d)' %(self.currentClass, x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []
    #%%
    def select_TypeClass(self,each1):
        self.currentClass=CarTypeLabels[each1]
        self.classbox.delete(0,END)
        self.classbox.insert(0,CarTypeLabels[each1])
        self.classbox.itemconfig(0,fg=COLORS[0])
     
    def select_Plate_ColorClass(self,each2):
        self.currentClass=Plate_Color_Labels[each2]
        self.classbox.delete(0,END)
        self.classbox.insert(0,Plate_Color_Labels[each2])
        self.classbox.itemconfig(0,fg=COLORS[0])
        
    def select_BrandClass(self,each3):
        self.currentClass=BrandLabels[each3]
        self.classbox.delete(0,END)
        self.classbox.insert(0,BrandLabels[each3])
        self.classbox.itemconfig(0,fg=COLORS[0])
    
#    def selectSedan(self):
#        self.currentClass = 'Sedan'
#        self.classbox.delete(0,END)
#        self.classbox.insert(0, 'Sedan')
#        self.classbox.itemconfig(0,fg = COLORS[0])
#        
#    def selectplate(self):
#        self.currentClass = 'plate'
#        self.classbox.delete(0,END)
#        self.classbox.insert(0, 'plate')
#        self.classbox.itemconfig(0,fg = COLORS[0])
#
#    def selectbentian(self):
#        self.currentClass = 'bentian'
#        self.classbox.delete(0,END)
#        self.classbox.insert(0, 'bentian')
#        self.classbox.itemconfig(0,fg = COLORS[0])
#
#    def selectbenchi(self):
#        self.currentClass = 'benchi'
#        self.classbox.delete(0,END)
#        self.classbox.insert(0, 'benchi')
#        self.classbox.itemconfig(0,fg = COLORS[0])
     
    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 0:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx - 1
            self.loadImage()

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
root.mainloop()
