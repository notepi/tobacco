#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:42:26 2018

@author: pan
"""

import numpy as np
import pandas as pd
import os 
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.externals import joblib  

def file_name(file_dir):  
  for paths, dirs, files in os.walk(file_dir): 
#    print(paths) #当前目录路径 
#    print(dirs) #当前路径下所有子目录 
#    print(files) #当前路径下所有非目录子文件 
    pass
  return paths,dirs,files  

if __name__ == "__main__":
    rootfile="./plan"

    inout=pd.read_excel('./date/品牌引入退出时间.xlsx',encoding = "GBK")
    inout=inout[inout[u"退出时间"]!=u"没有数据"]
    dataplan=pd.read_csv("./date/plan/planDaySum.csv",encoding='GBK')
    datareal=pd.read_csv("./date/real/realDaySum.csv",encoding='GBK')
    quitsave=pd.read_csv("./date/quitsave.csv",encoding='GBK')
    
    datareal["sum"]=datareal.iloc[:,1:].T.sum().T
    dataplan["sum"]=dataplan.iloc[:,1:].T.sum().T

    
    #完整存在
    fulldate=inout[inout["引入时间"]==20170101]
    fulldate=fulldate[fulldate["退出时间"]==-1]
    fulldatename=fulldate[u'日期'].tolist()
    
    
    #只存在了一段时间、剔除
    middledate=inout[inout["引入时间"]!=20170101]
    middledate=middledate[middledate["退出时间"]!=-1]
    middledatename=middledate[u'日期'].tolist()
    

    
    #已经退出的、剔除
    quitdate=inout[inout["引入时间"]==20170101]
    quitdate=quitdate[quitdate["退出时间"]!=-1]
    quitdatename=quitdate[u'日期'].tolist()
    
    #新引进的
    newdate=inout[inout["引入时间"]!=20170101]
    newdate=newdate[newdate["退出时间"]==-1]
    newdatename=newdate[u'日期'].tolist()
    
    finl=fulldatename+newdatename
    
    pd.DataFrame(finl).to_csv("classname.csv",encoding='GBK',index=False)
    

    
    
    pass
    
    
    
    
    
    
    