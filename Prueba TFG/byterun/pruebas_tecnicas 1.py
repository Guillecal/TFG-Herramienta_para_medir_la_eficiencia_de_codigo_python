# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:38:40 2019

@author: Adrian
"""
dic={}
paco=()
x=3
'''dic['paco',x]=dic['paco',x]+1'''
print(dic)
dic['paco',type(x)]=9
paco=('paco',type(x))

if paco in dic:
    print(dic[paco])
    print('hola')