# -*- coding: utf-8 -*-

# 使用多线程进行io文件复制操作


import os,threading
from shutil import copyfile,copy

def mkdir(path1,path2):
    '''创建目录'''
    #使用两种文件夹命名
    # path1为中文方式
    # path2为不会出现重复的id方式    
    path1=path1.strip()
    path2=path2.strip()
    is_Exists=os.path1.exists(path1)
    path=''
    if not is_Exists:
        try:
            os.makedirs(path)
            path=path1
        except WindowsError as e:
            os.makedirs(path2)
            path=path2
        print path+':目录创建成功'
        return path
    else:
        os.makedirs(path2)
        path=path2
        print path+':目录已经存在'
        return path

def copy_f(cpath,spath):
    '''
    copyfile方法进行复制文件
    cpath 要复制文件的路径
    spath 要复制到的目录
    '''
    try:
        copyfile(cpath,spath)
    except IOError as er:
        print "os error:%s"%er

def copy_p(cpath,spath):
    '''
    copy的方法复制文件
    cpath 要复制文件的路径
    spath 要复制到的目录
    '''
    try:
        copy(cpath,spath)
    except IOError as e:
        print "os error:%s"%e

def runAll():
    id=10
    name='文件夹名称'
    c_path=r"D:\web\word"
    s_path=r"D:\word"
    path=mkdir(s_path+"\%s"%name,s_path+"\%s"%id)
    t=threading.Thread(target=copy_p,args=(c_path+'\word.txt',path))
    t.setDaemon(True)
    t.start()
    t.join()

if __name__:"__main__":
        runAll()
