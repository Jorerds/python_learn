'''
关于多线程的例子
'''
import threading
import time

def loop1(name):
    print('loop1打印参数 %s'%name)
    time.sleep(4)
    print('结束loop1')

def loop2(name):
    print('loop2打印参数 %s'%name)
    time.sleep(2)
    print('结束loop2')

# 创建这个函数作为主线程，所以这个程序除了被分开的两个线程以外还有一个主线程，一共有三个线程
def main():
    print('主程序开始')
    t1=threading.Thread(target=loop1,args=('老王',))
    # 设置守护线程，一但主线程结束子线程立即结束 守护线程必须要在start之前设置
    t1.setDaemon(True)
    # 设置线程名字
    t1.setName('THR_1')
    t1.start()
    t2=threading.Thread(target=loop2,args=('老李',))
    # 设置守护线程，一但主线程结束子线程立即结束
    t2.setDaemon(True)
    # 设置线程名字
    t2.setName('THR_2')
    t2.start()
    # enumerate 得到当前运行的线程
    for thr in threading.enumerate():
        print('当前正在运行的线程名字：%s'%thr.getName())
    print('正在运行子线程数量为：%s'%threading.activeCount())
    t1.join()
    t2.join()
    print('主程序结束')

if __name__ == '__main__':
    main()