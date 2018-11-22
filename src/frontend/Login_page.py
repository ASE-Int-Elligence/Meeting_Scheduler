#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json


class Login_page(object):

	def __init__(self):
		self.frame = None

	def setRoot(self, kinter):
		self.root = kinter
		self.frame = Frame(self.root, width = 600, height = 600)
		self.frame.pack(side = LEFT)
		self.frame.columnconfigure(0, {'minsize': 150})
		self.frame.rowconfigure(3, {'minsize': 30})

	def get_page(self, kinter):
		self.setRoot(kinter)
		self.username_label = Label( self.frame, text = "User Name :")
		self.username_label.grid(row = 1, column = 1)
		self.username_entry = Entry( self.frame)
		self.username_entry.grid(row = 1, column = 3)
		self.password_label = Label( self.frame, text = "Password :")
		self.password_label.grid(row = 2, column = 1)
		self.password_entry = Entry( self.frame, show = "*")
		self.password_entry.grid(row = 2, column = 3)
		self.login_button = Button( self.frame, text = "Login", command = self.login_button_pressed )
		self.login_button.configure(width = 6)
		self.login_button.grid(row = 4, column = 2)
		self.newuser_button = Button( self.frame, text = "New User", command = self.newuser_button_pressed)
		self.newuser_button.configure(width = 6)
		self.newuser_button.grid(row = 5, column = 2)

	def login_button_pressed(self):
		self.user_id = self.username_entry.get()
		self.pwd = self.password_entry.get()
		if self.user_id == "" or self.pwd == "":
			messagebox.showinfo("Error", "Fields cannot be empty")
			# do login code here, check if login works or not
		try:
			r = requests.post("http://127.0.0.1:5000/login", data=json.dumps({'username': self.user_id, 'password': self.pwd}))
			print (r.status_code)
			if r.status_code != "200":
				print("Woohoo")
				self.frame.destroy()
				self.root.userid = self.user_id
				self.root.load_home_page()
			else:
				messagebox.showinfo("Error", "Brooo, Wrong Credentials !")
		except:
			messagebox.showinfo("Error", "Brooo, Not Connected to Internet !")



	def newuser_button_pressed(self):
		self.frame.destroy()
		self.root.load_newuser_page()
