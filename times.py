import calendar
import time



def data_time():
    # 通过time模块的localtime函数获取当前时间
    # 这是一个格式化时间戳的方法，没有返回值所以如果没有传递显示参数默认显示整个格式输出
    day_now=time.localtime()
    print day_now
    #利用拼接的方式来拼接成一个格式化的日期时间
    day_begin = '%d-%d-01' % (day_now.tm_year,day_now.tm_mon)
    print day_begin
    # 通过calendar模块的monthrange方法获取当前这个月份的天数
    # 传递两个参数 第一个参数为当前年，第二个参数为当前月份
    # 返回一个元组，第一个参数为当前时间为周几，第二个为当前月份的天数
    week,monRen=calendar.monthrange(day_now.tm_year,day_now.tm_mon)
    print '今天是周%s,这个月一共有：%d天'%(week,monRen)
    day_end='%d-%d-%d'%(day_now.tm_year,day_now.tm_mon,monRen)
    print day_end
