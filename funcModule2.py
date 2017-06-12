# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:56:40 2017

@author: F19465B
"""

import json
from stopwords import allStopWords
import re

def countWordsTweets(filepath):
    dictofwords = dict()
    print('Counting tweets words.')
    trash = ['http','https','com','co','rt']
    with open(filepath,'r',encoding='utf-8') as file:
        for line in file:
            tweet = json.loads(line)
            words = re.sub(r'\W+', ' ', tweet['text']).lower().strip().split()
            for word in trash:
                allStopWords[word]=1
            for word in words:
                if len(word) <=1:
                    continue
                if word in allStopWords:
                    continue
                if word in dictofwords:
                    dictofwords[word]+=1
                else:
                    dictofwords[word] = dict()
                    dictofwords[word]=1
        file.close()
    with open('.\\files\\counted_words.json', 'a') as file:
        json.dump(dictofwords, file, indent=4)        
        file.close()                           
    print('Count for {} words has ended.'.format(len(dictofwords)))    
    #return dictofwords


#def sortCount(dictofwords):
#    lst = [(value,key) for key, value in dictofwords.items()]
#    return sorted(lst, reverse=True)

        
    
    
    
    
    
    
    
    
    