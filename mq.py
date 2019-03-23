'''
实现简单的队列功能
'''
from queue import Queue
import threading
import time

queue=Queue()

class   ThreadNum(threading.Thread):
    """每打印一个数字等待1秒，并发打印10个数字"""
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue

    def run(self):
        '''消费者端，从队列中获取num'''
        while True:
            num=self.queue.get()
            print('消费者端%s'%num)
            time.sleep(1)
            self.queue.task_done()

start=time.time()
def main():
# 产生一个 threads pool, 并把消息传递给thread函数进行处理，这里开启10个并发
    a=['一','二','三','四']
    for i in a:
        t=ThreadNum(queue)
        t.setDaemon(True)
        t.start()
    # 往队列中填充数据
    for num in a:
        queue.put(num)
    queue.join()
if __name__=="__main__":
    main()
    print('运行时间%s'%(time.time()-start))