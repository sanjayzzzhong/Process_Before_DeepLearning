from PIL import Image     
import os       
path = '/home/sanjay/DATA/ChromeDownload/WeaponS/img/' #图片目录 
for file in os.listdir(path):      
     extension = file.split('.')[-1]
     if extension == 'jpg' or extension == 'png':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB':
                 os.remove(fileLoc)
                 print(file+', '+img.mode)