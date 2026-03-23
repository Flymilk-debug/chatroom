# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 20:02:49 2025

@author: xingc
"""

ptxt=input("请输入明文文本：")
for p in ptxt:
    if"a"<=p<="z":
        print(chr(ord("a")+(ord(p)-ord("a")-3)%26),end='')
    elif"A"<=p<="Z":
        print(chr(ord("A")+(ord(p)-ord("A")-3)%26),end='')
    elif 0x4E00<=ord(p)<=0x9FA5:#中文字符加密处理
        print(chr(ord(p)-3),end='')
    else:
        print(p,end='')
    
etxt=input("请输入加密后文本：")
for p in etxt:
    if"a"<=p<="z":
        print(chr(ord("a")+(ord(p)-ord("a")+3)%26),end='')
    elif"A"<=p<="Z" :
        print(chr(ord("A")+(ord(p)-ord("A")+3)%26),end='')
    else:
        print(p,end='')