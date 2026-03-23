# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""
"""
print('Hello,荣格-林')
print(0b10111)               #二进制
print(111)                 #十进制
print(0xf1a10)               #十六进制
print(0o111)               #八进制
"""
'''
a=2+9j
b=3+8j
print(a+b)
print(a.imag)
print(a.real)
                          #与   或   非
'''
"""
print(1==1)
print(0==False)
print(-1==True)
print(1==True)
"""

'''
c=[1,2,3,4,5,6,7,8]
a='景德镇鸡排哥'
b="0123456789"  #零到长度减一(从左往右)从负一一直减小(从右往左)改成列表也一样
c.append('dfg')
c.append([12,33,'dd'])
c.append({'q':'12','w':'2233'})
s=c+[1.2,3.4]
c.insert(2,'ko')       #在2号数前增加'ko'
print(c)
print(s)
'''
'''
                          #切片用:操作，前小后大
print(b[:])               #全切片
print(b[1:])              #不取第一个
print(b[:1])              #只取第一个
print(b[1:3])             #从一到二
print(b[1:3:1])           #从一到二间隔为一
print(b[9:2:-2])          #从九到三间隔为二
print(b[0:])              #从第一个开始到最后
print(b[0])               #第一个
print(b[5])               #第六个
print(b[::2])             #间隔为2
print(b[2::])             #从三开始
'''


'''                       #对应赋值
n=5
X=y=n+1
C,D=n,n+1
print(X,y,C,D)
'''
'''
                          #带入中间值c进行赋值交换
a=5;b=7;
print(a,b)
c=a
a=b
b=c
print(a,b)
m=1;n=2
m,n=n,m                   #仅限Python有这种交换赋值方法
'''


'''
import numpy as np        #导入包的方法
a=np.array([1,2,3])
print(a)
a=-3
print(np.abs(a))
'''


'''
temp=9
#>25,短袖;<25,长袖<8羽绒服
if temp>=25:
    print("穿短袖")
elif temp<=15 and temp>8:
    print("穿毛衣")
elif temp<=8:
    print("穿羽绒服")
else:
    print("穿卫衣")
'''



"""
h=5
while h>0:
    print("此轮循环h=",h)
    print("总之就是德国进口的")
    h=h-1
"""

"""
a=[1,2,3,4,]              #逐个操作
for i in a:
    print(i*2)
"""

'''
temp=int(input('这是一段提示性文字:'))
print('这是在您回复input函数后的结果',temp,'摄氏度')
print(type(temp))
'''



'''                   #eval可以让你不用关注是int还是float放心输入数字
ccb=55
a=input("请输入一个公式:")
print(a)
b=eval(input("请输入一个公式："))
print(b)
'''


# print(3)
# print(4)
# print(5)
# print(3,end='')
# print(4,end='')
# print(5,end='')
# print(3,end='\\')
# print(4,end='\\')
# print(5)
# print(3,end='//')
# print(4,end='//')
# print(5)
# print(3,end='\t')
# print(4,end='\t')
# print(5)
# print(3,end='\n')
# print(4,end='\n')
# print(5)
# print('大聪明：\t无效消音')



# a=6;b=9;c=78
# print('{}和{}以及{}的乘积是:'.format(a,b,c),a*b*c)
#print('{}是{}和{}的乘积',format(a,b,c),a*b*c)

# a=eval(input('请输入一个数:'))
# b=eval(input('请输入一个数:'))
# c=eval(input('请输入一个数:'))
# print('{}和{}以及{}的乘积是:'.format(a,b,c),a*b*c)



# a=['字符1','字符2','字符3',4,(5+7j),6.34,7]
# print(a)
# print(len(a))
# print(type(a))
# b=['字符0','字符2','字符3',4,(5+7j),6.34,7]
# print(b)
# print(len(b))
# print(type(b))



#a={'01':'学生1'}

'''
gxy=[1,1.2,'搞什么',1+9j,[1,2,3],(1,2)]
print(gxy)
a=(2,)
b=(2)
'''

"""
c={1:'xiaoh',2:'xiaoj',3:4,4:[1,2,1.3]}
print(c)
"""

'''
a=range(1,7,2)           #从第一个到第n-1个，间隔为m个
for c in a:
    print(c)

print(ord('c'))
print(ord('d'))
'''


# a=eval(input('请输入第一个数字：'))
# b=eval(input('请输入第二个数字：'))
# print('{}和{}的乘积是{}'.format(a,b,a*b))
# print('{2}是{0}和{1}的乘积'.format(a,b,a*b))


