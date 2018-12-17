#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import requests
import json
from tkinter.scrolledtext import ScrolledText
from Create_group import *
from create_meeting import *
from meetings import *
# from tkinter.tix import *

class Home_page(object):

	def __init__(self):
		self.frame = None
		self.newusers = []
		self.delusers = []

	def get_page(self, kinter):
		self.root = kinter
		self.groups = Frame( self.root.nb )
		# self.configureFrame()
		self.meetings = Frame( self.root.nb )
		self.logout = Frame( self.root.nb )
		self.root.nb.add( self.groups, text = 'Groups')
		self.root.nb.add( self.meetings, text = 'Meetings')
		self.root.nb.add( self.logout, text = 'Logout')
		self.root.nb.pack( expand = 1, fill = "both")
		self.get_groups_page()
		self.get_meetings_page()
		self.create_logout()

	def configureFrame(self):
		self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
		self.groups = tk.Frame(self.canvas, background="#ffffff")
		self.vsb = tk.Scrollbar(self.root.nb, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.groups, anchor="nw",
                                  tags="self.frame")
		self.groups.bind("<Configure>", self.onFrameConfigure)

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def create_group(self):
		self.clear_frame(self.groups)
		self.group = Create_group(self.root, self)
		self.group.create_group(self.groups)

	def logout_pressed(self):
		self.groups.destroy()
		self.meetings.destroy()
		self.logout.destroy()
		# self.root.nb.destroy()
		self.root.load_login_page()

	def create_logout(self):

		self.logout_button = Button( self.logout, text = "Logout", command = self.logout_pressed)
		self.logout_button.place( relx = 0.5, rely = 0.5, anchor = CENTER)

	def get_popup_selection(self):
		try:
			self.listbox_selection = self.lb.get(self.lb.curselection())
			self.newusers.append(self.listbox_selection)
			# print(self.newusers)
			self.popup.destroy()
		except:
			messagebox.showinfo("Error", "Select an user")

	def del_popup_selection(self):
		try:
			self.listbox_selection = self.lb.get(self.lb.curselection())
			self.delusers.append(self.listbox_selection)
			# print(self.newusers)
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
		self.select_user.place( relx = 0.5, rely = 0.75, anchor = CENTER)
		self.del_user = Button(self.popup, text = "Delete User", command = self.del_popup_selection)
		self.del_user.place( relx = 0.5, rely = 0.9, anchor = CENTER)
		self.popup.mainloop()

	def show_group_details(self, key):

		self.newusers = []
		self.delusers = []
		try:
			r = requests.post("http://127.0.0.1:5000/individual_groups", data=json.dumps({'groupID': self.groups_info[key]['groupID']}))
			if r.status_code == 200:
				self.ind_group_info = json.loads(r.content)
				print(self.ind_group_info)
			else:
				messagebox.showinfo("Error", "Individual groups returned error")
		except:
			messagebox.showinfo("Error", "Exception after individual groups")

		# self.ind_group_info = { '0' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23"},
		# 					 '1' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24"}}

		self.top = Toplevel()
		self.top.title("Group info "+self.groups_info[key]['groupName'])
		self.top.geometry("300x300")
		left = Label( self.top, width = 50, text = "Admin : "+self.groups_info[key]["admin"] )
		left.place( relx = 0.5, rely = 0.25, anchor = CENTER)

		user_names = ""

		for ind in self.ind_group_info.keys():
			user_names += self.ind_group_info[ind]['nameFirst']+" "+self.ind_group_info[ind]['nameLast']+", "

		left = Label( self.top, text = "Users : "+user_names[0:-2] )
		left.place( relx = 0.5, rely = 0.45, anchor = CENTER)

		left = Label( self.top, width = 50, text = "Group type : "+groups_info[key]["groupType"] )
		left.place( relx = 0.5, rely = 0.35, anchor = CENTER)
			

		print("Curr user", self.root.userid, "admin", self.groups_info[key]["admin"] )
		if self.root.userid == self.groups_info[key]["admin"]:
			self.user_name_entry = Entry(self.top, width = 20)
			self.user_name_entry.place( relx = 0.5, rely = 0.7, anchor = CENTER)

			add_user_button = Button(self.top, text="Search User", command = self.create_popup)
			add_user_button.place( relx = 0.8, rely = 0.7, anchor = CENTER)

			self.save_changes = Button(self.top, text = "Save Changes", command = lambda p = key: self.edit_group(p))
			self.save_changes.place( relx = 0.5, rely = 0.8, anchor = CENTER)

			self.create_meeting_buttons.append( Button( self.top, text = "Create Meeting",
					command = lambda arg = self.groups_info[key]["groupID"]: Create_meeting.meeting_tab( arg, self) ))
			self.create_meeting_buttons[-1].place( relx = 0.5, rely = 0.9, anchor = CENTER)

	def edit_group(self, key):

		old_users = []
		# for ind in self.ind_group_info.keys():
		# 	old_users.append(self.ind_group_info[ind]['username'])
		# print(old_users+self.newusers)
		try:
			r = requests.post("http://127.0.0.1:5000/add_more_users", data=json.dumps( { 'groupID' : self.groups_info[key]['groupID'], 'users': old_users+self.newusers,
				'admin': self.root.userid, "groupName": self.groups_info[key]["groupName"], "groupType": self.groups_info[key]["groupType"]}))
			if r.status_code == 200:
				self.load_groups_info()
				self.top.destroy()
			else:
				messagebox.showinfo("Error", "Wasn't able to add new users to group")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")

		try:
			r = requests.post("http://127.0.0.1:5000/delete_users_in_group", data=json.dumps( { 'groupID' : self.groups_info[key]['groupID'],
								'users': old_users+self.delusers}))
			if r.status_code == 200:
				pass
			else:
				messagebox.showinfo("Error", "Wasn't able to delete users to group")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")


	def load_groups_info(self):
		self.clear_frame(self.groups)
		self.scrollbar = Scrollbar(self.groups)
		self.scrollbar.pack( side = RIGHT, fill = Y )
		self.nu_create_group = Button( self.groups, text = "Create Group", command = self.create_group )
		self.nu_create_group.pack(side = BOTTOM)

		self.groups_info = {}
		self.label_frames = []
		self.group_name_buttons = []
		self.create_meeting_buttons = []
		self.group_info_status = []


		try:
			r = requests.post("http://127.0.0.1:5000/display_groups", data=json.dumps({'username': self.root.userid}))
			if r.status_code == 200:
				print(r.content)
				self.groups_info = json.loads(r.content)
			else:
				messagebox.showinfo("Error", "display groups retuned error")
		except:
			messagebox.showinfo("Error", "Error while displaying groups")

		self.groups_info = { '0' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '1' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '2' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '3' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '4' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '5' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '6' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '7' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '8' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '9' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '10' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '11' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '12' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"},
							 '13' : {'groupName' : "Guts", "groupType" : "Informal", "groupID": "24", "admin" : "2"},
							 '14' : {'groupName' : "Colons", "groupType" : "Formal", "groupID": "23", "admin" : "1"}
							 }

		for key in self.groups_info.keys():
			self.group_info_status.append(False)
			group_info = self.groups_info[ key ]
			labelframe = LabelFrame( self.groups, text = "Group "+str(int(key)+1) )
			labelframe.pack( fill = "both",expand = "yes")
			# labelframe.configure(height=labelframe["height"],width=labelframe["width"])
			# labelframe.grid_propagate(1)
			self.label_frames.append( labelframe)

			self.group_name_buttons.append(Button( self.label_frames[-1], width = 50, text = group_info["groupName"], command = lambda p = key: self.show_group_details(p) ))
			self.group_name_buttons[-1].place( relx = 0.5, rely = 0.2, anchor = CENTER)
			# left = Label( self.label_frames[-1], width = 50, text = "Admin : "+group_info["admin"] )
			# left.place( relx = 0.5, rely = 0.5, anchor = CENTER)
				# left = Label( self.label_frames[-1], text = "Users : "+user_names[0:-2] )
			# left.place( relx = 0.5, rely = 0.65, anchor = CENTER)

			
			# self.add_user_button =


	def get_groups_page(self):
		print("username groups", self.root.userid)
		self.load_groups_info()

	def get_meetings_page(self):
		self.meetings_obj = Meetings( self.meetings, self.root)
		self.meetings_obj.load_page()


	def clear_frame(self, frame):
		for widget in frame.winfo_children():
			widget.destroy()
