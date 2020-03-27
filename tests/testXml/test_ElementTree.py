# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

tree = ET.parse('sample.xml')
root = tree.getroot()

# for child in root:
#     print child.tag, child.attrib
#
#
# for neighbor in root.iter('year'):
#     print neighbor.text

print root.find(".//*[@name='Singapore']/rank").text
for country in root.findall('country'):
    if country.attrib['name'] == 'Singapore':
        year = country.find('year')  # 使用Element.find()
        print year
        del year.attrib["name"]
        print year.text
tree.write('test2.xml')  # 保存
# for country in root.findall('country'):
#     if country.attrib['name'] == 'Singapore':
#         years = country.findall('year')  # 使用Element.findall()
#         print years
#         print years[0].text  # 注意和上段的区别

# for country in root.findall('country'):
#     if country.attrib['name'] == 'Singapore':
#         year = country.find('year')
#         year.text = "2019"
#         print(year.text)
# tree.write('test.xml')  # 保存

# for country in root.findall('country'):
#     if country.attrib['name'] == 'Singapore':
#         year = country.find('year')
#         country.remove(year)
# tree.write('test.xml')  # 保存

# for country in root.findall('country'):
#     if country.attrib['name'] == 'Singapore':
#         element = Element("year")
#         element.text = "2020"
#         country.append(element)
# tree.write('test2.xml')  # 保存


# def prettyXml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
#     if len(element):  # 判断element是否有子元素
#         if element.text == None or element.text.isspace():  # 如果element的text没有内容
#             element.text = newline + indent * (level + 1)
#         else:
#             element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
#             # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
#         # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
#     temp = list(element)  # 将elemnt转成list
#     for subelement in temp:
#         if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
#             subelement.tail = newline + indent * (level + 1)
#         else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
#             subelement.tail = newline + indent * level
#         prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作
#
#
#
# tree = ElementTree.parse(r'E:\work\python\UI-Project\tests\testXml\xml\test2.xml')  # 解析test.xml这个文件，该文件内容如上文
# root = tree.getroot()  # 得到根元素，Element类
# prettyXml(root, '\t', '\n')  # 执行美化方法
# # ElementTree.dump(root)  # 显示出美化后的XML内容
# tree.write(r'E:\work\python\UI-Project\tests\testXml\xml\test3.xml')
