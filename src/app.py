#!/usr/bin/python
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox


class SampleApp(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)
		self.login_frame = Frame(self)
		self.login_frame.pack()
		self.load_login_page(False)


	def load_login_page(self, should_delete):

		if should_delete:
			self.nu_username_label.destroy()
			self.nu_password_label.destroy()
			self.nu_password_confirm_label.destroy()
			self.nu_username_entry.destroy()
			self.nu_password_entry.destroy()
			self.nu_password_confirm_entry.destroy()
			self.nu_create_button.destroy()


		self.username_label = Label( self, text = "User Name :")
		self.username_label.place( relx = 0.3, rely = 0.3, anchor = CENTER)
		self.username_entry = Entry( self)
		self.username_entry.place( relx = 0.55, rely = 0.3, anchor = CENTER)
		
		self.password_label = Label( self, text = "Password :")
		self.password_label.place( relx = 0.3, rely = 0.4, anchor = CENTER)	
		self.password_entry = Entry( self, show = "*")
		self.password_entry.place( relx = 0.55, rely = 0.4, anchor = CENTER)

		self.login_button = Button( self, text = "Login", command = self.login_button_pressed )
		self.login_button.place( relx = 0.5, rely = 0.5, anchor = CENTER)
		self.newuser_button = Button( self, text = "New User", command = self.newuser_button_pressed)
		self.newuser_button.place( relx = 0.5, rely = 0.57, anchor = CENTER)

	def load_newuser_page(self):

		self.username_label.destroy()
		self.password_label.destroy()
		self.username_entry.destroy()
		self.password_entry.destroy()
		self.login_button.destroy()
		self.newuser_button.destroy()

		self.nu_username_label = Label( self, text = "Email Id")
		self.nu_username_label.place( relx = 0.2, rely = 0.3, anchor = CENTER)
		self.nu_username_entry = Entry( self)
		self.nu_username_entry.place( relx = 0.55, rely = 0.3, anchor = CENTER)

		self.nu_password_label = Label( self, text = "Password")
		self.nu_password_label.place( relx = 0.2, rely = 0.4, anchor = CENTER)
		self.nu_password_entry = Entry( self, show = "*")
		self.nu_password_entry.place( relx = 0.55, rely = 0.4, anchor = CENTER)

		self.nu_password_confirm_label = Label( self, text = "Confirm Password")
		self.nu_password_confirm_label.place( relx = 0.2, rely = 0.5, anchor = CENTER)
		self.nu_password_confirm_entry = Entry( self, show = "*")
		self.nu_password_confirm_entry.place( relx = 0.55, rely = 0.5, anchor = CENTER)

		self.nu_create_button = Button( self, text = "Create Account", command = self.create_user_pressed )
		self.nu_create_button.place( relx = 0.55, rely = 0.6, anchor = CENTER)

	def login_button_pressed(self):
		self.user_id = self.username_entry.get()
		self.pwd = self.password_entry.get()

	def newuser_button_pressed(self):
		self.load_newuser_page()

	def create_user_pressed(self):
		if self.nu_password_confirm_entry.get() == self.nu_password_entry.get():
			self.new_user_id = self.nu_username_entry.get()
			self.new_user_pwd = self.nu_password_confirm_entry.get()
			self.load_login_page(True)
		else:
			messagebox.showinfo("Error", "Passwords don't match")

	def get_user_credentials(self):
		return self.user_id, self.pwd

	def get_new_user_credentials(self):
		return self.new_user_id, self.new_user_pwd




app = SampleApp()
app.geometry("600x400")
app.title("Meeting Scheduler")
app.mainloop()