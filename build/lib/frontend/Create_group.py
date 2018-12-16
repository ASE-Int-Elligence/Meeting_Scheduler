#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json
from tkinter.scrolledtext import ScrolledText

class Create_group(object):

	def __init__(self, root, parent):
		self.users = []
		self.root = root
		self.parent = parent

	def clear_frame(self, frame):
		for widget in frame.winfo_children():
			widget.destroy()

	def get_popup_selection(self):
		try:
			self.listbox_selection = self.lb.get(self.lb.curselection())
			# print(self.listbox_selection)
			self.users.append(self.listbox_selection)
			# print(set(self.users))
			self.popup.destroy()
		except:
			messagebox.showinfo("Error", "Select an user")

	def create_popup(self):
		self.popup = tk.Toplevel(self.frame)
		self.scrollbar = Scrollbar(self.popup)
		self.scrollbar.pack( side = RIGHT, fill = Y )
		partial_name = self.user_name_entry.get()
		self.popup.title("Users")
		potential_users = {0:"John Does", 1:"John Doesnt"}
		try:
			r = requests.post("http://127.0.0.1:5000/search_user", data=json.dumps({'username': partial_name}))
			if r.status_code == 200:
				potential_users = json.loads(r.content)
			else:
				messagebox.showinfo("Error", "No Response about groups !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")

		self.lb = Listbox(self.popup)

		for key in potential_users.keys():
			self.lb.insert(key, potential_users[key])

		self.lb.pack()
		self.select_user = Button(self.popup, text = "Add User", command = self.get_popup_selection)
		self.select_user.place( relx = 0.5, rely = 0.9, anchor = CENTER)
		self.popup.mainloop()

	def set_group_type(self):
		if self.var.get() == 1:
			self.group_type = "formal"
		else:
			self.group_type = "informal"

	def final_create_group(self):
		try:
			self.users.append(self.root.userid)
			r = requests.post("http://127.0.0.1:5000/create_group", data=json.dumps( { 'users': list(self.users),
				'admin': self.root.userid, "groupName": self.group_name_entry.get(), "groupType": self.group_type}))
			if r.status_code == 200:
				pass
			else:
				messagebox.showinfo("Error", "Wasn't able to create group")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")
		self.parent.load_groups_info()

	def go_back(self):

		self.parent.load_groups_info()
		
	def create_group( self, frame):
		self.frame = frame
		# self.(self.frame)

		self.var = IntVar()

		self.group_name_label = Label(self.frame, text = "Group Name :")
		self.group_name_label.place( relx = 0.3, rely = 0.3, anchor = CENTER)

		self.group_name_entry = Entry(self.frame)
		self.group_name_entry.place( relx = 0.6, rely = 0.3, anchor = CENTER)

		self.group_type_label = Label(self.frame, text = "Group Type :")
		self.group_type_label.place( relx = 0.3, rely = 0.4, anchor = CENTER)

		self.r1 = Radiobutton(self.frame, text="Formal", variable = self.var, value = 1, command = self.set_group_type)
		self.r1.place( relx = 0.495, rely = 0.4, anchor = CENTER)

		self.r2 = Radiobutton(self.frame, text="Informal", variable = self.var, value = 2, command = self.set_group_type)
		self.r2.place( relx = 0.5, rely = 0.45, anchor = CENTER)

		self.user_name_entry = Entry(self.frame, width = 20)
		self.user_name_entry.place( relx = 0.4, rely = 0.55, anchor = CENTER)

		self.add_user = Button(self.frame, text = "Find User", command = self.create_popup)
		self.add_user.place( relx = 0.65, rely = 0.55, anchor = CENTER)

		self.add_group = Button(self.frame, text = "Create Group", command = self.final_create_group)
		self.add_group.place( relx = 0.65, rely = 0.65, anchor = CENTER)

		self.add_group = Button(self.frame, text = "Back", command = self.go_back)
		self.add_group.place( relx = 0.4, rely = 0.65, anchor = CENTER)
