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
  
  3.运行Muti_Labels.py :  
  ![Label Tool](https://github.com/sheirving/VOCdata_Make_project/blob/master/Images/2.JPG)  
  * 先点击当前类别，如suv,sedan等，此步骤一定要在绘制包围盒之前进行。  
  * 在图片上绘制框（点击两次，不要拖拽），右方列表可见类别及位置坐标。选定坐标按下Delete按钮可删除该坐标。按下ClearAll可清除全部坐标。  
  * 绘制完成后点击save,保存当前坐标。  
  * 点击prev或next按钮进行其他图片的处理。（点击同时具有保存效果）  
  * "Go" 可输入指定编号进行跳转。    
  
  4.生成VOC格式的XML文件：  
  * 运行TXt_To_XML.py
