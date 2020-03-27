#coding=utf-8

from PIL import Image,ImageEnhance
import pytesseract
from selenium import webdriver

def savePage(path):
    im = Image.open(path)
    imgry = im.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save(path)


if __name__ == '__main__':
    savePage(r'E:\work\python\UI-Project\tests\testScapy\verify.png')
# url='http://192.168.0.178:8080/WebGis/'
# driver = webdriver.Chrome('chromedriver.exe')
# driver.maximize_window() #将浏览器最大化，以获取更清晰的校验码图片
# driver.get(url)
# driver.save_screenshot('f://gps.png') #截取当前网页，该网页有我们需要的验证码
# imgelement = driver.find_element_by_id('verifyCodeImg') #通过id定位验证码
# location = imgelement.location #获取验证码的x,y轴
# size = imgelement.size  #获取验证码的长宽
# rangle=(int(location['x']),\
#          int(location['y']),\
#          int(location['x']+size['width']),\
#          int(location['y']+size['height'])) #写成我们需要截取的位置坐标
# i=Image.open(r'E:\work\python\UI-Project\tests\testScapy\verify.png') #打开截图
# verifycodeimage=i.crop(rangle)   #使用Image的crop函数，从截图中再次截取我们需要的区域
# verifycodeimage.save('f://verifycodeimage.png')
# image=Image.open(r'E:\work\python\UI-Project\tests\testScapy\verify.png')
#print image
# vcode=pytesseract.image_to_string(image).strip() #使用image_to_string识别验证码
# print vcode
