#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json
import re


class Createuser_page(object):

	def __init__(self):
		self.frame = None
		self.pass_regex = "^(?=.*\d).{4,15}$"
		self.email_regex = '^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'

	def setRoot(self, kinter):
		self.root = kinter
		self.frame = Frame(self.root, width = 600, height = 600)
		self.frame.pack(side = LEFT)
		self.frame.columnconfigure(0, {'minsize': 150})

	def get_page(self, kinter):
		self.setRoot(kinter)

		self.nu_firstname_label = Label( self.frame, text = "First Name")
		self.nu_firstname_label.place( relx = 0.2, rely = 0.2, anchor = CENTER)
		self.nu_firstname_entry = Entry( self.frame)
		self.nu_firstname_entry.place( relx = 0.55, rely = 0.2, anchor = CENTER)

		self.nu_lastname_label = Label( self.frame, text = "Last Name")
		self.nu_lastname_label.place( relx = 0.2, rely = 0.25, anchor = CENTER)
		self.nu_lastname_entry = Entry( self.frame)
		self.nu_lastname_entry.place( relx = 0.55, rely = 0.25, anchor = CENTER)

		self.nu_username_label = Label( self.frame, text = "User Name")
		self.nu_username_label.place( relx = 0.2, rely = 0.3, anchor = CENTER)
		self.nu_username_entry = Entry( self.frame)
		self.nu_username_entry.place( relx = 0.55, rely = 0.3, anchor = CENTER)

		self.nu_email_label = Label( self.frame, text = "Email Id")
		self.nu_email_label.place( relx = 0.2, rely = 0.35, anchor = CENTER)
		self.nu_email_entry = Entry( self.frame)
		self.nu_email_entry.place( relx = 0.55, rely = 0.35, anchor = CENTER)

		self.nu_password_label = Label( self.frame, text = "Password")
		self.nu_password_label.place( relx = 0.2, rely = 0.4, anchor = CENTER)
		self.nu_password_entry = Entry( self.frame, show = "*")
		self.nu_password_entry.place( relx = 0.55, rely = 0.4, anchor = CENTER)

		self.nu_password_confirm_label = Label( self.frame, text = "Confirm Password")
		self.nu_password_confirm_label.place( relx = 0.2, rely = 0.45, anchor = CENTER)
		self.nu_password_confirm_entry = Entry( self.frame, show = "*")
		self.nu_password_confirm_entry.place( relx = 0.55, rely = 0.45, anchor = CENTER)

		self.nu_create_button = Button( self.frame, text = "Create Account", command = self.create_user_pressed )
		self.nu_create_button.place( relx = 0.55, rely = 0.5, anchor = CENTER)

		self.nu_back_button = Button( self.frame, text = "Go Back", command = self.go_back )
		self.nu_back_button.place( relx = 0.55, rely = 0.55, anchor = CENTER)

	# def check_pass_regex(self):


	def create_user_pressed(self):

		self.new_user_id = self.nu_username_entry.get()
		self.new_user_pwd = self.nu_password_entry.get()
		firstName = self.nu_firstname_entry.get()
		lastName = self.nu_lastname_entry.get()
		self.email = self.nu_email_entry.get()

		if self.new_user_id == "" or self.new_user_pwd == "" or self.nu_firstname_entry.get() == "" or self.nu_lastname_entry.get() == "":
			messagebox.showinfo("Error", "Fields cannot be empty")
			return
		rmatch = re.compile(self.pass_regex)
		ematch = re.compile(self.email_regex)


		if rmatch.match(self.new_user_pwd) == None:
			messagebox.showinfo("Error", "Passwords must include at least one numeric digit, Length 4-15")
			return

		if ematch.match(self.email) == None:
			messagebox.showinfo("Error", "Invalid Email ID")
			return

		if self.nu_password_confirm_entry.get() == self.new_user_pwd:
			self.root.load_login_page()
		else:
			messagebox.showinfo("Error", "Passwords don't match")
			return

		try:
			print("0ne")
			r = requests.post("http://127.0.0.1:5000/signup", data=json.dumps({'username': self.new_user_id,
			'password': self.new_user_pwd, 'nameFirst': firstName, 'nameLast': lastName, 'email': self.email}))
			print("two")
			if r.status_code == 200:
				print("three")
				self.go_back()
				# messagebox.showinfo("Success", "User creation success !")
			else:
				print("four")
				messagebox.showinfo("Error", "User creation failed !")
		except:
			messagebox.showinfo("Error", "Unabble to connect to internet")

	def go_back(self):
		self.frame.destroy()
		self.root.load_login_page()
