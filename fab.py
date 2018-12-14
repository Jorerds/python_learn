# 用迭代的方式来实现斐波那契数列
def fab(n):
    n1=1
    n2=1
    n3=1

    if n<1:
        print('请输入大于0的数')
        return -1
    while (n-2)>0:
        n3=n2+n1
        n1=n2
        n2=n3
        n-=1
    return n3

# 用递归实现
# 思路：层层相加
# 例如：当输入5时候 要求5的和那么一层一层往下分解
#          5的和为 4和3的和 而在下面4和3继续分解 4是由3和2的和 3是由2和1的和 然后继续对下一层分解直到全部分解

def fabs(n):
    if n<1:
        return -1
    if n==1 or n==2:
        return 1
    else:
        return fabs(n-1)+fabs(n-2)


res=fabs(5)
print('递归方式%d'%res)

result=fab(5)
if result !=-1:
    print('迭代方式%d'%result)
