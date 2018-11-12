#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:42:26 2018

@author: pan
"""

import numpy as np
import pandas as pd
import os 
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
    #plan的加_paln后缀
    nametemp=AllDataPlan.columns.tolist()
    nametemp[4:]=[i+"_plan" for i in nametemp[4:]]
    AllDataPlan.columns=nametemp
    
    #real的加real后缀
    nametemp=AllDataReal.columns.tolist()
    nametemp[4:]=[i+"_real" for i in nametemp[4:]]
    AllDataReal.columns=nametemp

    
    #对客户购买次数做统计
    #起始时间
    start = time()
    listd=pd.DataFrame([AllDataPlan[u"客户编码"].value_counts().index,
                    AllDataPlan[u"客户编码"].value_counts()]).T
    listd.columns=['ID','times']
    print("took %.2f seconds for" % ((time() - start)))
    
    #将客户的购买和标准进行合并
    #统计后，每行数据包括用户针对每种烟的真实购买记录和公司定额计划
    start = time()
    Datatemp=pd.merge(AllDataReal,AllDataPlan,
                on=[u"日期",u"客户编码"],how='left')
    print("took %.2f seconds for" % ((time() - start)))
    
    #因为两边的都有 档位和购货周期的列，所以合并后会有重复，需要删除
    #删除合并后重复的字段
    del Datatemp["档位_y"]
    del Datatemp["订货周期_y"]
    
    #获取原始的名称
    nametemp=[i.split('_')[0] for i in nametemp]
    
    #增加购买比例的特征
    #如果公司的定额计划是0，则此项标-1
    #起始时间
    start = time()  
    for i in nametemp[4:]:
        Datatemp[i+"_percent"]=Datatemp[i+'_real']/Datatemp[i+'_plan']
        pass
    #除以0的是nan，用-1替换nan
    Datatemp[np.isnan(Datatemp)]=-1
    print("took %.2f seconds for" % ((time() - start)))
    
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
    

    #每种在地区的每日销售都有记录
    saledata=pd.read_csv("./date/real/realDaySum.csv",encoding='GBK')
    adddate=pd.DataFrame()
    #
    adddate[u"日期"]=saledata[u"日期"][20:].tolist()  
    temp=pd.DataFrame()
    for i in nametemp[4:]:
        a=saledata[i]
        #列出前20销售日的每日销售
        #temp 第一列是第前20日的
        for j in range(20):
            temp[str(j)]=a[0+j:-20+j].tolist()
            pass
        #对前20-11求和
        twenty2ten=temp.iloc[:,:10].T.sum()
        #对前10-1求和
        ten2yesterday=temp.iloc[:,10:].T.sum()
        
        adddate[i+"_twenty2ten"]=twenty2ten
        adddate[i+"_ten2yesterday"]=ten2yesterday
        
#        break
        pass
      
        
    #与整体的销售数据合并
    start = time()
    Datatemp=pd.merge(Datatemp,adddate,
                on=[u"日期"],how='left')
    print("took %.2f seconds for" % ((time() - start)))
    
    #自动生成实际和预期一一对应的顺序
    cc=[]
    for i in nametemp[4:]:
        cc.append(i+"_real")
        cc.append(i+"_plan")
        cc.append(i+"_percent")
        cc.append(i+"_twenty2ten")
        cc.append(i+"_ten2yesterday")
        pass
    templist=nametemp[:4]+cc
    
    #合并后的有x后缀
    cc=Datatemp.columns.tolist()
    cc[2]=cc[2].split("_")[0]
    cc[3]=cc[3].split("_")[0]
    Datatemp.columns=cc
    Datatemp=Datatemp[templist]  
    
#    #写入数据
#    start = time() 
#    listd.to_csv("./02dataprocess_custumer_merge/list.csv",encoding='GBK',index=False)
#    final.to_csv("./02dataprocess_custumer_merge/merge.csv",encoding='GBK',index=False)
#    print("took %.2f seconds for" % ((time() - start)))   

#test gropby
#    dd=Datatemp.iloc[:,:10].copy()     
#    dgroup=dd.groupby([u"客户编码"])
#测试可行   
#    start = time() 
#    dgroup=Datatemp.groupby([u"客户编码"])
#    def f(inputT):
#
#        c=inputT[j].tolist()
#        tempc=pd.DataFrame()
#        tempc=inputT[[u"日期",u"客户编码"]].reset_index(drop=True)
#            
#        for w in range(1,5):
#            aa=[-1 for x in range(0, w)]
#            tempc[j+'_'+str(-w)]=(aa+c)[:-(w)]
##           break
#            pass
##        tempc[u"日期"]=inputT[u"日期"].reset_index(drop=True)
##        tempc[u"客户编码"]=inputT[u"客户编码"].reset_index(drop=True)
#        return tempc
#    #对每个品种
#    for j in nametemp[4:]:
#        j=j+"_real"
#        a=dgroup.apply(f)
#        break
#        pass
#
#    print("took %.2f seconds for" % ((time() - start))) 

##优化
#    #要获取列的名称
#    cc=[]
#    for i in nametemp[4:]:
#        cc.append(i+"_real")
#        pass
#    cc=nametemp[0:4]+cc
#    
#    start = time() 
#    zz=pd.DataFrame()
#    for i in listd[u"ID"][:5]:
#        print(len(Datatemp[Datatemp[u"客户编码"]==i]))
#        zz=pd.concat([zz,Datatemp[Datatemp[u"客户编码"]==i]])
##        break
#        pass
##    dtemp=Datatemp[Datatemp[u"客户编码"]==i].reset_index(drop=True)
#    
#    dgroup=zz.groupby([u"客户编码"])
#    def f(inputT):
#        #针对所有品类
#        dtemp=inputT[cc]
#        #获取开头
#        tempc=dtemp.iloc[:,:4]
#        #获取数据内容
#        c=dtemp.iloc[:,4:]
#        
#        for w in range(1,5):
#
#            aa=pd.DataFrame(np.ones((w,c.shape[1]))*(-1),columns=cc[4:])
#            bb=pd.concat([aa,c]).iloc[:-w,:].reset_index(drop=True)
#            namett=[i+"_"+str(w) for i in cc[4:]]
#            bb.columns=namett
#            tempc=pd.concat([tempc,bb],axis=1)
##            break
#            pass        
#
#        return len(tempc)
#    a=dgroup.apply(f)
#    print("took %.2f seconds for" % ((time() - start))) 
    
##代码效率慢    
#    start = time()
#    #历边每一个ID
#    finaltemp=pd.DataFrame()
#    for i in listd[u"ID"]:
#        start = time()
#        dtemp=Datatemp[Datatemp[u"客户编码"]==i].reset_index(drop=True)
##        dtemp=temp.iloc[:,4:]
#        #针对每一个品类
#        for j in nametemp[4:]:
#            j=j+"_real"
#            c=dtemp[j].tolist()
#            tempc=pd.DataFrame()
#            
#            for w in range(1,5):
#                aa=[-1 for x in range(0, w)]
#                tempc[j+'_'+str(-w)]=(aa+c)[:-(w)]
##                break
#                pass
#            #对每个品类进行合并
#            dtemp=pd.concat([dtemp,tempc],axis=1)
##            break
#            pass
#        finaltemp=pd.concat([finaltemp,dtemp])
#        print("took %.2f seconds for" % ((time() - start)))    
#        break
#        pass

#最后代码    
    #历边每一个ID
    datatemp=[]
    finaltemp=pd.DataFrame()
    start = time()
    j=0
    for z in listd[u"ID"][:]:
        j=j+1
        print(j)
        dtemp=Datatemp[Datatemp[u"客户编码"]==z].reset_index(drop=True)
        cc=[]
        for i in nametemp[4:]:
            cc.append(i+"_real")
            cc.append(i+"_real")
            pass
        cc=nametemp[0:4]+cc
        #针对每一个品类
        dtemp=dtemp[cc]
        tempc=dtemp.iloc[:,:4]
        c=dtemp.iloc[:,4:]

        for w in range(1,5):
            #生成-1的头数据
            aa=pd.DataFrame(np.ones((w,c.shape[1]))*(-1),columns=cc[4:])
            #添加-1的头数据，删除尾数据
            bb=pd.concat([aa,c]).iloc[:-w,:].reset_index(drop=True)
            namett=[i+"_"+str(w) for i in cc[4:]]
            bb.columns=namett
#            print(len(bb))
#            print(w)
            tempc=pd.concat([tempc,bb],axis=1)
#            break
            pass
        datatemp.append(tempc)
#        print(z)
#        print(len(dtemp))
#        print(len(tempc))
#        finaltemp=pd.concat([finaltemp,tempc])
   
#        break
        pass
        print("took %.2f seconds for" % ((time() - start))) 
        
    start = time()        
    #针对每个用户做完处理后合并
    finaltemp=pd.concat(datatemp)
    datatemp=0
    print("took %.2f seconds for" % ((time() - start))) 
    
    del finaltemp[u"档位"]
    del finaltemp[u"订货周期"]
    
    #个人数据
    start = time()
    final=pd.merge(Datatemp,finaltemp,
                on=[u"日期",u"客户编码"],how='left')
    Datatemp=0
    finaltemp=0
    print("took %.2f seconds for" % ((time() - start)))
    
    #内存勉强够用
    start = time()
    date=adddate[u"日期"]
    final=final[[x in adddate[u"日期"].values for x in final[u"日期"]]]
    print("took %.2f seconds for" % ((time() - start))) 
    
    name=final.columns.tolist()
    namett=[]
    for i in nametemp :
        for j in name:
            if j.split("_")[0]==i:
                namett.append(j)
#            break
            pass
#        break
        pass
    pass
    
    
    
    
    
    
    