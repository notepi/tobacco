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
    AllDataPlan=pd.read_csv("./dataprocess_dataExtract/planData.csv",encoding='GBK')
    AllDataReal=pd.read_csv("./dataprocess_dataExtract/realData.csv",encoding='GBK')
    print("took %.2f seconds for" % ((time() - start))) 
    
    #重命名
    #plan的加_paln后缀
    nametemp=AllDataPlan.columns.tolist()
    nametemp[4:]=[i+"_plan" for i in nametemp[4:]]
    AllDataPlan.columns=nametemp
    
    #real的加real后缀
    nametemp=AllDataReal.columns.tolist()
    nametemp[4:]=[i+"_real" for i in nametemp[4:]]
    AllDataReal.columns=nametemp
    
    #与整体的销售数据合并
    start = time()
    Datatemp=pd.merge(AllDataReal,AllDataPlan,
                on=[u"日期",u"客户编码"],how='left')
    print("took %.2f seconds for" % ((time() - start)))
    
    #因为两边的都有 档位和购货周期的列，所以合并后会有重复，需要删除
    #删除合并后重复的字段
    del Datatemp["档位_y"]
    del Datatemp["订货周期_y"]
    
        #自动生成实际和预期一一对应的顺序
    cc=[]
    for i in nametemp[4:]:
        cc.append(i+"_real")
        cc.append(i+"_plan")
        cc.append(i+"_percent")
        pass
    templist=nametemp[:4]+cc
    
    #合并后的有x后缀
    cc=Datatemp.columns.tolist()
    cc[2]=cc[2].split("_")[0]
    cc[3]=cc[3].split("_")[0]
    Datatemp.columns=cc
    Datatemp=Datatemp[templist]
    
    name=[x.split("_")[0] for x in nametemp]
    
    temp=[]
    for i in name[4:]:
        real=i+"_real"
        plan=i+"_plan"
        Datatemp[i+"_percent"]=Datatemp[real]/Datatemp[plan]
#        break
        pass
    
    nametemp=[x.split("_")[0] for x in nametemp]
    cc=[]
    for i in nametemp[4:]:
        cc.append(i+"_real")
        cc.append(i+"_plan")
        cc.append(i+"_percent")
        pass
    templist=nametemp[:4]+cc    
    Datatemp=Datatemp[templist]  
    
    #除以0的是nan，用-1替换nan
    Datatemp[np.isnan(Datatemp)]=-1

    Datatemp.to_csv("mergedate.csv",encoding='GBK',index=False)
   
    pass


    
    
    
    
    
    
    