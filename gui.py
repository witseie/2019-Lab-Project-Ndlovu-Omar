# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 22:28:29 2019

@author: Sanele
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
import AnalyseProject

LARGE_FONT= ("Verdana", 12)

obj = AnalyseProject.ProjectResults
flist = []

#select project from listbox
def selected(lbox,controller):
    global obj
    all_items = lbox.get(0,tk.END)
    sel_idx= lbox.curselection()
    sel_list = [all_items[item] for item in sel_idx]
    sel_item = lbox.get(tk.ANCHOR)
    res = AnalyseProject.AnalyseProject(sel_item)
    obj = res
    controller.show_frame(PageOne)
    return obj

#analyse all projects 
def allprojects(controller):
    global obj
    res = AnalyseProject.AnalyseAllProjects()
    controller.show_frame(PageFour)
    obj = res
    return obj
#get repository names 
def repoDetails(Entry1,Entry2,Entry3,lbox):
    global flist
    username = Entry1.get()
    password = Entry2.get()
    year = Entry3.get()
    
    lbox.delete(0,tk.END)
    names = CloneAllProjects.getRepoNames(username,password,year)
    flist = names
    for item in flist:
        lbox.insert(tk.END, item)
    return flist
#get user credentials
def userDetails(Entry1,Entry2,Entry3):
    global flist
    username = Entry1.get()
    password = Entry2.get()
    year = Entry3.get()  
    CloneAllProjects.cloneAllProjects(username,password,year)

