import os

img_path = "/home/sanjay/DATA/Dataset/meter_with_label/mechanical_meter/xml/"
xml_path = "/home/sanjay/DATA/Dataset/meter_with_label/mechanical_meter/new_img/"

for xml_file in os.listdir(xml_path):
    xml_name = os.path.splitext(xml_file)[0]
    flag = False
    for img_file in os.listdir(img_path):
        img_name = os.path.splitext(img_file)[0]
        if xml_name == img_name:
            flag = True
            break
    if flag == False:
        print(xml_name)
        os.remove(os.path.join(xml_path, xml_file))
        print("Deleted " + xml_file)
    flag = False