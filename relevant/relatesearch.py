#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import json
import codecs

def edit_distance(s1, s2):
    m, n = len(s1), len(s2)  
    colsize, v1, v2 = m + 1, [], []  
    for i in range((n + 1)):  
        v1.append(i)  
        v2.append(i)  
    for i in range(m + 1)[1:m + 1]:  
        for j in range(n + 1)[1:n + 1]:
            cost = 0
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            minValue = v1[j] + 1
            if minValue > v2[j - 1] + 1:
                minValue = v2[j - 1] + 1
            if minValue > v1[j - 1] + cost:
                minValue = v1[j - 1] + cost
            v2[j] = minValue
        for j in range(n + 1):
            v1[j] = v2[j]
    return v2[n]

def relate_search(keyword):
    result_list = []
    fin = codecs.open("word", "r", "utf-8")
    search_dict = json.load(fin, encoding='utf-8')
    fin.close()
    relate_dict = {}
    for word in search_dict:
        relate_dict[word] = edit_distance(keyword, word)
    #print relate_dict
    top_list = sorted(relate_dict.iteritems(), key=lambda f:f[1])[:6]
    temp_list = []
    for i in range(len(top_list)):
        temp_list.append(top_list[i][0].encode('utf-8'))
        if (i+1)%3 == 0:
            result_list.append(temp_list)
            temp_list = []
    return result_list