#initialise Tkinter pages
class ProjectAnalyser(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=None)
        tk.Tk.wm_title(self, "C++ Analyser Program")
        #set screen dimensions
        screen_width = str(self.winfo_screenwidth()//2)
        screen_height = str(self.winfo_screenheight()//2)
        resolution =screen_width +'x'+screen_height
        self.geometry(resolution)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        #create page frames
        for F in (StartPage,PageOne,PageTwo,PageThree,PageFour,PageFive):

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

        lbox = tk.Listbox(self)
        lbox.place(relx=0.533, rely=0.044, relheight=0.858, relwidth=0.44)
                               
        button = ttk.Button(self, text="Analyse",
                            command=lambda:(threading.Thread(target=selected,args=(lbox,controller,)).start()))

        button.place(relx=0.533, rely=0.911, height=32, width=68)
  


        button2 = ttk.Button(self, text="Analyse All",
                             command=lambda:(threading.Thread(target=allprojects,args=(controller,)).start()))
        button2.place(relx=0.8, rely=0.911, height=32, width=98)
        
              
#        TProgressbar1 = ttk.Progressbar(self)
#        TProgressbar1.place(relx=0.1, rely=0.422, relwidth=0.417
#                , relheight=0.0, height=22)
#        TProgressbar1.configure(length="250")
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.05, rely=0.044, height=31, width=59)

                  
    
        Label1.configure(text='''Username :''')
        
        Label2 = tk.Label(self)
        Label2.place(relx=0.05, rely=0.111, height=31, width=55)

        Label2.configure(text='''Password :''')

        Label3 = tk.Label(self)
        Label3.place(relx=0.05, rely=0.178, height=31, width=43)

        Label3.configure(text='''Year :''')
        
        Entry1 = tk.Entry(self)
        Entry1.place(relx=0.15, rely=0.044,height=26, relwidth=0.357)

        Entry1.configure(width=214)

        Entry2 = tk.Entry(self)
        Entry2.place(relx=0.15, rely=0.111,height=26, relwidth=0.357)

        Entry2.configure(show='*')

        Entry3 = tk.Entry(self)
        Entry3.place(relx=0.15, rely=0.178,height=26, relwidth=0.357)

        Entry3.configure(width=214)
        
        button3 = ttk.Button(self, text="Search",command=lambda: repoDetails(Entry1,Entry2,Entry3,lbox))
        button3.place(relx=0.15, rely=0.254, height=32, width=68)
        
        button4 = ttk.Button(self, text="Clone All",
                             command=lambda:(threading.Thread(target=userDetails,args=(Entry1,Entry2,Entry3,)).start()))

        button4.place(relx=0.333, rely=0.254, height=32, width=90)
                        

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Keywords Results")
    
        tabControl.pack(expan = 1,fill = "both")
        
        button1 = ttk.Button(self, text="Keyword Results",
                            command=lambda: (self.plot(canvas,figure1)))
        button2 = ttk.Button(self, text="Next",
                            command=lambda:(controller.show_frame(PageTwo)))
        button3 = ttk.Button(self, text="Back to Home",
                            command=lambda:controller.show_frame(StartPage))
        
        button2.place(relx=0.28, rely=0.049,height=26, width=68)
        button1.place(relx=0.20, rely=0.049,height=26, width=96)
        button3.place(relx=0.10, rely=0.049,height=26, width=87)
        
    def plot(self,canvas,figure1):
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.55, rely=0.050, height=55, width=500)

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
        ax1.set_title('Keywords Vs. Extent of use',fontweight="bold")
        
        for p in ax1.patches:
            ax1.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        
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
        
        button2.place(relx=0.32, rely=0.049,height=26, width=68)
        button1.place(relx=0.20, rely=0.049,height=26, width=115)
        button3.place(relx=0.10, rely=0.049,height=26, width=68)
               
    def plot2(self,canvas,figure1):
        
       
        Label1 = tk.Label(self)
        Label1.place(relx=0.45, rely=0.047, height=55, width=500)

        Label1.configure(text='''Number of classes in the project: ''' + str(obj.classes)+ '''\n'''+
                         '''Number of classes using public inheritance:''' + str(obj.public_inheritance)+ ''' \n'''+
                         '''Number of abstract base classes: ''' + str(obj.abstr_base_classes) + '''    &   '''+
                         '''Number of times ABC was used in code: ''' + str(obj.abc_used)+ '''\n'''
                         '''Number of classes using override functions: ''' + str(obj.override))
       
        df = pd.DataFrame({'Features':['Classes Present', 'Public Inheritance', 'Astract Base Classes','Times ABC used', 'Override'], 
                           'usage values':[obj.classes, obj.public_inheritance, obj.abstr_base_classes,obj.abc_used,obj.override]})
        
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        ax1.set_title('Classes and Inheritance Usage',fontweight="bold")
        
        df.plot.bar(x='Features', y='usage values', rot=0, ax=ax1,)  
        
        for p in ax1.patches:
            ax1.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
            
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
              
        button1 = ttk.Button(self, text="View Results",
                            command=lambda:(self.plot3(canvas,figure1)))
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda:(controller.show_frame(StartPage)))
        button3 = ttk.Button(self, text="Previous",
                            command=lambda:(controller.show_frame(PageOne)))
        
        button2.place(relx=0.28, rely=0.049,height=26, width=85)
        button1.place(relx=0.20, rely=0.049,height=26, width=77)
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
        df = pd.DataFrame({'Features':['enum', 'enum class', 
                                       'unique pointer','shared pointer','raw pointer'], 
    'usage value':[(obj.enum - obj.enum_class), obj.enum_class, obj.unique,obj.shared,obj.raw]})
        

        ax1 = df.plot.bar(x='Features', y='usage value', rot=0, ax=axes[0])
       
        for p in ax1.patches:
            ax1.annotate(str(p.get_height()),(p.get_x() * 1.005, p.get_height() * 1.005))  

        raw =  {'index': ['unique Pointers', 'shared Pointers', 'raw pointers'],
                'Pointer Usage': [obj.unique,obj.shared ,obj.raw]}

        df1 = pd.DataFrame(raw, columns= ['index','Pointer Usage'])
        plt.title('Pointer Usage Summary')
        plt.pie(df1['Pointer Usage'],labels=df1['index'],autopct='%1.1f%%',explode=[0,0.1,0])


        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
       
