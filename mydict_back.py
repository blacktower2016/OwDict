Нет такого файла или каталога
# -*- coding: utf-8 -*-

import os
import json
import urllib.request

class Dictionary():
    ''' Translation Dictionary class. Load dictionary from file
        and store it as dict. 
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
            with open(filename, 'r') as dictFile:
                for line in dictFile:
                    jl = json.loads(line)
                    self.dictData[jl[0]] = jl[1]
                dictFile.close()
        else:
            with open(filename, 'w') as dictFile:
                dictFile.close()
            
    def save(self):        
        '''saves dictionary data to file
        '''        
        with open(self.filename, 'w') as dictFile:
            for item in self.dictData.items():
                dictFile.write(json.dumps(item, ensure_ascii = False))
        dictFile.close()
            
    def find_word(self, word):
        ''' finds word in dictionary. If found returns True, otherwise False
        '''
        if (word in self.dictData.keys()):
            return self.dictData[word]
        else:
            return False
        
    def add_word(self, word):
        ''' Add word to dictionary. If word is already in dictionary,
            returns False, otherwise returns True
        '''
        if (not self.find_word(word)):
            self.dictData[word] = str(input("Enter translation of ( "+word+" ): "))
            return True
        else:
            print("Word '{}' is in dictionary already .", word)
            return False
        
    def get_translation_from_web(self, word):
        ''' gets the translation from glosbe.com in json formatted file
        '''
        fromLang = 'eng'    #original language
        destLang = 'rus'    #destination language
        pretty = 'true'     #pretty view of json file
        url_req = "https://glosbe.com/gapi/translate?from="+fromLang+"&dest="                  +destLang+"&format=json&phrase="+word+"&page=1&pretty="+pretty
        print (url_req)
        with urllib.request.urlopen(url_req) as resp:
            data = resp.read()
            print(data)
            jl = json.loads(data.decode('utf-8'))
            resp.close()
            '''
            with open(word+'.json', 'w') as tmpFile:
                tmpFile.write(data.decode('utf-8'))
                tmpFile.close()

        with open(word+'.json', 'r') as tmpFile:
            jl = json.load(tmpFile)
            tmpFile.close()
        '''
        if (jl['result'] == 'ok') and (len(jl['tuc'])!=0) and ('phrase' in jl['tuc'][0]):
            print(word+' - ' + jl['tuc'][0]['phrase']['text']) #To-Do: add to dictionary.
            return jl['tuc'][0]['phrase']['text']
        else:
            return False


my_dict = Dictionary('my_en_ru')
#print(my_dict.dictData)
#my_dict.add_word('hello')
#my_dict.save()
#print(my_dict.dictData)
print(my_dict.get_translation_from_web('bolek'))

#del my_dict

#my_dict = Dictionary('my_en_ru')
#print(my_dict.dictData)
        
