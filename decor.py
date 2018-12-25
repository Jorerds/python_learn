# -*- coding: utf-8 -*-
import functools,datetime,time

# 这里是设计一个装饰器
def log(text='日志'):
    def deco(func):
        @functools.wraps(func)
        def warpper(*args,**kw):
            time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print '%s'%time
            print '%s %s():'%(text,func.__name__)
            data = func(*args, **kw)
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print '%s'%end_time
            return data
        return warpper
    return deco

class decor():

    @log()
    def f(self):
        print '被调用日志装饰器的函数'



obj=decor()
obj.f()

