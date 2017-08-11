# VOCdata_Make_project
##制作VOC格式的数据集
1. 环境：(Anaconda)
    python3.6 
    opencv 3.2.0
2.创建目录结构：  
--某盘某目录（D:/project/VOC_make_project）  
  |  
  --Annotations # 用于保存xml文件  
  |  
  --JPEGImages  # 原始卡口数据预处理后存放处
  |  
  --Labels      # 生成的txt存放处  
  |  
  --Kakou_cars  #原始的卡口图像数据  
  |  
  --Batche_rename.py # 原始卡口数据批量预处理  
  |  
  --Muti_labels.py   # 对JPEGImages卡口图像进行标签  
  |  
  --Txt_To_XML  #Labels中TXT文件转XML，并存放于Annotations  
  |  
  --Set_create.py # 生成ImageSets文件夹中的train、trainval、val的txt  

  ![](https://github.com/sheirving/VOCdata_Make_project/blob/master/Images/1.PNG)  
  
  3.
  ![Label Tool](https://github.com/sheirving/VOCdata_Make_project/blob/master/Images/2.JPG)
