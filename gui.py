# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:19:47 2019

@author: user
"""
import os
import tkinter as tk
import CloneAllProjects
from tkinter import* 

def userDetails():
    username = entry_1.get()
    password = entry_2.get()
    CloneAllProjects.main(username,password)

my_window = Tk()
frame = Frame( my_window )
my_window.title("C++ Analyser App")
my_window.geometry('400x400')

label_1 = Label(my_window, text = "Enter your username: ")
entry_1 = Entry(my_window)

label_2 = Label(my_window, text = "Enter your password: ")
entry_2 = Entry(my_window, show='*')
button_1 = Button(my_window,text = "Clone Repository",command=userDetails)
button_2 = Button(my_window,text = "Analyse")

label_1.grid(row=0,column=0)
entry_1.grid(row=0,column=1)
label_2.grid(row=0,column=3)
entry_2.grid(row=0,column=4)
button_1.grid(row=1,column=0)
button_2.grid(row=1,column=1)

flist = os.listdir(r'C:\Users\user\Desktop\labproject\Lab Project\Repositories')
 
lbox = tk.Listbox(my_window)
lbox.grid(row=4,column=0)
 
# THE ITEMS INSERTED WITH A LOOP
for item in flist:
    lbox.insert(tk.END, item)
 
my_window.mainloop()
    
