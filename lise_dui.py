# 笛卡儿积
import itertools,random
    
def puke():
    # 生成一副扑克牌
    huashi=['♠','❤','♦','♣']
    paihao=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    quanfupai=[(i,v) for i in paihao for v in huashi]
    
    return quanfupai
  
def lotte_tick():
    '''以双色球为例的彩票案例'''
    # 生成1-33的不重复组合    
    red=[i for i in itertools.combinations([v for v in range(1,34)],6)]
    # 最终和1-16个蓝球组合      
    finally_set=[(j,c) for c in range(1,16) for j in red]
    print len(finally_set) #最终有16613520组合
    return finally_set

def random_select(set,sum):
    '''随机选取组合'''
    slist=random.sample(set,sum)
    return slist
    
if__name__=="__main__":
    # 随机抽取12张牌
    p=puke()    
    random_select(p,12)
    # 随机抽取5组号码
    l=lotte_tick()
    random_select(l,5)
    
  
