#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
from Login_page import *
from Home_page import *
from Createuser_page import *

class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)


        

        # self.canvas = Canvas( self, bg = '#FFFFFF', width=600, height=600, scrollregion=(0,0,1800,500))
        # vbar=Scrollbar( self, orient = VERTICAL)
        # vbar.pack(side=RIGHT,fill=Y)
        # vbar.config( command=self.canvas.yview)
        # self.canvas.config(width=600,height=600)
        # self.canvas.config(yscrollcommand=vbar.set)
        # self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.userid = ""
        self.nb = ttk.Notebook(self)
        # self.nb.pack
        self.load_login_page()


    def load_login_page(self):

        self.login_page = Login_page()
        self.login_page.get_page(self)

    def load_newuser_page(self):

        self.createuser_page = Createuser_page()
        self.createuser_page.get_page(self)

    def load_home_page(self):

        self.home_page = Home_page()
        self.home_page.get_page(self)


app = SampleApp()
app.geometry("600x900")
app.title("Meeting Scheduler")
app.mainloop()
