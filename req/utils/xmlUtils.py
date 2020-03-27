#!/usr/bin/python
# -*- coding=utf-8 -*-
# author : wanghao
# date: 2018-09-30
# version: 0.1

from xml.etree.ElementTree import ElementTree, Element


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    root = tree.getroot()
    prettyXml(root, '\t', '\n')
    # ElementTree.dump(tree)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def prettyXml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if len(element):  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
       node: 节点
       kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# ---------------search -----

def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
       nodelist: 节点列表
       kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# ---------------change -----

def change_node_properties(nodelist, kv_map, is_delete=False):
    '''修改/增加 /删除 节点的属性及属性值
       nodelist: 节点列表
       kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    '''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    '''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


if __name__ == "__main__":
    # 1. 读取xml文件
    tree = read_xml(r"C:\Users\ws\Desktop\11.xml")

    # 2. 属性修改
    # A. 找到父节点
    nodes = find_nodes(tree, ".//TransInfo/MergeVideoFileName")
    print nodes
    for node in nodes:
        print node.text
        print "1" + "/" + node.text.split("/")[-1]
        node.text = "1" + "/" + node.text.split("/")[-1]
    # B. 通过属性准确定位子节点
    # result_nodes = get_node_by_keyvalue(nodes, {"key": "kVideoFilter_Param_0"})
    # print result_nodes[0].get("type")
    # print result_nodes
    # # C. 修改节点属性
    # change_node_properties(result_nodes, {"direction": "111"})
    # # D. 删除节点属性
    # change_node_properties(result_nodes, {"direction": "E"}, True)
    #
    # # 3. 节点修改
    # # A.新建节点
    # a = create_node("person", {"age": "15", "money": "200000"}, "this is the firest content")
    # # B.插入到父节点之下
    # add_child_node(result_nodes, a)
    #
    # # 4. 删除节点
    # # 定位父节点
    # del_parent_nodes = find_nodes(tree, ".//country")
    # # 准确定位子节点并删除之
    # target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "neighbor", {"name": "Austria"})
    #
    # # 5. 修改节点文本
    # # 定位节点
    # text_nodes = get_node_by_keyvalue(nodes, {"name": "Austria"})
    # change_node_text(text_nodes, "new text")
    #
    # # 6. 输出到结果文件
    # tree = read_xml(r"C:\Users\ws\Desktop\res\2_Orb_1\Data\data.xml")
    write_xml(tree, r"C:\Users\ws\Desktop\11.xml")
