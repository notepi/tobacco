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
    AllDataPlan=pd.read_csv("tt.csv",encoding='GBK')
    print("took %.2f seconds for" % ((time() - start))) 

    start = time()
    AllDataPlan=AllDataPlan.iloc[200000:,]
    print("took %.2f seconds for" % ((time() - start)))     
    
    
       
    nametemp=AllDataPlan.columns.tolist()
    name=[i.split("_")[0] for i in nametemp]
    new_name=list(set(name))
    new_name.sort(key=name.index)
    
    #按种类记录特征的名称
    name=AllDataPlan.columns.tolist()
    namett=[]
    for i in new_name :
        for j in name:
            if j.split("_")[0]==i:
                namett.append(j)
#            break
            pass
#        break
        pass
    pass
    
    #读取要分类烟的名称
    classname=pd.read_csv("classname.csv",encoding='GBK')
    #保留特征的开头
    head=namett[0:4]
    #提取其余的特征名称
    end=namett[4:]
    
    

    #针对每种要检测的烟
    for i in classname.iloc[:,0]:
        i=classname.iloc[:,0][24]
        typename=i
        #针对所有的烟,保存出了要检测的烟其余的名称
        cor=[]
        for j in new_name[4:]:
            #保存出了要检测的烟其余的名称
            if j!=i:
                cor.append(j)
#                break
            pass
        #删除其余烟的 real plan percent
        delname=[]
        for j in cor:
            delname.append(j+"_real")
            delname.append(j+"_plan")
            delname.append(j+"_percent")
#            break
            pass
        
        #提取需要的特征数据
        start = time()       
        mydatename=list(set(nametemp).difference(set(delname)))
        mydate=AllDataPlan[mydatename]
        
        #按种类记录特征的名称
        namett=[]
        for i in new_name :
            for j in mydatename:
                if j.split("_")[0]==i:
                    namett.append(j)
    #            break
                pass
    #        break
            pass
        
        print("took %.2f seconds for" % ((time() - start)))
        
        todataname=[typename+"_real",typename+"_real_1",
                    typename+"_percent",typename+"_plan",
                     typename+"_percent_1"]
        todata=mydate[todataname]


        #对结果进行编码
        def c(temp):
            result=0
            #进行逻辑
            # 当期的plan为0，返回-1
            if temp[typename+"_plan"]<=0:
#                print("a")
                result=-1
                pass
            #档期的plan不为0
            else:
                #实际购买大于等于计划
                if temp[typename+"_real"] >= temp[typename+"_plan"]:
                    result=-2
#                    print("b")
                    pass
                #实际购买小于计划
                else:
                    #上期的plan为0时，赋值为-1
                    #上期的占比为-1表明，上期的plan为-1
                    if temp[typename+"_percent_1"] <= -1:
                        result=-1
#                        print("c")
                        pass
                    #上期的plan不为0
                    else:
                        #上期的real为0
                        if temp[typename+"_real_1"] <=0:
                            #本期实现0突破
                            if temp[typename+"_real"] >0:
#                                print("d")
                                result=-2
                                pass
                            #本期没有实现0突破
                            else:
                                result=1
#                                print("e")
                                pass#本期没有实现0突破
                            pass
                        #上月的real不为0
                        else:
#                            print("f")
                            zf=temp[typename+"_real"]/temp[typename+"_plan"]
                            if zf <= 0.5:
                                result=0
                            elif zf <=0.7:
                                result=1
                            elif zf <=0.9:
                                result=2
                            elif zf <=1.1:
                                result=3
                            elif zf <=1.3:
                                result=4
                            elif zf <=1.5:
                                result=5
                            else:
                                result=6
                                pass
                            pass#上月real不为0
                        pass#当期real不为0
                    pass#档期plan不为0
#            print(result)
            return result            
        resultcl=[]
        
        #apply
        start = time()
        resultcl=todata.apply(c,axis=1)
        print("took %.2f seconds for" % ((time() - start)))
        #释放内存
        todata=0
        
        #提取数据
        delname=[typename+"_real",typename+"_percent",
                 typename+"_plan"]
        mydatename=list(set(mydatename).difference(set(delname)))
        mydate=mydate[mydatename]

        
        #按种类记录特征的名称
        namett=[]
        for i in new_name :
            for j in mydatename:
                if j.split("_")[0]==i:
                    namett.append(j)
    #            break
                pass
    #        break
            pass
        mydate=mydate[namett]
        #组成完整的数据
        mydate['tag']=resultcl  
        
        #释放内存
        resultcl=0
##############################################################################
        #进行分类
        #数据分割
        AllDataPlan=0
        DataTest, DataTrain = train_test_split(mydate, train_size=0.2, random_state=1)

        XdataTrain = DataTrain.iloc[:,2:-1]
        TagTrain = DataTrain.iloc[:,-1]
        #释放内存
        DataTrain=0
        
        XdataTest = DataTest.iloc[:,2:-1]
        TagTest = DataTest.iloc[:,-1]
        
        XdataTestOther=DataTest[[u"日期",u"客户编码"]]
        
        #释放内存
        DataTest=0
        
        #释放总内存
        mydate=0
        
        # 使用随机森林作为分类器，分类器有20课树
        clf = RandomForestClassifier(n_estimators=20)
        
        
        # Utility function to report best scores
        def report(results, n_top=3):
            for i in range(1, n_top + 1):
                candidates = np.flatnonzero(results['rank_test_score'] == i)
                for candidate in candidates:
                    print("Model with rank: {0}".format(i))
                    print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                          results['mean_test_score'][candidate],
                          results['std_test_score'][candidate]))
                    print("Parameters: {0}".format(results['params'][candidate]))
                    print("")
        
        
        # 设置可能学习的参数
        param_dist = {"max_depth": [3, None],
                      "max_features": sp_randint(1, 11),
                      "min_samples_split": sp_randint(2, 11),
                      "min_samples_leaf": sp_randint(1, 11),
                      "bootstrap": [True, False],
                      "criterion": ["gini", "entropy"]}
        
        # 随机搜索， randomized search
        n_iter_search = 35
        random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                           n_iter=n_iter_search)
        #起始时间
        start = time()
        random_search.fit(XdataTrain, TagTrain)
        print("RandomizedSearchCV took %.2f seconds for %d candidates"
              " parameter settings." % ((time() - start), n_iter_search))
        report(random_search.cv_results_)
        
        print("=============================================")
    
        
        #对比分类效果
        #random_search
        #预测结果        
        print("============================random_search=========================================")
        Result = random_search.predict(XdataTest)
        print('The accuracy is:',accuracy_score(TagTest,Result))
        #混淆矩阵
        print('The confusion matrix is:\n',confusion_matrix(TagTest,Result))
        # 3 precision, recall, f1 score
        print('The precision, recall, f1 score are:\n',classification_report(TagTest,Result))
        #all
        print('The precision are:\n',precision_score(TagTest,Result,average='micro'))
        XdataTestOther[i]=Result
        XdataTestOther.to_csv("result_pre.csv",encoding='GBK',index=False)
        break
        pass#每种烟结束
   
    pass


    
    
    
    
    
    
    