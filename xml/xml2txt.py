import xml.etree.ElementTree as et
import os
import shutil

SHIP_CLASSES = ('ore carrier', 'bulk cargo carrier', 'general cargo ship', 'container ship', 'fishing boat',
                'passenger ship')


def parse_rec(filename):
    tree = et.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        # difficult = int(obj.find('difficult').text)
        # if difficult == 1:
        #     continue
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)

    return objects


training_file = os.listdir("Seaships\\JPEGImages")
file_name_list = []
for i in training_file:
    file_name_list.append(i.split('.')[0])

Annotations = 'Seaships\\Annotations/'
xml_files = os.listdir(Annotations)

count = 0
for xml_file in xml_files:
    count += 1
    file_number = xml_file.split('.')[0]
    if file_number not in file_name_list:
        print(xml_file.split('.')[0]+'照片不存在')
        continue

    results = parse_rec(Annotations + xml_file)
    if len(results) == 0:
        print(xml_file)
        continue
    class_name_gather = []
    for res in results:
        class_name_gather.append(res['name'])
    if 'ore carrier' in class_name_gather:
        text_name = xml_file.split('.')[0] + '.txt'
        txt_file = open('Seaships\\labels_ore_carrier\\' + text_name, 'w')
        image_path = xml_file.split('.')[0] + '.jpg'
        oldname = 'Seaships\\JPEGImages\\' + file_number + '.jpg'
        newname = 'Seaships\\JPEGImages_ore\\' + file_number + '.jpg'
        shutil.copyfile(oldname, newname)
    else:
        continue

    for result in results:
        class_name = result['name']
        bbox = result['bbox']
        class_name = SHIP_CLASSES.index(class_name)
        x_center = (bbox[2] + bbox[0]) / (2 * 1920)
        y_center = (bbox[3] + bbox[1]) / (2 * 1080)
        width = (bbox[2] - bbox[0]) / 1920
        height = (bbox[3] - bbox[1]) / 1080
        txt_file.write(str(class_name)+' '+str(x_center)[0:8].ljust(8,'0')+' '+str(y_center)[0:8].ljust(8,'0')+' '+str(width)[0:8].ljust(8,'0')+' '+str(height)[0:8].ljust(8,'0'))
        txt_file.write('\n')
    txt_file.close()

print('共解析'+str(count)+'个XML文件')