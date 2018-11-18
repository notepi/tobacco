#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:42:26 2018

@author: pan
"""
from scipy.stats import randint as sp_randint
import numpy as np
import pandas as pd
from time import time  
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import confusion_matrix, classification_report,precision_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
# 模型评价 混淆矩阵
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":
    
    start = time()
    AllData=pd.read_csv("mergedate.csv",encoding='GBK')
    print("took %.2f seconds for" % ((time() - start)))
    
    data=pd.read_csv("result_pre.csv",encoding='GBK')
    name=data.columns.tolist()[-1]
    
    namelist=[]
    namelist.append(u"日期")
    namelist.append(u"客户编码")
    namelist.append(u"档位")
    namelist.append(u"订货周期")
    namelist.append(name+"_real")
    namelist.append(name+"_plan")
    namelist.append(name+"_percent")
    
    mydate=AllData[namelist]
    
    testdata=data[data[name]==-1]
    
    for i in testdata[u"客户编码"]:
        datatemp=mydate[mydate[u"客户编码"]==i]
        datatemp_1=datatemp[datatemp[name+"_plan"]!=0]
        
        break
        pass
    
#    Datatemp.to_csv("mergedate.csv",encoding='GBK',index=False)
   
    pass


    
    
    
    
    
    
    