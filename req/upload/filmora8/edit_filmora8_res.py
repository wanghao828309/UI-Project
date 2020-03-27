#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2018/12/3 13:53

from req.utils import xmlUtils
from req.utils.FileParserUtil import MyFileParserUtil
from req.utils.FileParserUtil import del_headerr
from req.utils.mysqldbUtil import MysqldbHelper
import sys, time

reload(sys)
sys.setdefaultencoding('utf-8')

# ---------------------------------------------------------------------
# 编辑xml
# ---------------------------------------------------------------------
PNG_NAME = []


def read(in_path):
    return xmlUtils.read_xml(in_path)


def edit_temp(tree, resName, type):
    if type.lower() == "transitions":
        # 修改MergeVideoFileName节点
        mergeVideoFileName_nodes = xmlUtils.find_nodes(tree, ".//TransInfo/MergeVideoFileName")
        for node in mergeVideoFileName_nodes:
            node.text = resName + "/" + node.text.split("/")[-1]
        # 修改ResourceTag节点
        resourceTag_nodes = xmlUtils.find_nodes(tree, ".//TransInfo/ResourceTag")
        xmlUtils.change_node_text(resourceTag_nodes, resName)
        # 修改ThumbFileName节点
        thumbFileName_nodes = xmlUtils.find_nodes(tree, ".//TransInfo/ThumbFileName")
        for node in thumbFileName_nodes:
            node.text = resName + "/" + node.text.split("/")[-1]

    if type.lower() == "effect":
        # 修改MergeVideoFileName节点
        mergeVideoFileName_nodes = xmlUtils.find_nodes(tree, ".//EffectInfo/MergeVideoFileName")
        for node in mergeVideoFileName_nodes:
            node.text = resName + "/" + node.text.split("/")[-1]
        # 修改ResourceTag节点
        resourceTag_nodes = xmlUtils.find_nodes(tree, ".//EffectInfo/ResourceTag")
        xmlUtils.change_node_text(resourceTag_nodes, resName)

    if type.lower() == "contents":
        # 修改File节点text
        file_nodes = xmlUtils.find_nodes(tree, ".//File")
        for node in file_nodes:
            node.text = resName + "\\" + node.text.split("\\")[-1]
        # 修改File节点的Tag属性的值
        xmlUtils.change_node_properties(file_nodes, {"Tag": resName})


def edit_ResourceType(tree):
    nodes = xmlUtils.find_nodes(tree, ".//CaptionArray/CaptionResource/ResourceType")
    xmlUtils.change_node_text(nodes, "0")


def edit_ResourceTag(tree, resName):
    nodes = xmlUtils.find_nodes(tree, ".//CaptionArray/CaptionResource/ResourceTag")
    xmlUtils.change_node_text(nodes, resName)


def edit_Opener_BackVideo(tree):
    nodes_Alias = xmlUtils.find_nodes(tree, ".//CaptionArray/CaptionResource/Alias")
    nodes_TemplateStyle = xmlUtils.find_nodes(tree, ".//CaptionArray/CaptionResource/TemplateStyle")
    nodes_BackVideo = xmlUtils.find_nodes(tree, ".//CaptionArray/CaptionResource/BackVideo")
    for node_tuple in zip(nodes_Alias, nodes_TemplateStyle, nodes_BackVideo):
        alias = node_tuple[0].text
        if "Opener" in alias:
            # print alias
            node_tuple[1].text = "3"
            node_tuple[2].text = "$CaptionPath$" + alias + ".mp4"