'''
a='我爱中国'
print('小明说:{:10}，'.format(a))
print('小明说:{:<10}，'.format(a))
print('小明说:{:>10}，'.format(a))
print('小明说:{:^10}，'.format(a))
print('小明说:{:#<10}，'.format(a))
print('小明说:{:+>10}，'.format(a))
print('小明说:{:*^10}，'.format(a))
'''


"""
a=10000000.8755
print('小明说:{:,},'.format(a))        #逗号用于分割整数部分
a=1254.8755
print('小明说:{:.3},'.format(a))       #.精度
b=157
print('小明说:{:d}。'.format(b))
"""


'''
a=473884725.078589
print('小明说:{:.5}。'.format(a))
print('小明说:{:.5f}。'.format(a))
print('小明说:{:.5%}。'.format(a))
print('小明说:{:.5e}。'.format(a))
print('小明说:{:20.5f}。'.format(a))
print('小明说:{:+^20,.5f}。'.format(a))
'''


'''
a="我爱"
b="中国"
c=a+b
print(c*3)
print("中国"in c)
'''


'''
a="abcdef"
for i in a:
    print(i)
'''

'''
#for循环正在嵌套
a=range(1,5)
for i in a:
    for j in range(5-i):
        print(i)
        print('---')
    print(j)
    print('***')
'''

'''
a=range(1,3)
b=range(1,3)
for i in a:
    for j in b:
        if j%2==0:
            print('{}*{}={}'.format(i,j,i*j))
            break
        else:
            print('{}不是偶数，本轮跳过'.format(j))
            print('本轮i={}，j={}'.format(i,j))



#break和continue
'''



'''
while True:
    s=input("请输入一个名字(按Q退出):")
    if s=="Q":
        break
    print("输入的名字是:",s)
print("程序退出")
'''


'''
s=0
i=0
while i <=100:
    s=s+i
    i=i+1
print(s)
'''


'''
for i in[1,2,3,4,5]:
    for j in [6,7,8,9,10]:
        print(i,",",j)
        if j==7:
            break
'''



'''
def add_dd(a,b):
    c=a+b
    ba=(a+b)/2
    bbq=2*(a+b)
    return c,ba,bbq
print (add_dd(1,2))
'''



"""
def change_list(a):
    a[0]='value changes!'                #将集合a的第0项赋值（可变参数）
a=[1,2,3,4,5]
print(a)
change_list(a)
print(a)
"""



'''
def change_dist(b):
    b[0]='values change!'

b={0:"0",1:"1",2:"2"}                  #将字典b的第0项赋值（可变参数）
print(b)                             
change_dist(b)                         #调用change_dist导入外部改变后的b
print(b)


def change_str(s):
    s[0]='aaaaa'                  #内部改变无法影响外部（字符串，元组是不可不参数）
    
s='NJUST'
print(s)
change_str(s)
print(s)    
'''

'''
def change_gup(t):
    t=(10,22,33)                  #元组也是不可不参数
    
t=(1,2,3)
print(t)
change_gup(t)
print(t)
'''

'''
def change_num(k):                     #字符串是不可变参数
    k=123456789
    print('in function',id(k))
    
k=13579
print('before function',id(k))
change_num(k)
print('after function',id(k))
'''


'''
def change_num2(p):                     
    p=(1,2,3,4,5)
    print('in function',id(p))
    
p=(5,4,3,2,1)
print('before function',id(p))
change_num2(p)
print('after function',id(p))  
'''

'''
f=lambda a,b:a+b

#def sum_ab(a,b):
#    return a+b


f(1,2)
print(f(1,2))
'''



'''
def an(n):
    if n==1:
        p=1
    else :
        p=an(n-1)+3
    return p

print(an(3))
'''

"""
def bn(n):
    if n==1:
        p=1
    else :
        p=bn(n-1)*5
    return p

print(bn(3))
"""



'''
def fib(t):
    if t==1 or t==2:
        p=1
    else:
        p=fib(t-1)+fib(t-2)
    return p
print(fib(5))
'''


'''
def fib_new(t):
    if t==1 or t==2:
        return 1
    else:
        a1=1
        a2=1
        i=3
        s=0
        while i<=t:
            #a2=a2+a1
            #a1=a2
            s=a1+a2
            i=i+1
            a1=a2
            a2=s                #a1,a2后移
        return s
print(fib_new(5))               #循环方式
'''


'''
s='ajkshfwifoiqwjiopfjio;edk'
a=set(s)                        #set使之转为集合
print(a)
'''


'''
#Python计算派的思路蒙格玛洛撒点法
import random as rd
n=100000
s=0
for i in range(n):
    x=rd.uniform(0,1)
    y=rd.uniform(0,1)
    if x**2+y**2<=1:
        s=s+1
        
p=s/n
result=4*p
print(result)
'''
        