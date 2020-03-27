#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree
# import xpath
import xml.dom.minidom
from xml.dom.minidom import parse
from req.utils.ExcelUtil import MyExcelUtil


def get_doc_root(path):
    doc = parse(path)
    root = etree.fromstring(doc.toprettyxml())
    return root


def get_video(path, id):
    root = get_doc_root(path)
    FrameRate = root.xpath("//FormatInfo/VideoEnc/EncParam/FrameRate/text()")
    videoList = []
    i = 0
    VideoBitrate = root.xpath("/Product/FormatInfo[{}]/VideoEnc/EncParam/VideoBitrate/text()".format(id))
    for v in VideoBitrate:
        i = i + 1
        for v_val in v.split(";"):
            f = FrameRate[i - 1]
            for f_val in f.split(";"):
                VideoFourCC = root.xpath("/Product/FormatInfo[{}]/VideoEnc/EncParam[{}]/@VideoFourCC".format(id, i))[0]
                Resolution = root.xpath("/Product/FormatInfo[{}]/VideoEnc/EncParam[{}]/@Resolution".format(id, i))[0]
                if v_val != "":
                    # print VideoFourCC, Resolution, v_val, f_val
                    videoList.append("{},{},{},{}".format(VideoFourCC, Resolution, v_val, f_val))
    # print videoList
    return videoList


def get_audio(path, id):
    root = get_doc_root(path)
    SampleRate = root.xpath("//FormatInfo/AudioEnc/EncParam/SampleRate/text()")
    audioList = []
    i = 0
    AudioBitrate = root.xpath("/Product/FormatInfo[{}]/AudioEnc/EncParam/AudioBitrate/text()".format(id))
    for a in AudioBitrate:
        i = i + 1
        for a_val in a.split(";"):
            f = SampleRate[i - 1]
            for f_val in f.split(";"):
                AudioFourCC = root.xpath("/Product/FormatInfo[{}]/AudioEnc/EncParam[{}]/@AudioFourCC".format(id, i))[0]
                Channel = root.xpath("/Product/FormatInfo[{}]/AudioEnc/EncParam[{}]/@Channel".format(id, i))[0]
                if a_val != "":
                    # print AudioFourCC, Channel, a_val, f_val
                    audioList.append(
                        "{},{},{},{}".format(AudioFourCC, Channel, a_val, f_val))
    # print audioList
    return audioList


def write_video(path, excelPath, cname):
    root = get_doc_root(path)
    Name = root.xpath("//FormatInfo/Name/text()")
    # print Name
    for index, name in enumerate(Name):
        # print index, name
        if name == cname:
            video = get_video(path, index + 1)
            audio = get_audio(path, index + 1)
            j = len(video) + 1
            i = 1
            for v in video:
                v_list = v.split(",")
                if v_list[0] == "Xvid" or v_list[0] == "MP4V":
                    v_list[0] = "MPEG-4"
                elif v_list[0] == "MJPG":
                    v_list[0] = "MJPEG"
                elif v_list[0] == "H264":
                    v_list[0] = "H.264"
                elif v_list[0] == "MP2V":
                    v_list[0] = "MPEG-2"
                elif v_list[0] == "H263":
                    v_list[0] = "H.263"
                print v_list
                MyExcelUtil(excelPath).write_rowNum_data2(i, 3, MyExcelUtil.set_style(8), index, v_list)
                i = i + 1
            for a in audio:
                a_list = a.split(",")
                if a_list[0] == "MP2A":
                    a_list[0] = "MPEG-2 audio"
                elif a_list[0] == "VBIS":
                    a_list[0] = "Vorbis"

                if a_list[1] == "1":
                    a_list[1] = "Mono"
                elif a_list[1] == "2":
                    a_list[1] = "Stereo"
                else:
                    a_list[1] = "5.1 Surround Sound"
                print a_list
                MyExcelUtil(excelPath).write_rowNum_data2(j, 7, MyExcelUtil.set_style(8), index, a_list)
                j = j + 1


if __name__ == '__main__':
    # root = get_doc_root(r"C:\Program Files\Wondershare\Filmora 9\Format.dat")
    # Name = root.xpath("//FormatInfo/Name/text()")
    # print Name
    Name2 = ['WMV', 'HEVC', 'MP4', 'AVI', 'MOV', 'F4V', 'MKV', 'TS', '3GP', 'MPEG-2', 'WEBM', 'GIF', 'MP3']
    # Name2 = [ 'HEVC', 'MP4', 'AVI', 'MOV', 'F4V', 'MKV', 'TS', '3GP', 'MPEG-2', 'WEBM', 'GIF', 'MP3']
    # Name2 = [ 'AVI', 'MOV', 'F4V', 'MKV', 'TS', '3GP', 'MPEG-2', 'WEBM', 'GIF', 'MP3']
    for n in Name2:
        write_video(r"E:\work\python\UI-Project\req\utils\Format_R_H.dat",
                    r"E:\work\python\UI-Project\autoFilmora\config\autoCase_win10.xls", n)
    # get_doc_root(r"C:\Users\ws\Desktop\res\2_Orb_1\Data\data.xml")