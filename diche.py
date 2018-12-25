# -*- coding: utf-8 -*-
import urllib,os,re,time
from threading import Thread
from multiprocessing import Process

def downloadURL(urls,dirpath):
    for url in urls:
        if len(url)>0:
            content=urllib.urlopen(url).read()
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            print dirpath+r'/'+url[-26:]
            open(dirpath+'tda.txt','w').write(content)



urls=['https://www.csdn.net/']
downloadURL(urls,'1')
