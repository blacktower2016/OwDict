#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import json
import urllib.request
import argparse

class Dictionary():
    ''' Translation Dictionary class. Loads dictionary from file
        and stores it as dict. 
    '''
    dictData={}
    filename=''
    
    def __init__(self, filename):
        self.filename = filename
        self.load(self.filename)
        
    
    def load(self, filename):
        ''' reads dictionary from file and stores it in dict self.dictData
        '''
        if os.path.isfile(filename):
            with open(filename, 'r', encoding = 'utf-8') as dictFile:
                self.dictData=json.load(dictFile)
                dictFile.close()
        else:
            with open(filename, 'w', encoding = 'utf-8') as dictFile:
                dictFile.close()
            
    def save(self):        
        '''saves dictionary data to file
        '''        
        with open(self.filename, 'w', encoding = 'utf-8') as dictFile:
            dictFile.write(json.dumps(self.dictData, ensure_ascii = False))
            dictFile.close()
            
    def find_word(self, word):
        ''' searches for the word in dictionary. If not found looks for the word online.
            If found returns word in translation, otherwise empty string ('')
        '''
        #print(self.dictData.keys())
        word = word.lower()
        if (word in self.dictData.keys()):
            return self.dictData[word]
        else:
            if(self.add_word(word)!=False):
                return self.dictData[word]
            else:
                return ''
        
    def add_word(self, word, translation=''):
        ''' adds word to dictionary. If 'translation' is not provided, 
            searches in the online dictionary.
            If word is already in the dictionary, returns False, otherwise returns True
        '''
        if (translation):
            self.dictData[word] = translation
            return True
        else:
            web_translation=self._get_translation_from_web(word)
            #print(web_translation)
            if (web_translation!=False):
                self.dictData[word] = web_translation
                return True
            else:
                return False
        
    def _get_translation_from_web(self, word):
        ''' gets the translation from glosbe.com in json formatted file
            If found, returns translation of the word (first in response)
            otherwise returns False
            Raises urllib.error.URLError error in there is no internet connection.
        '''
        #TODO: What if there is no internet connection?
        
        fromLang = 'eng'    #original language
        destLang = 'rus'    #destination language
        pretty = 'true'     #pretty view of json file
        url_req = "https://glosbe.com/gapi/translate?from="+fromLang+"&dest="\
                  +destLang+"&format=json&phrase="+word+"&page=1&pretty="+pretty
        
        with urllib.request.urlopen(url_req) as resp:
            data = resp.read()
            jl = json.loads(data.decode('utf-8'))
            resp.close()
            #print(jl)
        if (jl['result'] == 'ok') and (len(jl['tuc'])!=0) and ('phrase' in jl['tuc'][0]):
            #print(word+' - ' + jl['tuc'][0]['phrase']['text'])
            return jl['tuc'][0]['phrase']['text']
        else:
            return False
        

def internet_on():
    #for timeout in [1,5]:  
    timeout = 1
    try:
        response=urllib.request.urlopen('http://glosbe.com',timeout=timeout)
        return True
    except urllib.error.URLError as err:
        pass #print(err)
    return False
     

if __name__=='__main__':
    
    ''' if runs as a script, not as an imported module'''
    #print(internet_on())
    def cl_parse():
        '''command line argument parser 
            takes word to translate as an argument
        '''
        parser = argparse.ArgumentParser(description = "Takes a word in English as an argument and translate it into Russian")
        parser.add_argument('word', type = str, help='A word to translate')
        args=parser.parse_args()
        return args.word
        
    #print(cl_parse())
    
    my_dict = Dictionary('my_en_ru')    
    #print(my_dict.dictData)
    #my_dict.add_word('bike', 'мотоцикл')
    try:
        print(str(my_dict.find_word(cl_parse())))
    except urllib.error.URLError:
        print("Error: no connection. Check your internet connection and try again.")
    finally:
        my_dict.save()
    #print(my_dict.dictData.keys())
    #print(my_dict.get_translation_from_web('idiosyncratic'))

    #del my_dict

    #my_dict = Dictionary('my_en_ru')
    #print(my_dict.dictData)

        
