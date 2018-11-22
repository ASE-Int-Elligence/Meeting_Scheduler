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
		self.get_groups_page()

	def get_groups_page(self):
		try:
			r = requests.post("http://127.0.0.1:5000/display_groups", data=json.dumps({'username': self.root.userid}))
			print (r.status_code)
			if r.status_code == 200:
<<<<<<< HEAD
				self.frame.destroy()
				#self.root.load_home_page()
=======
				print ("Chandana is a genius")
				# self.frame.destroy()
				print ("1")
				#self.root.load_home_page()
				#print ("2")
				#	print (r)
>>>>>>> Changes from Srujan
			else:
				messagebox.showinfo("Error", "Brooo !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")
