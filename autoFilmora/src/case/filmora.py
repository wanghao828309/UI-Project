#!/usr/bin/python
# -*- coding: UTF-8 -*-
from uiautomation import *
from autoFilmora.src.page import exportPage
from autoFilmora.src.page import settingPage
from autoFilmora.src.page import homePage
from autoFilmora.src.utils import mediaInfoUtil
from autoFilmora.src.utils import ExcelUtil
import os, time


def get_AppAuto_path():
    pwd = os.getcwd()
    # print(pwd)
    path = pwd.split("autoFilmora")[0] + "autoFilmora"
    return path


screenshotPath = get_AppAuto_path() + "\\screenshot\\"
now = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))


class FilmoraRun():

    def setFrameRate(self, resolution, frameRate):
        # print(resolution,frameRate)
        if exportPage.ExportPage.v_exportText():
            homePage.HomePage.clickFile()
            homePage.HomePage.clickProSet()
            if resolution in (
                    "512x512 (1:1 Square)", "600x600 (1:1 Square)", "1080x1080 (1:1 Square)",
                    "720x1280 (9:16 Portrait)",
                    "1080x1920 (9:16 Portrait)", "2160x3840 (9:16 Portrait)"):
                homePage.HomePage.selectResolution2(resolution)
            else:
                homePage.HomePage.selectResolution(resolution)
            homePage.HomePage.selectFrameRate(frameRate)
            homePage.HomePage.clickOk()
            homePage.HomePage.clickEXPORT()
        else:
            homePage.HomePage.clickFile()
            homePage.HomePage.clickProSet()
            if resolution in (
                    "512x512 (1:1 Square)", "600x600 (1:1 Square)", "1080x1080 (1:1 Square)",
                    "720x1280 (9:16 Portrait)",
                    "1080x1920 (9:16 Portrait)", "2160x3840 (9:16 Portrait)"):
                homePage.HomePage.selectResolution2(resolution)
            else:
                homePage.HomePage.selectResolution(resolution)
            homePage.HomePage.selectFrameRate(frameRate)
            homePage.HomePage.clickOk()
            homePage.HomePage.clickEXPORT()

    def exportCase(self, i, format, name, encoder="H.264", resolution="1920*1080", frameRate="29.97 fps",
                   videoBitrate="8000 kbps", audioEncoder="AAC", channel="Stereo", sampleRate="44100 Hz",
                   audioBitrate="192 kbps", page=0, path=""):
        # PaneControl(ClassName="Qt5QWindowIcon").SetFocus()
        exportPage.ExportPage.inputName(name)
        exportPage.ExportPage.clickFormat(format)
        exportPage.ExportPage.clickSetting()
        settingPage.SettingPage.clickDefault()
        vals = settingPage.SettingPage.get_videoValues()
        if encoder != vals[0]:
            settingPage.SettingPage.selectEncoder(encoder)
        if resolution != vals[1]:
            settingPage.SettingPage.selectResolution(resolution)
        if frameRate != vals[2]:
            if (frameRate in ("60 fps", "120 fps", "240 fps")) and settingPage.SettingPage.getFrameRateNum() == 10:
                settingPage.SettingPage.selectFrameRate2(frameRate)
            else:
                settingPage.SettingPage.selectFrameRate(frameRate)
        # print settingPage.SettingPage.getBitRateNum()
        if videoBitrate != vals[3]:
            if (videoBitrate in (
                    "20000 kbps", "30000 kbps", "80000 kbps", "10000 kbps",
                    "15000 kbps")) and settingPage.SettingPage.getBitRateNum() == 10:
                settingPage.SettingPage.selectVideoBitrate2(videoBitrate)
            else:
                settingPage.SettingPage.selectVideoBitrate(videoBitrate)
        if audioEncoder != vals[4]:
            settingPage.SettingPage.selectAudioEncoder(audioEncoder)
        if channel != vals[5]:
            settingPage.SettingPage.selectChannel(channel)
        if sampleRate != vals[6]:
            settingPage.SettingPage.selectSampleRate(sampleRate)
        if audioBitrate != vals[7]:
            settingPage.SettingPage.selectAudioBitrate(audioBitrate)
        # GetForegroundControl().CaptureToImage(screenshotPath + name + "_" + now + ".jpg")
        # ExcelUtil.MyExcelUtil(path).write_data(i, 13, screenshotPath + name + "_" + now + ".jpg",
        #                                    ExcelUtil.MyExcelUtil.set_style(4), page)
        settingPage.SettingPage.clickOk()
        exportPage.ExportPage.clickExport()
        exportPage.ExportPage.v_completedText()

        if format == "MPEG-2":
            filePath = settingPage.SettingPage.getPathValue() + "//" + name + ".mpg"
        elif format == "HEVC":
            filePath = settingPage.SettingPage.getPathValue() + "//" + name + ".mp4"
        else:
            filePath = settingPage.SettingPage.getPathValue() + "//" + name + "." + format
        # print(filePath)
        if os.path.exists(filePath):
            mediaInfo = mediaInfoUtil.video_analysis(filePath)
            # print(mediaInfo)
        else:
            assert Exception, filePath + " is not Exist"
        # if abs(float(frameRate.split()[0])-float(mediaInfo["v_framerate"])>0.1):
        if mediaInfo["v_framerate"] is None:
            assert Exception, "Frame Rate Mode is Variable"
        elif frameRate.split(" ")[0] not in mediaInfo["v_framerate"]:
            ExcelUtil.MyExcelUtil(path).write_data(i, 16, mediaInfo["v_framerate"],
                                                   ExcelUtil.MyExcelUtil.set_style(6), page)
            assert Exception, "FrameRate is not equal"
        # resoAc = str(mediaInfo["res_width"]) + "*" + str(mediaInfo["res_height"])
        assert str(mediaInfo["res_width"]) in resolution and str(
            mediaInfo["res_height"]) in resolution, "Resolution is not equal"
        assert str(mediaInfo["a_samplerate"]) in sampleRate, "SampleRate is not equal"
        mediaInfoUtil.v_video(format, encoder, mediaInfo["v_encoder"], audioEncoder, mediaInfo["a_encoder"])
        print("--------------------------------")

    def exportGif(self, i, format, name, encoder="GIFV", resolution="640*360", frameRate="10 fps",
                  videoBitrate="1500 kbps", page=0):
        # PaneControl(ClassName="Qt5QWindowIcon").SetFocus()
        exportPage.ExportPage.inputName(name)
        exportPage.ExportPage.clickFormat(format)
        exportPage.ExportPage.clickSetting()
        settingPage.SettingPage.clickDefault()
        settingPage.SettingPage.selectEncoder(encoder)
        settingPage.SettingPage.selectResolution(resolution)
        if (frameRate in ("60 fps", "120 fps", "240 fps")):
            settingPage.SettingPage.selectFrameRate2(frameRate)
        else:
            settingPage.SettingPage.selectFrameRate(frameRate)
        if (videoBitrate in ("20000 kbps", "30000 kbps", "80000 kbps")):
            settingPage.SettingPage.selectVideoBitrate2(videoBitrate)
        else:
            settingPage.SettingPage.selectVideoBitrate(videoBitrate)
        # GetForegroundControl().CaptureToImage(screenshotPath + name + "_" + now + ".jpg")
        # ExcelUtil.MyExcelUtil().write_data(i, 13, screenshotPath + name + "_" + now + ".jpg",
        #                                    ExcelUtil.MyExcelUtil.set_style(4), page)
        settingPage.SettingPage.clickOk()
        exportPage.ExportPage.clickExport()
        exportPage.ExportPage.v_completedText()

        filePath = settingPage.SettingPage.getPathValue() + "//" + name + "." + format
        if os.path.exists(filePath):
            mediaInfo = mediaInfoUtil.video_analysis(filePath)
            # print(mediaInfo)
        else:
            assert Exception, filePath + " is not Exist"
        resoAc = str(mediaInfo["res_width"]) + "*" + str(mediaInfo["res_height"])
        assert resoAc == resolution, "Resolution is not equal"
        assert mediaInfo["v_encoder"] == "Lossless", "encoder is not equal"
        print("--------------------------------")

    def exportMP3(self, i, format, name, audioEncoder="MP3", channel="Stereo", sampleRate="44100 Hz",
                  audioBitrate="192 kbps", page=0):
        # PaneControl(ClassName="Qt5QWindowIcon").SetFocus()
        exportPage.ExportPage.inputName(name)
        exportPage.ExportPage.clickFormat(format)
        exportPage.ExportPage.clickSetting()
        settingPage.SettingPage.clickDefault()
        settingPage.SettingPage.selectEncoder(audioEncoder)
        settingPage.SettingPage.selectResolution(channel)
        settingPage.SettingPage.selectFrameRate(sampleRate)
        settingPage.SettingPage.selectVideoBitrate(audioBitrate)
        # GetForegroundControl().CaptureToImage(screenshotPath + name + "_" + now + ".jpg")
        # ExcelUtil.MyExcelUtil().write_data(i, 13, screenshotPath + name + "_" + now + ".jpg",
        #                                    ExcelUtil.MyExcelUtil.set_style(4), page)
        settingPage.SettingPage.clickOk()
        exportPage.ExportPage.clickExport()
        exportPage.ExportPage.v_completedText()

        filePath = settingPage.SettingPage.getPathValue() + "//" + name + "." + format
        if os.path.exists(filePath):
            mediaInfo = mediaInfoUtil.video_analysis(filePath)
            # print(mediaInfo)
        else:
            assert Exception, filePath + " is not Exist"
        assert str(mediaInfo["a_samplerate"]) in sampleRate, "SampleRate is not equal"
        print("--------------------------------")

    def exportCasett(self, format, name, encoder="H.264", resolution="1920*1080", frameRate="29.97 fps",
                     videoBitrate="8000 kbps", audioEncoder="AAC", channel="Stereo", sampleRate="44100 Hz",
                     audioBitrate="192 kbps", page=0):
        # PaneControl(ClassName="Qt5QWindowIcon").SetFocus()
        exportPage.ExportPage.inputName(name)
        exportPage.ExportPage.clickFormat(format)
        exportPage.ExportPage.clickSetting()
        settingPage.SettingPage.clickDefault()
        settingPage.SettingPage.selectEncoder(encoder)
        settingPage.SettingPage.selectResolution(resolution)

        if (frameRate in ("60 fps", "120 fps", "240 fps")) and settingPage.SettingPage.getFrameRateNum() == 10:
            settingPage.SettingPage.selectFrameRate2(frameRate)
        else:
            settingPage.SettingPage.selectFrameRate(frameRate)
        # print settingPage.SettingPage.getBitRateNum()
        if (videoBitrate in (
                "20000 kbps", "30000 kbps", "80000 kbps")) and settingPage.SettingPage.getBitRateNum() == 10:
            settingPage.SettingPage.selectVideoBitrate2(videoBitrate)
        else:
            settingPage.SettingPage.selectVideoBitrate(videoBitrate)
        settingPage.SettingPage.selectAudioEncoder(audioEncoder)
        if (channel != "Stereo"):
            settingPage.SettingPage.selectChannel(channel)
        if (sampleRate != "44100 Hz"):
            settingPage.SettingPage.selectSampleRate(sampleRate)
        settingPage.SettingPage.selectAudioBitrate(audioBitrate)
        GetForegroundControl().CaptureToImage(screenshotPath + name + "_" + now + ".jpg")
        settingPage.SettingPage.clickOk()
        exportPage.ExportPage.clickExport()
        exportPage.ExportPage.v_completedText()

        if format == "MPEG-2":
            filePath = settingPage.SettingPage.getPathValue() + "//" + name + ".mpg"
        else:
            filePath = settingPage.SettingPage.getPathValue() + "//" + name + "." + format
        # filePath = "D:\export\WMV.wmv"
        # print(filePath)
        mediaInfo = mediaInfoUtil.video_analysis(filePath)
        print(mediaInfo)
        mediaInfoUtil.v_video(format, encoder, mediaInfo["v_encoder"], audioEncoder, mediaInfo["a_encoder"])
        # resoAc = str(mediaInfo["res_width"]) + "×" + str(mediaInfo["res_height"])
        print resolution
        assert str(mediaInfo["res_width"]) in resolution and str(
            mediaInfo["res_height"]) in resolution, "Resolution is not equal"
        assert str(mediaInfo["a_samplerate"]) in sampleRate, "SampleRate is not equal"
        print("--------------------------------")


