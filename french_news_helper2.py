#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 16:33:48 2019

@author: alyshareinard
"""

import requests
from bs4 import BeautifulSoup

#import re
#import cookielib
#import urllib
import nltk
import string
#nltk.download('popular')
import pickle
from googletrans import Translator

def new_words_in_article(url = 'https://www.troyhunt.com/the-773-million-record-collection-1-data-reach/'):
    

    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    
    words = ''
    blacklist = [
    	'[document]',
    	'noscript',
    	'header',
    	'html',
    	'meta',
    	'head', 
    	'input',
    	'script',
        'style',
    	# there may be more elements you don't want, such as "style", etc.
    ]
    
    for t in text:
    	if t.parent.name not in blacklist:
            print("\n\n", t.parent.name, "\n")
            print('{} '.format(t))
            words += '{} '.format(t)
            
    print("Before  ", type(words))  
    words=words.split()
    words=" ".join(words)
    print(words)
    table = str.maketrans('', '', string.punctuation.replace("-", "").replace('\'', ""))

    stripped = [w.translate(table) for w in words]
    stripped = ''.join(c for c in stripped if not c.isdigit())
    print(stripped)
        
    tokens = nltk.word_tokenize(''.join(stripped))
#    print(tokens, len(tokens))
    words = [w.lower() for w in tokens]
    vocab = sorted(set(words))
    print(vocab, len(vocab))
    stop_words = nltk.corpus.stopwords.words('french')
    
    vocab = [w for w in vocab if not w in stop_words]
    
    with open('ignore_words.pickle', 'rb') as f:
        ignore_words=pickle.load(f)
    vocab = [w for w in vocab if not w in ignore_words]
    print(len(vocab))
    translator = Translator()

    try:
        translations = translator.translate(vocab, src='fr', dest='en')
        print("\nDo you know these words (type 'y' or 'n' for each).\nIf it's a proper name or similar type 'y' to add to ignore list")
        new_words={}
        for translation in translations:
    #        translation = translator.translate(word, src='fr', dest='en')
            if translation.origin!=translation.text.lower():
                print(translation.origin, ' -> ', translation.text, "    ")
                ans=input("?")
                if ans.lower()=='y':
                    ignore_words.append(translation.origin)
                elif ans.lower()=='n':
                    new_words[translation.origin]=translation.text
                elif ans.lower()=='q':
                    break
        print("these are the new words: ", new_words)
        
        with open('ignore_words.pickle', 'wb') as f:
            pickle.dump(ignore_words,f)
            
        ans=input("save new words and translations to csv file? ")
        if ans == 'y':
                    
            with open('new_words.csv', 'w') as f:
                print("saving to new_words.csv")
                for key in new_words.keys():
                   f.write("%s,%s\n"%(key,new_words[key]))
    except:
        print("google translate is tired, need to work manually")
        print("\nDo you know these words (type 'y' or 'n' for each).\nIf it's a proper name or similar type 'y' to add to ignore list")
        new_words = []
        for word in vocab:
            ans=input(word+"?")
            if ans.lower()=='y':
                ignore_words.append(word)
            elif ans.lower()=='n':
                new_words.append(word)
            elif ans.lower()=='q':
                break
        print("these are the new words: ", new_words)
        with open('ignore_words.pickle', 'wb') as f:
            pickle.dump(ignore_words,f)
            
        ans=input("save new words and translations to csv file? ")
        if ans == 'y':
                    
            with open('new_words_notrans.csv', 'w') as f:
                print("saving to new_words_notrans.csv")
                for word in new_words:
                   f.write("%s\n"%(word))
