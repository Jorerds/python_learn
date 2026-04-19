# 面试遇到的题目记录

## 代码案例

把一个字典的值进行累加，其中条件有：

1. 浮点型的数据类型正常累加

2. 非浮点型的数据类型则取字典最后的值进行累加

代码如下：

```python
a={
    'a':1.1
    ,'b':2.0
    ,'c':5.0
    ,'d':6
    ,'e':7.5
    ,'f':8.10
}
# 累加初始化
totle=0
# 将字典反转，随后通过获取第一位的键值对从而达到获取到原来字典最后一位
disc_item=next(reversed(a.items()))

for k,v in a.items():
    if isinstance(v,float):
        totle+=v
    else:
        totle+=a[disc_item[0]]
```


