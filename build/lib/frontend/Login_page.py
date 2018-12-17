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
		# self.frame.columnconfigure(0, {'minsize': 100})
		# self.frame.rowconfigure(3, {'minsize': 30})

	def get_page(self, kinter):
		self.setRoot(kinter)
		self.username_label = Label( self.frame, text = "User Name :")
		self.username_label.place( relx = 0.2, rely = 0.35, anchor = CENTER)
		self.username_entry = Entry( self.frame)
		self.username_entry.place( relx = 0.45, rely = 0.35, anchor = CENTER)
		self.password_label = Label( self.frame, text = "Password :")
		self.password_label.place( relx = 0.2, rely = 0.4, anchor = CENTER)
		self.password_entry = Entry( self.frame, show = "*")
		self.password_entry.place( relx = 0.45, rely = 0.4, anchor = CENTER)

		self.login_button = Button( self.frame, text = "Login", command = self.login_button_pressed )
		self.login_button.place( relx = 0.35, rely = 0.5, anchor = CENTER, width = 100)
		# self.forgot_button = Button( self.frame, text = "Forgot Password" )
		# self.forgot_button.place( relx = 0.55, rely = 0.5, anchor = CENTER)

		self.newuser_button = Button( self.frame, text = "New User", command = self.newuser_button_pressed)
		self.newuser_button.place( relx = 0.45, rely = 0.55, anchor = CENTER)

	def login_button_pressed(self):
		self.user_id = self.username_entry.get()
		self.pwd = self.password_entry.get()
		if self.user_id == "" or self.pwd == "":
			messagebox.showinfo("Error", "Fields cannot be empty")

		# self.frame.destroy()
		# self.root.userid = self.user_id
		# self.root.load_home_page()
		
		try:
			r = requests.post("http://127.0.0.1:5000/login", data=json.dumps({'username': self.user_id, 'password': self.pwd}))
			print (r.status_code)
			if r.status_code == 200:
				self.frame.destroy()
				self.root.userid = self.user_id
				self.root.load_home_page()
			else:
				messagebox.showinfo("Error", " Wrong Credentials !")
		except:
			messagebox.showinfo("Error", "Exception in login, Not Connected to Internet !")


	def newuser_button_pressed(self):
		self.frame.destroy()
		self.root.load_newuser_page()