if __name__ == '__main__':
    FilmoraRun().exportCasett("WMV", "WMV", encoder="WMV3", resolution=u"320×240", frameRate="12 fps",
                              videoBitrate="256 kbps", audioEncoder="WMA9", sampleRate="44100 Hz",
                              audioBitrate="128 kbps")
    # FilmoraRun().exportCasett("MP4", "MP", resolution="720*480", frameRate="120 fps", videoBitrate="4000 kbps")
    # FilmoraRun().exportCasett("AVI", "AVI", encoder="MPEG-4", resolution="720*480", frameRate="20 fps",
    #                           videoBitrate="4000 kbps", audioEncoder="PCM")
    # FilmoraRun().exportCasett("MOV", "MOV", resolution="720*480", frameRate="120 fps", videoBitrate="4000 kbps")
    # FilmoraRun().exportCasett("F4V", "F4V", resolution="720*480", frameRate="60 fps", videoBitrate="4000 kbps")
    # FilmoraRun().exportCasett("MKV", "MKV", resolution="720*480", frameRate="20 fps", videoBitrate="4000 kbps")
    # FilmoraRun().exportCasett("TS", "TS", resolution="1280*720", frameRate="25 fps", videoBitrate="4000 kbps",
    #                           audioEncoder="MPEG-2 audio")
    # FilmoraRun().setFrameRate("720x480 (4:3)","23.97 fps")
    # FilmoraRun().exportCasett(1, "GIF", "GIFV")
