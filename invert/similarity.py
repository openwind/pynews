# -*- coding:utf-8 -*-

import jieba
import os
import sys
import re
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding('utf-8')


#获取指定路径下所有文件
def getFiles(path):
    fileList1=[]
    fileList2=[]
    files=os.listdir(path)
    
    for f in files:
        if f[0]=='.':
            pass
        else:
            fileList1.append((path+'/'+f,int(f[0:f.index('.')])))
    fileList1.sort(key=lambda x:x[1])
    fileList2=[t[0] for t in fileList1]
    return fileList2

#获取所有文件的分词结果
def cutWord(fileList):
    #fileList=getFiles()
    wordOfFiles=[]
    for f in fileList:
        #filename=path+'/'+f;

        fi=open(f)
        lines=fi.readlines()
        artical=lines[1][lines[1].find(':')+3:-1]
        title=lines[7][lines[7].find(':')+3:-1]
        #print s
        fi.close()
        text=title+artical
        
        p=re.findall(r'<.*?>',text)
        for pp in p:
            text=text.replace(pp,'')
            '''
        signal=['？','?',',',';',':','。','，','；','：','"','“','”','《','》','!',
                '(',')','（','）','——','_','-','’','‘','\'','[',']','【','】','！']
        for sig in signal:
            text=text.replace(sig,'')
            '''
        words=list(jieba.cut_for_search(text))
        s=' '.join(words)

        wordOfFiles.append(s)
    return wordOfFiles

#根据分词结果计算TF-IDF权重
def getWeight(resultOfCut):
    #storeofwords=cutWord(path)
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(resultOfCut))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()

    return word,weight

#查询并返回未排序的结果
def query(sentence,resultOfCut,path):
    degree=[]
    index=[]
    keywords=list(jieba.cut_for_search(sentence))
    wordList,weight=getWeight(resultOfCut)
    for key in keywords:
        if key in wordList:
            index.append(wordList.index(key))
    for i in range(len(weight)):
        w=0
        for j in index:
            w=w+weight[i][j]

        fName=path+'/'+str(i+1)+'.json'
        degree.append((fName,w))
    
    degree=[degree[i] for i in range(len(degree)) if degree[i][1]!=0]
    
    return degree

#对查询结果进行排序
def sortResult(degree):
    degree.sort(key=lambda x:x[1],reverse=True)
    return degree

def sortByTime(arg):
    arg.sort(key=lambda x:x[3],reverse=True)
    return arg

def sortByHot(arg):
    arg.sort(key=lambda x:string.atoi(x[4]),reverse=True)
    return arg
