# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 19:24:03 2025

@author: xingc
"""

# CaesarEncode.py
ptxt=input("请输入明文文本：")
for p in ptxt:
    if"a"<=p<="z":
        print(chr(ord("a")+(ord(p)-ord("a")+3)%26),end='')
    elif"A"<= p<="Z" :
        print(chr(ord("A")+(ord(p)-ord("A")+3)%26),end='')
    else:
        print(p,end='')

etxt=input("请输入加密后文本：")
for p in etxt:
     if"a"<= p <="z":
         print(chr(ord("a")+(ord(p)-ord("a")-3)%26),end='')
     elif"A"<= p <="Z":
         print(chr(ord("A")+(ord(p)-ord("A")-3)%26),end='')
     else:
         print(p,end='')