def edit_Texture(tree, resName):
    nodes_Texture_Enable = xmlUtils.find_nodes(tree,
                                               ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/TextParam/Texture/Enable")
    nodes_Texture_TextureImagePath = xmlUtils.find_nodes(tree,
                                                         ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/TextParam/Texture/TextureImagePath")
    nodes_Texture_TextureTempImagePath = xmlUtils.find_nodes(tree,
                                                             ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/TextParam/Texture/TextureTempImagePath")
    for node_tuple in zip(nodes_Texture_Enable, nodes_Texture_TextureImagePath, nodes_Texture_TextureTempImagePath):
        # print node_tuple
        if node_tuple[0].text == "1":
            textureImagePath = node_tuple[1].text
            pngName = textureImagePath.split("\\")[-1]
            # print pngName
            PNG_NAME.append(pngName)
            new_textureImagePath = "$CaptionPath$" + resName + "/" + pngName
            node_tuple[1].text = new_textureImagePath
            node_tuple[2].text = ""


def edit_VideoParam(tree, resName):
    nodes_VideoParam = xmlUtils.find_nodes(tree,
                                           ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/VideoParam")
    # print nodes_VideoParam
    if len(nodes_VideoParam) > 0:
        nodes_VideoPath = xmlUtils.find_nodes(tree,
                                              ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/VideoParam/VideoPath")
        nodes_VideoDataPath = xmlUtils.find_nodes(tree,
                                                  ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/VideoParam/VideoDataPath")
        nodes_ImagePath = xmlUtils.find_nodes(tree,
                                              ".//CaptionArray/CaptionResource/NLETitleArray/NLETitleItem/VideoParam/ImagePath")
        for node_tuple in zip(nodes_VideoPath, nodes_VideoDataPath, nodes_ImagePath):
            videoPath = node_tuple[0].text
            # print videoPath
            videoDataPath = node_tuple[1].text
            imagePath = node_tuple[2].text
            new_videoPath = "$CaptionPath$" + resName + "/" + videoPath.split("/")[-1]
            new_videoDataPath = "$CaptionPath$" + resName + "/" + videoDataPath.split("/")[-1]
            new_imagePath = "$CaptionPath$" + resName + "/" + imagePath.split("/")[-1]
            node_tuple[0].text = new_videoPath
            node_tuple[1].text = new_videoDataPath
            node_tuple[2].text = new_imagePath


# ---------------------------------------------------------------------
# 编辑ini
# ---------------------------------------------------------------------


# 清空文件
def modify_file(path):
    with open(path, "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()  # 清空文件


# 复制文件
def copyOneFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!" % (srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print "copy %s -> %s" % (srcfile, dstfile)


def copyDir(sourceSrcDir, dstSrcDir):
    if os.path.exists(dstSrcDir):
        print dstSrcDir, '存在先删除'
        shutil.rmtree(dstSrcDir)

    print '拷贝代码文件夹开始...'
    shutil.copytree(sourceSrcDir, dstSrcDir)
    print '拷贝代码文件夹结束！\n'


def edit_ini(path, res, categorys):
    mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root', db='Wang_Test')
    langs = ["ZHH", "CHT", "NLD", "ENG", "FRA", "DEU", "ITA", "JPN", "PTG", "RUS", "ESP", "ESM", "ARG"]
    del_headerr(path)
    m = MyFileParserUtil(path)
    # m.del_headerr()
    result = mydb.executeSql(
        'SELECT ZHH,CHT,NLD,ENG,FRA,DEU,ITA,JPN,PTG,RUS,ESP,ESM,ARG from `res_language` where ENG = "{}" '.format(res))
    if len(result) > 0:
        for lang in langs:
            print lang, categorys, result[0][lang]
            m.add_fileValue(lang, categorys, result[0][lang].strip())
    m.write_fileValue()


# ---------------------------------------------------------------------
# 编辑Christmas.iss
# ---------------------------------------------------------------------

def edit_iss(infile, outfile, resPack):
    mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root', db='Wang_Test')
    langs = ["ZHH", "CHT", "NLD", "ENG", "FRA", "DEU", "ITA", "JPN", "PTG", "RUS", "ESP", "ESM", "ARG"]
    result = mydb.executeSql(
        'SELECT ZHH,CHT,NLD,ENG,FRA,DEU,ITA,JPN,PTG,RUS,ESP,ESM,ARG from `res_language` where ENG = "{}" '.format(
            resPack))
    infopen = open(infile, 'r')
    outfopen = open(outfile, 'w')
    try:
        lines = infopen.readlines()
        for line in lines:
            for lang in langs:
                if line.find(lang + ".AppName") == 0:
                    new_line = line.split("=")[0] + "=" + result[0][lang].strip()
                    # print new_line
                    outfopen.writelines(new_line)
                    outfopen.writelines("\n")
                    break
            else:
                outfopen.writelines(line)
    finally:
        infopen.close()
        outfopen.close()


def edit_iss2(infile, outfile, res, resPack, categorys):
    infopen = open(infile, 'r')
    outfopen = open(outfile, 'w')
    try:
        lines = infopen.readlines()
        for line in lines:
            if line.find("OutputBaseFilename") == 0:
                new_line = line.split("for")[0] + "for " + res
                outfopen.writelines(new_line)
                outfopen.writelines("\n")
            elif line.find("VersionInfoDescription") == 0:
                new_line = line.split("=")[0] + "=" + resPack + " Setup"
                outfopen.writelines(new_line)
                outfopen.writelines("\n")
            elif line.find("VersionInfoProductName") == 0:
                new_line = line.split("=")[0] + "=" + resPack
                outfopen.writelines(new_line)
                outfopen.writelines("\n")
            elif line.find("Category_") > 0:
                new_line = line.split("Category_")[
                               0] + "Category_" + res + '.ini"; DestDir: "{commonappdata}\{#OldAppName}\Resources"; Flags: ignoreversion'
                print new_line
                outfopen.writelines(new_line)
                outfopen.writelines("\n")
            elif line.find("SetIniInt") > 0:
                for category in categorys:
                    new_line = line.split("fraCaptionCate")[0] + category + line.split("fraCaptionCate")[1]
                    print new_line
                    outfopen.writelines(new_line)

            else:
                outfopen.writelines(line)
    finally:
        infopen.close()
        outfopen.close()


# ---------------------------------------------------------------------
# 文件拷贝
# ---------------------------------------------------------------------
import os
import shutil
from shutil import copyfile


def copy_uuid_bmp(bmpPath, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        os.makedirs(dst)
    else:
        os.makedirs(dst)
    for png in PNG_NAME:
        file = bmpPath + "//" + png
        if os.path.exists(file):
            copyfile(file, dst + "//" + png)


def copy_not_uuid_file(bmpPath, dst, type=0):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        os.makedirs(dst)
    else:
        os.makedirs(dst)
    files = os.listdir(bmpPath)
    if type == 0:
        for f in files:
            if ".mp4" in f:
                mp4 = bmpPath + "\\" + f
                copyfile(mp4, dst + "//" + f)
                continue
            if ".png" in f:
                png = bmpPath + "\\" + f
                copyfile(png, dst + "//" + f)
                continue
    else:
        for f in files:
            if ".bmp" in f and "}.bmp" not in f:
                bmp = bmpPath + "\\" + f
                copyfile(bmp, dst + "//" + f)
                continue


def delblankline(infile, outfile):
    """
    删除每行的空格
    :param infile:
    :param outfile:
    """
    infopen = open(infile, 'r')
    outfopen = open(outfile, 'w')
    try:
        lines = infopen.readlines()
        for line in lines:
            if line.find("=") > 0:
                new_line = line.split("=")[0].strip() + "=" + line.split("=")[1].strip()
                outfopen.writelines(new_line)
                outfopen.writelines("\n")
            else:
                outfopen.writelines(line.strip())
                outfopen.writelines("\n")
    finally:
        infopen.close()
        outfopen.close()


def copy_file(filePath, dst):
    if os.path.exists(filePath):
        files = os.listdir(filePath)
        # print bmps
        if os.path.exists(dst):
            shutil.rmtree(dst)
            os.makedirs(dst)
        else:
            os.makedirs(dst)
        for f in files:
            file = filePath + "\\" + f
            # print file
            copyfile(file, dst + "//" + f)
    else:
        print "不存在：" + filePath


def copy_dir(srcdir, dstdir):
    if os.path.exists(dstdir):
        shutil.rmtree(dstdir)
    shutil.copytree(srcdir, dstdir)


if __name__ == '__main__':

    # 资源类型(需要修改)
    categorys = ["fraCaptionCate_71", "fraTransCate_61"]
    # 资源名称(需要修改)
    resName = "Chinese New Year"
    # 资源包名称(需要修改)
    packName = "Chinese New Year Pack"
    template_name = r"C:\Users\ws\Desktop\fimmora8.x\Setup_"
    f_source_path = r"C:\Users\ws\Desktop\Setup_" + resName
    # 原文件路径(需要修改)
    r_source_path = r"C:\Users\ws\Desktop\Clean Call Outs\ProgramData\Resources\\"

    # ---------------------------------------------------------------------
    # 复制文件夹到桌面
    copyDir(template_name, f_source_path)
    time.sleep(5)

    # 处理Resources目录
    print "---------------------------处理Resources目录---------------------"
    # 处理xml文件
    xmlPath = r"C:\Users\ws\Desktop\fimmora8.x\conver_8.x\MergeXML\CaptionResource_.xml"
    new_xmlPath = f_source_path + r"\Resources\Captions\CaptionResource_" + resName + ".xml"
    # print new_xmlPath
    tree = read(xmlPath)
    edit_ResourceType(tree)
    edit_ResourceTag(tree, resName)
    edit_Opener_BackVideo(tree)
    edit_Texture(tree, resName)
    edit_VideoParam(tree, resName)
    xmlUtils.write_xml(tree, new_xmlPath)

    # 源地址
    srcPng = r_source_path + r"Captions\CustomCaption"
    srcBmp = r_source_path + r"Captions\Thumbnail"
    sre16_9 = r_source_path + r"Captions\Titles\16_9"
    # 目标地址
    dstpng = f_source_path + r"\Resources\Captions\Titles\\" + resName
    dstbmp = f_source_path + r"\Resources\Captions\Thumbnail"
    dst16_9 = f_source_path + r"\Resources\Captions\Titles\16_9"

    # 根据uuid复制png
    copy_uuid_bmp(srcPng, dstpng)
    # 复制MP4与png
    copy_not_uuid_file(srcPng, dstpng, 0)
    # 复制bmp
    copy_not_uuid_file(srcPng, dstbmp, 1)
    # 复制bmp
    copy_file(srcBmp, dstbmp)
    # 复制16:9
    copy_file(sre16_9, dst16_9)

    # ---------------------------------------------------------------------
    # 处理bin目录
    print "---------------------------处理bin目录---------------------"
    # 1.处理ini文件
    iniPath = r"C:\Users\ws\Desktop\fimmora8.x\Category_.ini"
    src_iniPath = f_source_path + r"\Bin\Category_" + resName + ".ini"
    modify_file(iniPath)
    edit_ini(iniPath, resName, categorys)
    delblankline(iniPath, src_iniPath)

    # 2.处理Fonts文件夹
    srcFonts = r_source_path + r"Fonts"
    dstFonts = f_source_path + r"\Bin\Fonts"
    copy_file(srcFonts, dstFonts)

    # ---------------------------------------------------------------------
    # 处理Christmas.iss文件
    print "---------------------------处理Christmas.iss文件---------------------"
    issPath = f_source_path + r"\Christmas.iss"
    issPath2 = r"C:\Users\ws\Desktop\Christmas2.iss"
    issPath3 = r"C:\Users\ws\Desktop\Christmas.iss"

    edit_iss(issPath, issPath2, resName)
    edit_iss2(issPath2, issPath3, resName, packName, categorys)
    copyOneFile(issPath3, issPath)

    '''
    处理Transitions
    '''
    # Transitions的源地址
    trans_src = r_source_path + r"Transitions"
    if os.path.exists(trans_src):
        # Transitions目标地址
        trans_dst = f_source_path + r"\Resources\Transitions"
        trans_src_xmlPath = trans_dst + r"\MergeTransConfig_Temp.xml"
        trans_dst_xmlPath = trans_dst + r"\MergeTransConfig_" + resName + ".xml"
        trans_temp_path = trans_dst + "\Merge\Temp"
        trans_dst_path = trans_dst + "\Merge\\" + resName

        # 复制Transitions文件夹
        copy_dir(trans_src, trans_dst)
        # 修改xml文件名
        shutil.move(trans_src_xmlPath, trans_dst_xmlPath)
        # 修改xml内容
        tree = read(trans_dst_xmlPath)
        edit_temp(tree, resName, "Transitions")
        xmlUtils.write_xml(tree, trans_dst_xmlPath)
        # 修改temp文件夹名
        shutil.move(trans_temp_path, trans_dst_path)

    '''
    处理EffectPlug
    '''
    # EffectPlug的源地址
    effect_src = r_source_path + r"EffectPlug"
    if os.path.exists(effect_src):
        # EffectPlug目标地址
        effect_dst = f_source_path + r"\Resources\EffectPlug"
        effect_src_xmlPath = effect_dst + r"\MergeEffectConfig_Temp.xml"
        effect_dst_xmlPath = effect_dst + r"\MergeEffectConfig_" + resName + ".xml"
        effect_temp_path = effect_dst + "\Merge\Temp"
        effect_dst_path = effect_dst + "\Merge\\" + resName

        # 复制EffectPlug文件夹
        copy_dir(effect_src, effect_dst)
        # 修改xml文件名
        shutil.move(effect_src_xmlPath, effect_dst_xmlPath)
        # 修改xml内容
        tree = read(effect_dst_xmlPath)
        edit_temp(tree, resName, "effect")
        xmlUtils.write_xml(tree, effect_dst_xmlPath)
        # 修改temp文件夹名
        shutil.move(effect_temp_path, effect_dst_path)

    '''
    处理Contents
    '''
    # Contents的源地址
    contents_src = r_source_path + r"Contents"
    if os.path.exists(contents_src):
        # Contents目标地址
        contents_dst = f_source_path + r"\Resources\Contents"
        contents_src_xmlPath = contents_dst + r"\stills\AllStills_Temp.xml"
        contents_dst_xmlPath = contents_dst + r"\stills\AllStills_" + resName + ".xml"
        contents_temp_path = contents_dst + "\stills\Temp"
        contents_dst_path = contents_dst + "\stills\\" + resName

        # 复制Contents文件夹
        copy_dir(contents_src, contents_dst)
        # 修改xml文件名
        shutil.move(contents_src_xmlPath, contents_dst_xmlPath)
        # 修改xml内容
        tree = read(contents_dst_xmlPath)
        edit_temp(tree, resName, "contents")
        xmlUtils.write_xml(tree, contents_dst_xmlPath)
        # 修改temp文件夹名
        shutil.move(contents_temp_path, contents_dst_path)
