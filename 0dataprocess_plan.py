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
    Paths,dirs,AllFile = file_name(rootfile)
    
    inout=pd.read_excel('./date/品牌引入退出时间.xlsx',encoding = "GBK")
    

    #对目录进行拼接
    AllFile = [rootfile+'/'+x for x in AllFile]
    print("=====")
    #文件名升序排列
    AllFile=sorted(AllFile)
    AllData=pd.DataFrame()
    for i in AllFile:
        temp=pd.read_csv(i)
        del temp[u"营销部名称"]
        del temp[u"客户名称"]
        del temp[u"客户经理"]
        del temp[u"经营业态"]
        del temp[u"结算方式"]
        AllData = pd.concat([AllData,temp])
#        break
        pass
    date=sorted(AllData[u"日期"].value_counts().index.tolist())
    DaySum=pd.DataFrame()
    for i in date:
        temp=AllData[AllData[u"日期"]==i]
        temp=pd.DataFrame(temp.iloc[:,4:].sum()).T
        DaySum=pd.concat([DaySum,temp])
#        break
        pass
    DaySum.insert(0,u"日期",date)

    #没有投放的名单
    nodate=inout[inout["退出时间"]==u"没有数据"]
    nodatename=nodate[u"日期"].tolist()
    
    #完整存在
    fulldate=inout[inout["引入时间"]==20170101]
    fulldate=fulldate[fulldate["退出时间"]==-1]
    fulldatename=fulldate[u'日期'].tolist()
    
    #只存在了一段时间
    middledate=inout[inout["引入时间"]!=20170101]
    middledate=middledate[middledate["退出时间"]!=-1]
    middledatename=middledate[u'日期'].tolist()
    
    #已经退出的
    quitdate=inout[inout["引入时间"]==20170101]
    quitdate=quitdate[quitdate["退出时间"]!=-1]
    quitdatename=quitdate[u'日期'].tolist()
    
    #新引进的
    newdate=inout[inout["引入时间"]!=20170101]
    newdate=newdate[newdate["退出时间"]==-1]
    newdatename=newdate[u'日期'].tolist()
    
    for i in nodatename:
        del AllData[i]
#        break
        pass
    
    for i in nodatename:
        del DaySum[i]
#        break
        pass
    
       
    DaySum.to_csv("./date/plan/planDaySum.csv",encoding='GBK',index=False)
    AllData.to_csv("./date/plan/AllData.csv",encoding='GBK',index=False)
    pass
    
    
    
    
    
    
    