# python递归简单例子
# 求5的阶乘
# 分析：如果要求5的阶乘 那么就是1*2*3*4*5，5的阶乘而乘积为1*2*3*4*5的值

def factorial(n):
    if n==1:  #如果是求的阶乘为1 那么直接返回1
        return 1
    else: 
        return n*factorial(n-1) #但传入n不为1的时候执行，利用递归调用自身函数 进行每次传值，每调用一次减1
        # 第一次执行 factorial(5)=5*factorial(4) 返回 5*24(下面4*6得)=120
        # 第二次执行 factorial(4)=4*factorial(3) 返回 4*6(下面3*2*1得)=24
        # 第三次执行 factorial(3)=3*factorial(2) 返回 3*2*1=6
        # 第四次执行 factorial(2)=2*factorial(1) 返回 2*1
        # 第五次执行 factorial(1)=1 (return)
        # 然后在一层一层往上返回


print(factorial(5))
