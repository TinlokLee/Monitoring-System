#/usr/bin/env/ python
# -*- coding=utf-8 -*-

# 使用 seek 监控文件内容，并打印变化内容
pos = 0
while True:
    con = open('1.txt')
    if pos != 0:
        con.seek(pos, 0)
    while True:
        line = con.readline()
        if line.strip():
            print(line.strip())
        pos = pos + len(line)
        if not line.strip():
            break
        con.close()

# 利用工具pyinotify监控文件内容变化，当文件逐渐变大时，可轻松完成任务
import os
import datetime
import pyinotify
import logging

pos = 0
def printLog():
    global pos
    try:
        fd = open('log/1.txt')
        if pos != 0:
            fd.seek(pos, 0)
        while True:
            line = fd.readline()
            if line.strip():
                print(line.strip())
            pos = pos + len(line)
            if not line.strip():
                break
            fd.close()
    except Exception as e:
        print(str(e))

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        try:
            print(log())
        except Exception as e:
            print(str(e))

def main():
    print(log())
    wm = pyinotify.WatchManager()
    wm.add_watch('log/1.txt',pyinotify.ALL_EVENTS, rec=True)
    eh = MyEventHandler()
    notifier = pyinotify.notifier(wm, eh)
    notifier.loop()

if __name__ == "__main__":
    main()
    
