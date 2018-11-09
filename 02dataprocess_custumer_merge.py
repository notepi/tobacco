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
from time import time

def file_name(file_dir):  
  for paths, dirs, files in os.walk(file_dir): 
#    print(paths) #当前目录路径 
#    print(dirs) #当前路径下所有子目录 
#    print(files) #当前路径下所有非目录子文件 
    pass
  return paths,dirs,files  

if __name__ == "__main__":
    
    AllDataPlan=pd.read_csv("./dataprocess_dataExtract/planData.csv",encoding='GBK')
    AllDataReal=pd.read_csv("./dataprocess_dataExtract/realData.csv",encoding='GBK')
    
    #重命名
    nametemp=AllDataPlan.columns.tolist()
    nametemp[4:]=[i+"_plan" for i in nametemp[4:]]
    AllDataPlan.columns=nametemp
    
    nametemp=AllDataReal.columns.tolist()
    nametemp[4:]=[i+"_real" for i in nametemp[4:]]
    AllDataReal.columns=nametemp
    
    
    a=AllDataPlan.iloc[3:5,:]
    
    #检测过两边都重合
    custmer=AllDataPlan[u"客户编码"].value_counts().index.tolist()
    #起始时间
    start = time()
    cc=[]
    finalA=pd.DataFrame()
    for i in custmer:
        cc.append(len(AllDataReal[AllDataReal[u"客户编码"]==i]))
        pass
    print("took %.2f seconds for" % ((time() - start)))
    
    
    start = time()
    Datatemp=pd.merge(AllDataReal,AllDataPlan,
                on=[u"日期",u"客户编码"],how='left')
    print("took %.2f seconds for" % ((time() - start)))
    
    del Datatemp["档位_y"]
    del Datatemp["订货周期_y"]
    
    
    nametemp=[i.split('_')[0] for i in nametemp]
    cc=[]
    for i in nametemp[4:]:
        cc.append(i+"_real")
        cc.append(i+"_plan")
        pass
    nametemp=nametemp[:4]+cc
    nametemp[2]=nametemp[2]+"_x"
    nametemp[3]=nametemp[3]+"_x"
    final=Datatemp[nametemp]
    
    listd=pd.DataFrame([custmer,cc]).T
    listd.to_csv("./02dataprocess_custumer_merge/list.csv",encoding='GBK',index=False)
    final.to_csv("./02dataprocess_custumer_merge/merge.csv",encoding='GBK',index=False)
        
    pass
    
    
    
    
    
    
    