#!/usr/bin/python
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import requests


class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.login_frame = Frame(self)
        self.login_frame.pack()
        self.login_page_active = False
        self.newuser_page_active = False
        self.load_login_page()
        

    def destroy_login_page(self):
        self.username_label.destroy()
        self.password_label.destroy()
        self.username_entry.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()
        self.newuser_button.destroy()

    def destroy_newuser_page(self):
        self.nu_firstname_label.destroy()
        self.nu_firstname_entry.destroy()
        self.nu_lastname_label.destroy()
        self.nu_lastname_entry.destroy()
        self.nu_username_label.destroy()
        self.nu_password_label.destroy()
        self.nu_username_entry.destroy()
        self.nu_password_entry.destroy()
        self.nu_password_confirm_entry.destroy()
        self.nu_password_confirm_label.destroy()
        self.nu_create_button.destroy()
        self.nu_email_label.destroy()
        self.nu_email_entry.destroy()


    def load_login_page(self):

        if self.login_page_active == True:
            self.destroy_login_page()

        if self.newuser_page_active == True:
            self.destroy_newuser_page()

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
        self.login_page_active = True

    def load_newuser_page(self):

        if self.login_page_active == True:
            self.destroy_login_page()

        if self.newuser_page_active == True:
            self.destroy_newuser_page()

        self.nu_firstname_label = Label( self, text = "First Name")
        self.nu_firstname_label.place( relx = 0.2, rely = 0.2, anchor = CENTER)
        self.nu_firstname_entry = Entry( self)
        self.nu_firstname_entry.place( relx = 0.55, rely = 0.2, anchor = CENTER)

        self.nu_lastname_label = Label( self, text = "Last Name")
        self.nu_lastname_label.place( relx = 0.2, rely = 0.3, anchor = CENTER)
        self.nu_lastname_entry = Entry( self)
        self.nu_lastname_entry.place( relx = 0.55, rely = 0.3, anchor = CENTER)

        self.nu_username_label = Label( self, text = "User Name")
        self.nu_username_label.place( relx = 0.2, rely = 0.4, anchor = CENTER)
        self.nu_username_entry = Entry( self)
        self.nu_username_entry.place( relx = 0.55, rely = 0.4, anchor = CENTER)

        self.nu_email_label = Label( self, text = "Email Id")
        self.nu_email_label.place( relx = 0.2, rely = 0.5, anchor = CENTER)
        self.nu_email_entry = Entry( self)
        self.nu_email_entry.place( relx = 0.55, rely = 0.5, anchor = CENTER)

        self.nu_password_label = Label( self, text = "Password")
        self.nu_password_label.place( relx = 0.2, rely = 0.6, anchor = CENTER)
        self.nu_password_entry = Entry( self, show = "*")
        self.nu_password_entry.place( relx = 0.55, rely = 0.6, anchor = CENTER)

        self.nu_password_confirm_label = Label( self, text = "Confirm Password")
        self.nu_password_confirm_label.place( relx = 0.2, rely = 0.7, anchor = CENTER)
        self.nu_password_confirm_entry = Entry( self, show = "*")
        self.nu_password_confirm_entry.place( relx = 0.55, rely = 0.7, anchor = CENTER)

        self.nu_create_button = Button( self, text = "Create Account", command = self.create_user_pressed )
        self.nu_create_button.place( relx = 0.55, rely = 0.8, anchor = CENTER)

        self.newuser_page_active = True

    def login_button_pressed(self):
        self.user_id = self.username_entry.get()
        self.pwd = self.password_entry.get()
        if self.user_id == "" or self.pwd == "":
            messagebox.showinfo("Error", "Fields cannot be empty")
        # do login code here, check if login works or not
        r = requests.post("http://localhost/login", data={'username': self.user_id, 'password': self.pwd})
        
        if True:
            load_homepage()
        else:
            messagebox.showinfo("Error", "Wrong Credentials !")

    def newuser_button_pressed(self):
        self.load_newuser_page()

    def create_user_pressed(self):

        self.new_user_id = self.nu_username_entry.get()
        self.new_user_pwd = self.nu_password_entry.get()
        firstName = self.nu_firstname_entry.get()
        lastName = self.nu_lastname_entry.get()
        email = self.nu_email_entry.get()
            
        if self.new_user_id == "" or self.new_user_pwd == "" or self.nu_firstname_entry.get() == "" or self.nu_lastname_entry.get() == "":
            messagebox.showinfo("Error", "Fields cannot be empty")
            return

        if self.nu_password_confirm_entry.get() == self.new_user_pwd:
            self.load_login_page()
        else:
            messagebox.showinfo("Error", "Passwords don't match")
            return

        r = requests.post("http://localhost/signup", data={'username': self.new_user_id, 'password': self.new_user_pwd, 'nameFirst': firstName, 'nameLast': lastName, 'email': email})
        

    def get_user_credentials(self):
        return self.user_id, self.pwd

    def get_new_user_credentials(self):
        return self.new_user_id, self.new_user_pwd

    # def login_




app = SampleApp()
app.geometry("600x600")
app.title("Meeting Scheduler")
app.mainloop()