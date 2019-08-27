# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 22:28:29 2019

@author: user
"""
import numpy as np
import pandas as pd
from pandas import DataFrame

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure

import threading

import tkinter as tk
from tkinter import ttk
from tkinter import *

import os
import CloneAllProjects
import project_example
import AnalyseProject


LARGE_FONT= ("Verdana", 12)

obj = AnalyseProject.ProjectResults
x = []
     
def selected(lbox,controller):
    global x,y,z,obj
    all_items = lbox.get(0,tk.END)
    sel_idx= lbox.curselection()
    sel_list = [all_items[item] for item in sel_idx]
    sel_item = lbox.get(tk.ANCHOR)
    res = project_example.setName(sel_item)
    obj = res
    controller.show_frame(PageOne)
    return obj

def allprojects(controller):
    res = AnalyseProject.AnalyseAllProjects()
    controller.show_frame(PageTwo)
    return res
    
def clear(canvas):
        canvas.get_tk_widget().clear()
    
  
class ProjectAnalyser(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=None)
        tk.Tk.wm_title(self, "C++ Analyser Program")
        
        screen_width = str(self.winfo_screenwidth()//2)
        screen_height = str(self.winfo_screenheight()//2)
        resolution =screen_width +'x'+screen_height
        self.geometry(resolution)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (StartPage,PageOne,PageTwo,PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
               
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        flist = os.listdir(os.getcwd()+os.sep+r'Repositories')
        lbox = tk.Listbox(self)
        lbox.place(relx=0.533, rely=0.044, relheight=0.858, relwidth=0.44)
        
        for item in flist:
            lbox.insert(tk.END, item)
                         
        button = ttk.Button(self, text="Analyse",
                            command=lambda:(threading.Thread(target=selected,args=(lbox,controller,)).start()))

        button.place(relx=0.533, rely=0.911, height=32, width=68)
  
        #button.pack(rex=0.533, rely=0.911, height=32, width=68) command=lambda:controller.show_frame(PageOne))
        
        button2 = ttk.Button(self, text="Analyse All",
                             command=lambda:(threading.Thread(target=allprojects,args=(controller,)).start()))
        button2.place(relx=0.8, rely=0.911, height=32, width=98)
        
        TProgressbar1 = ttk.Progressbar(self)
        TProgressbar1.place(relx=0.1, rely=0.422, relwidth=0.417
                , relheight=0.0, height=22)
        TProgressbar1.configure(length="250")
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.0, rely=0.044, height=31, width=59)
#        Label1.configure(background="#d9d9d9")
#        Label1.configure(disabledforeground="#a3a3a3")
#        Label1.configure(foreground="#000000")
        Label1.configure(text='''Username :''')
        
        Label2 = tk.Label(self)
        Label2.place(relx=0.0, rely=0.111, height=31, width=55)
#        self.Label2.configure(background="#d9d9d9")
#        self.Label2.configure(disabledforeground="#a3a3a3")
#        self.Label2.configure(foreground="#000000")
        Label2.configure(text='''Password :''')

        Label3 = tk.Label(self)
        Label3.place(relx=0.0, rely=0.178, height=31, width=43)
#        self.Label3.configure(background="#d9d9d9")
#        self.Label3.configure(disabledforeground="#a3a3a3")
#        self.Label3.configure(foreground="#000000")
        Label3.configure(text='''Year :''')
        
        Entry1 = tk.Entry(self)
        Entry1.place(relx=0.15, rely=0.044,height=26, relwidth=0.357)
#        self.Entry1.configure(background="white")
#        self.Entry1.configure(disabledforeground="#a3a3a3")
#        self.Entry1.configure(font="TkFixedFont")
#        self.Entry1.configure(foreground="#000000")
#        self.Entry1.configure(insertbackground="black")
        Entry1.configure(width=214)

        Entry2 = tk.Entry(self)
        Entry2.place(relx=0.15, rely=0.111,height=26, relwidth=0.357)
#        self.Entry2.configure(background="white")
#        self.Entry2.configure(disabledforeground="#a3a3a3")
#        self.Entry2.configure(font="TkFixedFont")
#        self.Entry2.configure(foreground="#000000")
#        self.Entry2.configure(insertbackground="black")
#        self.Entry2.configure(width=214)
        Entry2.configure(show='*')

        Entry3 = tk.Entry(self)
        Entry3.place(relx=0.15, rely=0.178,height=26, relwidth=0.357)
#        self.Entry3.configure(background="white")
#        self.Entry3.configure(disabledforeground="#a3a3a3")
#        self.Entry3.configure(font="TkFixedFont")
#        self.Entry3.configure(foreground="#000000")
#        self.Entry3.configure(insertbackground="black")
        Entry3.configure(width=214)
                     
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Keywords Results")
    
        tabControl.pack(expan = 1,fill = "both")
        
        button1 = ttk.Button(self, text="View Keyword Results",
                            command=lambda: (self.plot(canvas,figure1)))
        button2 = ttk.Button(self, text="Next",
                            command=lambda:(controller.show_frame(PageTwo)))
        button3 = ttk.Button(self, text="Back to Home",
                            command=lambda:(controller.show_frame(StartPage)))
        
        button1.place(relx=0.28, rely=0.049,height=26, width=96)
        button2.place(relx=0.20, rely=0.049,height=26, width=68)
        button3.place(relx=0.10, rely=0.049,height=26, width=87)
        
#        button1.pack(side="left")
#        button2.pack(side ="left")

    def plot(self,canvas,figure1):
        Label1 = tk.Label(self)
        Label1.place(relx=0.55, rely=0.050, height=55, width=500)
#        Label1.configure(background="#d9d9d9")
#        Label1.configure(disabledforeground="#a3a3a3")
#        Label1.configure(foreground="#000000")
        Label1.configure(text='''Number of constant functions, variables or arguments : ''' + str(obj.const)+ '''\n'''+
                         str(obj.const_funcs) + ''' functions,''' + str(obj.const_vars) + ''' variables and ''' + str(obj.const_args) + ''' arguments. \n'''
                         '''Number of static functions or variables: ''' + str(obj.static) + '''\n'''+
                         str(obj.static_funcs) + ''' functions and ''' + str(obj.static_vars) + ''' variables.''')
        
        const = [obj.const_funcs, obj.const_args, obj.const_args]
        static = [obj.static_funcs,obj.static_vars,0]
        index = ['as a function', 'as a variable', 'as an argument']
        df = pd.DataFrame({'const': const,
                    'static': static}, index=index)

        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)

        df.plot(kind='bar', legend=True, ax=ax1, rot =0)
        ax1.set_title('Keywords Vs. Extent of use')
        
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2,text="Inheritance Results")
        tabControl.pack(expan = 1,fill = "both")
               
        button1 = ttk.Button(self, text="Inheritance Results",
                            command=lambda:(self.plot2(canvas,figure1)))
        
        button2 = ttk.Button(self, text="Next",
                            command=lambda:(controller.show_frame(PageThree)))
        
        button3 = ttk.Button(self, text="Previous",
                            command=lambda:(controller.show_frame(PageOne)))
        
        button1.place(relx=0.28, rely=0.049,height=26, width=115)
        button2.place(relx=0.20, rely=0.049,height=26, width=68)
        button3.place(relx=0.10, rely=0.049,height=26, width=68)
               
    def plot2(self,canvas,figure1):
        Label1 = tk.Label(self)
        Label1.place(relx=0.45, rely=0.047, height=55, width=500)
#        Label1.configure(background="#d9d9d9")
#        Label1.configure(disabledforeground="#a3a3a3")
#        Label1.configure(foreground="#000000")
        Label1.configure(text='''Number of classes in the project: ''' + str(obj.classes)+ '''\n'''+
                         '''Number of classes using public inheritance:''' + str(obj.public_inheritance)+ ''' \n'''+
                         '''Number of abstract base classes: ''' + str(obj.abstr_base_classes) + '''    &   '''+
                         '''Number of times ABC was used in code: ''' + str(obj.abc_used)+ '''\n'''
                         '''Number of classes using override functions: ''' + str(obj.override))
       
        df = pd.DataFrame({'lab':['Classes Present', 'Public Inheritance', 'ABC','Times ABC used', 'Ovveride'], 
                           'val':[obj.classes, obj.public_inheritance, obj.abstr_base_classes,obj.abc_used,obj.override]})
        
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        df.plot.bar(x='lab', y='val', rot=0, ax=ax1)   
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Enum & Pointer Results")
       
        tabControl.pack(expan = 1,fill = "both")
#               
        button1 = ttk.Button(self, text="View Results",
                            command=lambda:(self.plot3(canvas,figure1)))
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda:(controller.show_frame(StartPage)))
        button3 = ttk.Button(self, text="Previous",
                            command=lambda:(controller.show_frame(PageOne)))
        
        button1.place(relx=0.28, rely=0.049,height=26, width=68)
        button2.place(relx=0.20, rely=0.049,height=26, width=68)
        button3.place(relx=0.10, rely=0.049,height=26, width=68)
      
        
    def plot3(self,canvas,figure1):
        Label1 = tk.Label(self)
        Label1.place(relx=0.45, rely=0.047, height=95, width=500)

        Label1.configure(text='''Number of enumerations: ''' + str(obj.enum)+ ''' & '''+
                         '''Number of scoped enumerations:''' + str(obj.enum_class)+ ''' \n'''+
                         '''Number of STL vectors or maps: ''' + str(obj.stl) + ''' \n'''+  str(obj.vector) + ''' vectors and ''' + str(obj.map) + ''' maps. \n'''
                         '''Number of times "auto" keyword was used in the code: ''' + str(obj.auto)+ '''\n'''
                         '''Number of times pointers were used: ''' + str(obj.pointers) + '''\n'''+ str(obj.unique) +
                         '''  unique smart pointers ''' + str(obj.shared) + '''  shared pointers and ''' + str(obj.raw) +  '''  raw pointers( "*" or "&")''')
 
       
        
        figure1,axes = plt.subplots(nrows=1, ncols=2,figsize=(15,5))
        df = pd.DataFrame({'Features':['Enumerations', 'Scoped'+'\n'+ 'Enumerations', 
                                       'Unique Pointer','Shared Pointer','Raw Pointer'], 
    'usage value':[(obj.enum - obj.enum_class), obj.enum_class, obj.unique,obj.shared,obj.raw]})
        
        #figure1 = plt.Figure(figsize=(5,5), dpi=100)
        #ax1 = figure1.add_subplot(211)
        df.plot.bar(x='Features', y='usage value', rot=0, ax=axes[0])   
#        canvas = FigureCanvasTkAgg(figure1, self)
#        canvas.draw()
#        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        raw =  {'index': ['Unique Pointers', 'Shared Pointers', 'Raw Pointers'],
                'Pointer Usage': [obj.unique,obj.shared ,obj.raw]}
#        df1 = pd.DataFrame({'Pointer Usage': [obj.unique,obj.shared ,obj.raw]},
#                  index=['Unique Pointers', 'Shared Pointers', 'Raw Pointers'])
        df1 = pd.DataFrame(raw, columns= ['index','Pointer Usage'])
#                  index=['Unique Pointers', 'Shared Pointers', 'Raw Pointers'])
        #figure2 = plt.Figure(figsize=(5,5), dpi=100)
        #ax2 = figure2.add_subplot(111)
        plt.title('Pointer Usage Summary')
        plt.pie(df1['Pointer Usage'],labels=df1['index'],autopct='%1.1f%%',explode=[0,0.1,0])
        #df1.plot.pie(ax = axes[1],subplots=True,autopct ='%1.0%%f')
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
       
app = ProjectAnalyser()
app.mainloop()