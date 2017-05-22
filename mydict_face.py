#!/usr/bin/python3
from mydict_back import Dictionary
from urllib import error
from tkinter import *
from tkinter import messagebox

'''This is tkinter UI for owdict (mydict_back.py)
'''

root=Tk()
root.resizable(False,False)
mydict = Dictionary()

def find_word():
    root.configure(cursor="watch")
    trans.set("Searching...")
    word_to_find = word.get()
    try:
        translation = mydict.db_find_word(word_to_find)
    except error.URLError as err:
        trans.set("Error: no internet connection!")
    else:
        if (translation[0]):
            translation_result = translation[1]
            trans.set(translation_result)
        else:
            translation_result = "Error: "+translation[1]
            messagebox.showerror('Error', translation_result)
            trans.set('')

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

btn.pack(side = 'right')
lblTrans = Label(transFrame, bg="White", fg='black', textvariable=trans, font=('Times New Roman', 20), width = 25)
lblTrans.pack()

#root.bind('<Destroy>',p)

root.bind_all('<Return>', lambda e:find_word())

root.mainloop()
