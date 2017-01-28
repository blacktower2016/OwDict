#!/usr/bin/python3
from mydict_back import Dictionary, internet_on
from urllib import error
from tkinter import *

'''This is tkinter UI for owdict (mydict_back.py)
'''

root=Tk()
root.resizable(False,False)
mydict = Dictionary("my_en_ru")

def p(event): #on window destroy saves dictionary file
    #root.configure(cursor="watch")
    mydict.save()
    #root.configure(cursor="arrow")
    
root.bind('<Destroy>',p)


#def find_word(event): #for bind with event
def find_word():
    root.configure(cursor="watch")
    #if internet_on():        #перенести проверку в mydict_back
    try:
        trans.set(mydict.find_word(word.get()))
    except error.URLError as err:
        trans.set("Ошибка: нет подключения!")
    finally: 
        root.configure(cursor="arrow")

word=StringVar()
trans=StringVar()
    
wordFrame = LabelFrame(root)
wordFrame.pack(side = 'top')
transFrame = LabelFrame(root)
transFrame.pack(side = 'bottom')
txtWord = Entry(wordFrame, textvariable = word) 
txtWord.pack(side = 'left')
txtWord.focus_set()
btn = Button(wordFrame, text="Find Word", bg="white", fg="black", command = find_word ) #width=10, height=2
#btn.bind("<Button-1>", find_word)
btn.pack(side = 'right')
lblTrans = Label(transFrame, bg="White", fg='black', textvariable=trans, font=('Times New Roman', 20), width = 25)
lblTrans.pack()

root.bind('<Destroy>',p)

root.bind_all('<Return>', lambda e:find_word())

root.mainloop()