class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Project Keyword Results")
       
        tabControl.pack(expan = 1,fill = "both")

        button1 = ttk.Button(self, text="View Results",
                            command=lambda:(self.plot4(canvas,figure1)))
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda:(controller.show_frame(StartPage)))
        button3 = ttk.Button(self, text="Next",
                            command=lambda:(controller.show_frame(PageFive)))
        
        button3.place(relx=0.25, rely=0.049,height=26, width=68)
        button1.place(relx=0.17, rely=0.049,height=26, width=75)
        button2.place(relx=0.10, rely=0.049,height=26, width=80)
        
    def plot4(self,canvas,figure1):
        Label1 = tk.Label(self)
        Label1.place(relx=0.45, rely=0.050, height=120, width=500)

        Label1.configure(text='''Number of projects that used constant functions, variables or arguments: ''' + str(obj.const)+ '''\n'''+
                         '''Number of projects that used static functions or variables: ''' + str(obj.static)+ ''' \n'''+
                         '''Number of projects that used enumerations: ''' + str(obj.enum-obj.enum_class) + '''\n''' +
                         '''Number of projects that used scoped enumerations: ''' + str(obj.enum_class)+ '''\n'''+
                         '''Number of projects that used vectors: ''' + str(obj.vector) + '''\n'''+
                         '''Number of projects that used maps: '''+ str(obj.map) + '''\n'''+
                         '''Number of projects that used the "auto" keyword: ''' + str(obj.auto) +'''\n'''+
                         '''Number of projects that used smart pointers: ''' + str(obj.pointers))
       

        figure1,axes = plt.subplots(nrows=1, ncols=2,figsize=(15,5))
        
        df = pd.DataFrame({'Keyword Features':['const','static','enum','enum class','override'],
        'usage value':[obj.const,obj.static,(obj.enum - obj.enum_class), obj.enum_class,obj.override]})
                
        ax1 = df.plot.bar(x='Keyword Features', y='usage value', rot=0, ax=axes[0],title = 'Keywords Usage Summary')   
        
        df1 = pd.DataFrame({'Features':['vector','map','auto','smart pointers'], 
            'usage value':[obj.vector,obj.map,obj.auto,obj.pointers]})

        ax = df1.plot.bar(x='Features', y='usage value', rot=0, ax=axes[1],title ='STL And Pointers Usage Summary')   
        
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        for p in ax1.patches:
            ax1.annotate(str(p.get_height()),(p.get_x() * 1.005, p.get_height() * 1.005))
        
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
       
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        canvas = FigureCanvasTkAgg(figure1, self)
        
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Project Keyword Results")
       
        tabControl.pack(expan = 1,fill = "both")

        button1 = ttk.Button(self, text="View Results",
                            command=lambda:(self.plot5(canvas,figure1)))
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda:(controller.show_frame(StartPage)))
        button3 = ttk.Button(self, text="Previous",
                            command=lambda:(controller.show_frame(PageFour)))
        
        button3.place(relx=0.25, rely=0.049,height=26, width=87)
        button1.place(relx=0.17, rely=0.049,height=26, width=80)
        button2.place(relx=0.10, rely=0.049,height=26, width=75)
        
    def plot5(self,canvas,figure1):
        Label1 = tk.Label(self)
        Label1.place(relx=0.45, rely=0.040, height=120, width=500)

        Label1.configure(text='''Average number of classes: ''' + str(obj.classes) + '''\n'''+
                '''Number of projects with number of classes below average: ''' + str(obj.const_args) + '''\n'''
                '''Number of projects that used public inheritance: ''' + str(obj.public_inheritance) + '''\n'''
                '''Number of projects that use abstract base classes: ''' + str(obj.abstr_base_classes) + '''\n'''
               + str(obj.abc_used) + ''' used the ABC correctly at least once and ...'''
                + str(obj.override) + '''used the "override" keyword.''')

        
        df = pd.DataFrame({'Features':['Average No.'+'\n'+'of Classes','No. of Projects with classes'+'\n'+'below average'
                                        ,'Public inheritance','Abstract Base Classes (ABC)','Projects Used'+'\n'+ 'ABC correctly'], 
            'usage value':[obj.classes,obj.const_args,obj.public_inheritance,obj.abstr_base_classes,obj.abc_used]})
        
        figure1 = plt.Figure(figsize=(4,4), dpi=90)
        ax1 = figure1.add_subplot(111)
        ax = df.plot.bar(x='Features', y='usage value', rot=0, ax=ax1, title ='Inheritance and Classes Summary') 
    
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        

if __name__ == '__main__':
    app = ProjectAnalyser()
    app.mainloop()
