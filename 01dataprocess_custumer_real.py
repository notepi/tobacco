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
    
    AllData=pd.read_csv("./date/real/AllData.csv",encoding='GBK')
    a=AllData.iloc[3:5,:]
    custmer=AllData[u"客户编码"].value_counts().index.tolist()
    for i in custmer:
        print(i)
        temp=AllData[AllData[u"客户编码"]==i]
        temp.to_csv("./date/real/person/"+str(i)+".csv",encoding='GBK',index=False)
#        break
        pass
        
    pass
    
    
    
    
    
    
    