#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json
from tkinter.scrolledtext import ScrolledText
#from Tabs import *


class Home_page(object):

	def __init__(self):
		self.frame = None

	def get_page(self, kinter):
		self.root = kinter
		self.groups = Frame( self.root.nb )
		self.meetings = Frame( self.root.nb )
		self.root.nb.add( self.groups, text = 'Groups')
		self.root.nb.add( self.meetings, text = 'Meetings')
		self.root.nb.pack( expand = 1, fill = "both")

	def get_groups_page(self):
		try:
			r = requests.post("http://127.0.0.1:5000/display_groups", data=json.dumps({'username': self.root.userid}))
			if r.status_code == 200:
				self.frame.destroy()
				#self.root.load_home_page()
			else:
				messagebox.showinfo("Error", "Wrong Credentials !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")


		


