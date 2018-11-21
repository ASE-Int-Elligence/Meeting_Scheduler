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
        self.nb = ttk.Notebook(self)
        # self.nb.pack
        self.load_login_page()
        self.userid = ""
                

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
app.geometry("600x600")
app.title("Meeting Scheduler")
app.mainloop()