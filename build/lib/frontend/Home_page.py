#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json
from tkinter.scrolledtext import ScrolledText

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

	def load_groups_info(self):
		self.scrollbar = Scrollbar(self.groups)
		self.scrollbar.pack( side = RIGHT, fill = Y )
		self.nu_create_group = Button( self.groups, text = "Create Group", command = self.create_group )
		# self.nu_create_group.place( relx = 0.5, rely = 0.9, anchor = CENTER)
		self.nu_create_group.pack(side = BOTTOM)

		groups_info = {}
		label_frames = []

		try:
			r = requests.post("http://127.0.0.1:5000/display_groups", data=json.dumps({'username': self.root.userid}))
			print (r.status_code)
			if r.status_code == 200:
				groups_info = json.loads(r.content)
			else:
				messagebox.showinfo("Error", "No Response about groups !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")


		

		for key in groups_info.keys:

			group_info = groups_info[ key ]
			labelframe = LabelFrame( root, text="Group "+str(key))
			labelframe.pack( fill="both", expand="yes")
			label_frames.append( labelframe)
			 
			left = Label( label_frames[-1], text="Inside the LabelFrame")
			left.pack()


	def get_groups_page(self):
		
		self.load_groups_info()
		

	def clear_frame(self, frame):
		for widget in frame.winfo_children():
			widget.destroy()

	def create_popup(self):
		self.popup = tk.Toplevel(self.root)
		partial_name = self.user_name_entry.get()

		# self.lb = 
		

		self.popup.mainloop()

	def set_group_type(self):
		if self.var.get() == 1:
			self.group_type = "formal"
		else:
			self.group_type = "informal"

		print(self.group_type)

	def create_group(self):
		self.clear_frame(self.groups)

		self.var = IntVar()

		self.group_name_label = Label(self.groups, text = "Group Name :")
		self.group_name_label.place( relx = 0.3, rely = 0.3, anchor = CENTER)

		self.group_name_entry = Entry(self.groups)
		self.group_name_entry.place( relx = 0.6, rely = 0.3, anchor = CENTER)

		self.group_type_label = Label(self.groups, text = "Group Type :")
		self.group_type_label.place( relx = 0.3, rely = 0.4, anchor = CENTER)

		self.r1 = Radiobutton(self.groups, text="Formal", variable = self.var, value = 1, command = self.set_group_type)
		self.r1.place( relx = 0.495, rely = 0.4, anchor = CENTER)

		self.r2 = Radiobutton(self.groups, text="Informal", variable = self.var, value = 2, command = self.set_group_type)
		self.r2.place( relx = 0.5, rely = 0.45, anchor = CENTER)

		self.user_name_entry = Entry(self.groups, width = 20)
		self.user_name_entry.place( relx = 0.4, rely = 0.55, anchor = CENTER)

		self.add_user = Button(self.groups, text = "Find User", command = self.create_popup)
		self.add_user.place( relx = 0.65, rely = 0.55, anchor = CENTER)
		
