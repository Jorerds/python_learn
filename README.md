# python_learn
python个人学习用记录项目
## 个人学习项目目录
[冒泡排序](https://github.com/Jorerds/python_learn/blob/master/Bubble_sort.py)   
[excel文件编辑](https://github.com/Jorerds/python_learn/blob/master/Merge_excel.py)  
[斐波那契数列](https://github.com/Jorerds/python_learn/blob/master/fab.py)  
[递归写法](https://github.com/Jorerds/python_learn/blob/master/factorial.py)  
[插入排序](https://github.com/Jorerds/python_learn/blob/master/inse_sort.py)  
[time库的使用](https://github.com/Jorerds/python_learn/blob/master/times.py)    
[日志装饰器](https://github.com/Jorerds/python_learn/blob/master/decor.py)

## 学习笔记
### 1.关于None为真为假:  
```
>>> ()==None
False
>>> None is []
False
>>> a=()
>>> a==()
True
>>> a==None
False
```                  
### 2.关于python2.x版本与python3.x版本的print不换行区别        
python3版本中print(end='')中加入了end这个参数，可以设置不换行的字符         
python2并没有end这个参数，那么怎办呢？可以直接在print 结尾时候加上 , 逗号就可以了
