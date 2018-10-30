#!/usr/bin/python
import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, CENTER, Entry, Button

from backend.Models import db, User
from backend.login import login_email, login_username, create_user


class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.login_frame = Frame(self)
        self.login_frame.pack()
        self.load_login_page(False)

    def load_login_page(self, should_delete):

        if should_delete:
            self.destroy_newuser_page()

        self.username_label = Label(self, text="User Name :")
        self.username_label.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.username_entry = Entry(self)
        self.username_entry.place(relx=0.55, rely=0.3, anchor=CENTER)

        self.password_label = Label(self, text="Password :")
        self.password_label.place(relx=0.3, rely=0.4, anchor=CENTER)
        self.password_entry = Entry(self, show="*")
        self.password_entry.place(relx=0.55, rely=0.4, anchor=CENTER)

        self.login_button = Button(
            self, text="Login", command=self.login_button_pressed)
        self.login_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.newuser_button = Button(
            self, text="New User", command=self.newuser_button_pressed)
        self.newuser_button.place(relx=0.5, rely=0.57, anchor=CENTER)

    def destroy_login_page(self):
        self.username_label.destroy()
        self.password_label.destroy()
        self.username_entry.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()
        self.newuser_button.destroy()

    def destroy_newuser_page(self):
        self.nu_username_label.destroy()
        self.nu_password_label.destroy()
        self.nu_password_confirm_label.destroy()
        self.nu_username_entry.destroy()
        self.nu_password_entry.destroy()
        self.nu_password_confirm_entry.destroy()
        self.nu_create_button.destroy()
        self.nu_cancel_button.destroy()

    def load_newuser_page(self):

        self.destroy_login_page()

        self.nu_username_label = Label(self, text="Email Id")
        self.nu_username_label.place(relx=0.2, rely=0.3, anchor=CENTER)
        self.nu_username_entry = Entry(self)
        self.nu_username_entry.place(relx=0.55, rely=0.3, anchor=CENTER)

        self.nu_password_label = Label(self, text="Password")
        self.nu_password_label.place(relx=0.2, rely=0.4, anchor=CENTER)
        self.nu_password_entry = Entry(self, show="*")
        self.nu_password_entry.place(relx=0.55, rely=0.4, anchor=CENTER)

        self.nu_password_confirm_label = Label(self, text="Confirm Password")
        self.nu_password_confirm_label.place(relx=0.2, rely=0.5, anchor=CENTER)
        self.nu_password_confirm_entry = Entry(self, show="*")
        self.nu_password_confirm_entry.place(
            relx=0.55, rely=0.5, anchor=CENTER)

        self.nu_create_button = Button(
            self, text="Create Account", command=self.create_user_pressed)
        self.nu_create_button.place(relx=0.55, rely=0.6, anchor=CENTER)
        self.nu_cancel_button = Button(
            self, text="Cancel", command=self.cancel_create_user_pressed)
        self.nu_cancel_button.place(relx=0.55, rely=0.7, anchor=CENTER)

    def load_dashboard_page(self, user):
        self.destroy_login_page()

        self.dashboard_title_label = Label(
            self, text="Meeting Scheduler User Dashboard", font='Helvetica -16 bold')
        self.dashboard_title_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.dashboard_greeting_label = Label(
            self, text="Hi, " + user.username + "!")
        self.dashboard_greeting_label.place(relx=0.5, rely=0.6, anchor=CENTER)

    def login_button_pressed(self):
        self.user_id = self.username_entry.get()
        self.pwd = self.password_entry.get()

        result = login_username(self.user_id, self.pwd)

        if result:
            user = User.query.filter_by(username=self.user_id).first()
            self.load_dashboard_page(user)
        else:
            messagebox.showinfo(
                "Error", "Please check your username and password.")

    def newuser_button_pressed(self):
        self.load_newuser_page()

    def create_user_pressed(self):
        username = self.nu_username_entry.get()
        password = self.nu_password_entry.get()
        password_confirm = self.nu_password_confirm_entry.get()

        if username == "" or password == "" or password_confirm == "":
            messagebox.showinfo("Error", "Please fill all fields.")
        elif password != password_confirm:
            messagebox.showinfo("Error", "Passwords don't match")
        else:
            user = User.query.filter_by(email=username).first()
            if user:
                messagebox.showinfo("Error", "Enter a different email.")
            else:
                create_user(username, password)
                self.load_login_page(True)

    def cancel_create_user_pressed(self):
        self.load_login_page("True")

    def get_user_credentials(self):
        return self.user_id, self.pwd

    def get_new_user_credentials(self):
        return self.new_user_id, self.new_user_pwd


app = SampleApp()
app.geometry("600x400")
app.title("Meeting Scheduler")
app.mainloop()
