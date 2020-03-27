# -*- coding: utf-8 -*-
import time, sys
import cv2, os
import numpy as np
from PIL import ImageGrab


class Stats:

    def __init__(self, sequence):
        # sequence of numbers we will process
        # convert all items to floats for numerical processing
        self.sequence = [float(item) for item in sequence]

    def sum(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence)

    def count(self):
        return len(self.sequence)

    def min(self):
        if len(self.sequence) < 1:
            return None
        else:
            return min(self.sequence)

    def max(self):
        if len(self.sequence) < 1:
            return None
        else:
            return max(self.sequence)

    def avg(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence) / len(self.sequence)

    def median(self):
        if len(self.sequence) < 1:
            return None
        else:
            self.sequence.sort()
            return self.sequence[len(self.sequence) // 2]

    def stdev(self):
        if len(self.sequence) < 1:
            return None
        else:
            avg = self.avg()
            sdsq = sum([(i - avg) ** 2 for i in self.sequence])
            stdev = (sdsq / (len(self.sequence) - 1)) ** .5
            return stdev

    def percentile(self, percentile):
        if len(self.sequence) < 1:
            value = None
        elif (percentile >= 100):
            sys.stderr.write('ERROR: percentile must be < 100.  you supplied: %s\n' % percentile)
            value = None
        else:
            element_idx = int(len(self.sequence) * (percentile / 100.0))
            self.sequence.sort()
            value = self.sequence[element_idx]
        return value

def gen_video_frames(video):
    """
    生成视频流迭代器（减小内存占用）
    :param video:
    """
    video_cap = cv2.VideoCapture(video)
    while (True):
        ret, frame = video_cap.read()
        if ret is False:
            break
        yield frame


def get_video_laplacian(video1, video2):
    """
    对比同个视频前后帧
    :param video:
    :return:
    """
    video_other_cap1 = gen_video_frames(video1)
    video_other_cap2 = gen_video_frames(video2)
    imageVar_min_list=[]
    count = 0
    while True:
        count = count + 1
        try:
            video1_frame = next(video_other_cap1)
            video2_frame = next(video_other_cap2)
            imageVar1 = round(cv2.Laplacian(video1_frame, cv2.CV_64F).var(), 2)
            imageVar2 = round(cv2.Laplacian(video2_frame, cv2.CV_64F).var(), 2)
            imageVar_min_list.append(imageVar1-imageVar2)
            print imageVar1, imageVar2,imageVar1-imageVar2
        except StopIteration:
            print('遍历结束')
            break


    statsClass = Stats(imageVar_min_list)
    print("{},{}".format(statsClass.avg(), statsClass.max()))





if __name__ == '__main__':
    r = r"D:\STL\Footages\0055_1080P_25FPS_235Mbps_H264.mp4"
    r1 = r"C:/Users/ws/Desktop\My Video.mp4"
    get_video_laplacian(r, r1)
