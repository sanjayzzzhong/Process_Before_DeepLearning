import os
import xml.dom.minidom

read_file = '/Users/sanjay/Downloads/test_data/all/'

for file_name in os.listdir(read_file):
    new_txtname = file_name.split('.')[0]

    # 创建一个空的Dom文档对象
    doc = xml.dom.minidom.Document()
    # 创建根节点，此根节点为annotation
    annotation = doc.createElement('annotation')
    # 将根节点添加到DOm文档对象中
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    # 内容写入
    folder_text = doc.createTextNode('ee')
    folder.appendChild(folder_text)
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    filename_text = doc.createTextNode(file_name)
    filename.appendChild(filename_text)
    annotation.appendChild(filename)

    path = doc.createElement('path')
    path_text = doc.createTextNode('path is null')
    path.appendChild(path_text)
    annotation.appendChild(path)

    source = doc.createElement('source')
    databass = doc.createElement('databass')
    databass_text = doc.createTextNode('Unknown')
    source.appendChild(databass)
    databass.appendChild(databass_text)
    annotation.appendChild(source)

    size = doc.createElement('size')
    width = doc.createElement('width')
    width_text = doc.createTextNode('875')
    height = doc.createElement('height')

    height_text = doc.createTextNode('656')
    depth = doc.createElement('depth')
    depth_text = doc.createTextNode('1')
    size.appendChild(width)
    width.appendChild(width_text)
    size.appendChild(height)
    height.appendChild(height_text)
    size.appendChild(depth)
    depth.appendChild(depth_text)
    annotation.appendChild(size)

    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    annotation.appendChild(segmented)

    # 写入xml文本文件中
    fp = open('/Users/sanjay/Downloads/test_data/xml/%s.xml' % new_txtname, 'w+')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
    fp.close()
