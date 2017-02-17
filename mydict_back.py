#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import json
import urllib.request
import argparse
import sqlite3

class Dictionary():
    ''' Translation Dictionary class.
    '''

    dict_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dict.db")

    def __init__(self):
        self.db_init()

#============== get translation from web =====================================
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

#=========================sqlite3 version=====================================

    def db_init(self):
        '''initializes sqlite3 database'''
        try:
            conn = sqlite3.connect(self.dict_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS ex (id INTEGER PRIMARY KEY,
                        word text, translation text)''')
        except sqlite3.DatabaseError as err:
            print("Error: " + err)
            raise(sqlite3.DatabaseError)
        else:
            conn.commit()
        finally:
            conn.close()

    def db_add_word(self, word, translation):
        '''adds word and it's translation to the database'''
        try:
            conn = sqlite3.connect(self.dict_db)
            c = conn.cursor()
            c.execute('''INSERT INTO ex (word, translation) VALUES (?,?)''', (word, translation))
        except sqlite3.DatabaseError as err:
            #print("Error: " + err)
            return (False, err)
            raise(sqlite3.DatabaseError)
        else:
            conn.commit()
        finally:
            conn.close()


    def db_find_word(self, word):
        ''' Looks for word translation in the database. If not found
        tries to search for translation in the internet.
        Returns tuple of success(True, False)
        and translation(or error message if attempt fails))
        '''
        conn = sqlite3.connect(self.dict_db)
        c = conn.cursor()
        #c.execute('''CREATE TABLE IF NOT EXISTS ex (id INTEGER PRIMARY KEY, word text, translation text)''')
        c.execute('''SELECT * FROM ex WHERE word=?''', (word,))
        result_list = c.fetchall()
        conn.close()
        if len(result_list)>0:
            #print('FOUND: ')
            #print(result_list)
            return (True, result_list[0][2])
        else:
            #print('Not found! Searching in web-dictionary...')
            try:
                web_translation=self._get_translation_from_web(word)
                if (web_translation):
                    try:
                        self.db_add_word(word, web_translation)
                    except sqlite3.DatabaseError as err:
                        #print("Error: " + err)
                        return (False, err)
                    return (True, web_translation)
                else:
                    return (False, "Translation can not be found")
            except urllib.error.URLError:
                #print("Error: no connection. Check your internet connection and try again.")
                return (False, "No connection. Check your internet connection and try again.")
                #return False


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

    #print('Current dir: '+os.path.abspath(__file__))

    my_dict = Dictionary()

    word = cl_parse()
    translation = my_dict.db_find_word(word)
    if (translation[0]):
        print(word + ": " + translation[1])
    else:
        print("Error: "+translation[1])
