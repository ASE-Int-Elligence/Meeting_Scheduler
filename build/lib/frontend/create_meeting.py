#!/usr/bin/python
from tkinter import *
from tkinter import ttk, Canvas
import tkinter as tk
from tkinter import messagebox
import tkinter
import requests
import json
from tkinter.scrolledtext import ScrolledText
import webbrowser
# from CalendarDialog import *
import re
import datetime

class Create_meeting(object):


	__groupname = None
	__groupid = None
	__parent = None
	date_label_entry = None
	meeting_label_entry = None
	meet_dict = {}
	start_time = None
	end_time = None
	meetingName = None
	date_regex = "^(?:(?:31(/|-|.)(?:0?[13578]|1[02]))1|(?:(?:29|30)(/|-|.)(?:0?[1,3-9]|1[0-2])2))(?:(?:1[6-9]|[2-9]d)?d{2})$|^(?:29(/|-|.)0?23(?:(?:(?:1[6-9]|[2-9]d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1d|2[0-8])(/|-|.)(?:(?:0?[1-9])|(?:1[0-2]))4(?:(?:1[6-9]|[2-9]d)?d{2})$"
	date_regex = "^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$"

	@staticmethod
	def selectDate( parent ):
		cd = CalendarDialog(parent)
		# result = cd.result
		# selected_date = tkinter.StringVar()
		# selected_date.set(result.strftime("%m/%d/%Y"))
		# return selected_date.get()


	@staticmethod
	
	def setDate( parent ):
		pass
		# date = Create_meeting.selectDate( parent )
		# Create_meeting.date_label_entry.config(text = date)
		# print(date)

	@staticmethod
	def selectLocaton( parent):
		pass

	@staticmethod
	def create():

		Create_meeting.meet_dict = {'groupID' : Create_meeting.groupid , "meetingname":Create_meeting.meeting_label_entry.get() ,
		"starttime": Create_meeting.hour_var.get()+":"+Create_meeting.min_var.get(), "endtime": Create_meeting.to_hour_var.get()+":"+Create_meeting.to_min_var.get(),
		 "meetingdate" : Create_meeting.date_label_entry.get(), "lat" : Create_meeting.addr['lat'],
		 "lng" : Create_meeting.addr["lng"], "meetingLoc" : Create_meeting.addr["mapaddress"] }


		try:
			print ("In the end, it doesnt even")
			r = requests.post("http://127.0.0.1:5000/create_meeting", data=json.dumps(Create_meeting.meet_dict))
			if r.status_code == 200:
				potential_users = json.loads(r.content)
				Create_meeting.confirm.destroy()
				Create_meeting.top.destroy()
				Create_meeting.__parent.get_meetings_page()
			else:
				messagebox.showinfo("Error", "No Response about groups !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")



	@staticmethod
	def closetop():
		Create_meeting.confirm.destroy()

	@staticmethod
	def confirm_popup():

		if Create_meeting.meeting_label_entry.get() == "":
			messagebox.showinfo("Error", "Meeting Title cannot be empty")
			return

		try:
			datetime.datetime.strptime(Create_meeting.date_label_entry.get(),"%d/%m/%Y")
		except ValueError as err:
			messagebox.showinfo("Error", "Invalid date entered")
			return

		try:
			r = requests.post("http://127.0.0.1:5000/get_address")
			if r.status_code == 200:
				Create_meeting.addr = {}#json.loads(r.content)
				Create_meeting.addr = json.loads(r.content)
				
			else:
				messagebox.showinfo("Error", "No Response about groups !")
		except:
			messagebox.showinfo("Error", "Not Connected to Internet !")

		Create_meeting.confirm = Toplevel()
		Create_meeting.confirm.title("Confirm Location")
		Create_meeting.confirm.geometry("300x300")
		label = Label(Create_meeting.confirm, text = "Location set for meeting is \n" + str(Create_meeting.addr['mapaddress']))
		label.place(relx = 0.2, rely = 0.3, anchor = W)
		yes_but = Button(Create_meeting.confirm, text = "Yes", command = Create_meeting.create)
		yes_but.place(relx = 0.4, rely = 0.8)
		no_but = Button(Create_meeting.confirm, text = "No", command = Create_meeting.closetop)
		no_but.place(relx = 0.6, rely = 0.8)

	@staticmethod
	def setLocation():
		webbrowser.open("file:///C:/Users/Srujan/Desktop/ase_maps_new.html")

	@staticmethod
	def meeting_tab(groupid, parent):
		# op = arg.split('/')
		print("group id", groupid)
		# __groupname = op[0]
		Create_meeting.__groupid = groupid
		Create_meeting.__parent = parent
		Create_meeting.groupid = groupid

		Create_meeting.top = Toplevel()
		Create_meeting.top.title("Meeting for ")
		Create_meeting.top.geometry("400x400")
		# Create_meeting.selectDate(parent)

		meeting_label = Label(Create_meeting.top, text = "Title : " )
		meeting_label.place(relx = 0.25, rely = 0.2, anchor = CENTER)

		Create_meeting.meeting_label_entry = Entry(Create_meeting.top)
		Create_meeting.meeting_label_entry.place(relx = 0.55, rely = 0.2, anchor = CENTER)

		# group_label = Label(top, text = "Group Name : " )
		# group_label.place(relx = 0.25, rely = 0.3, anchor = CENTER)
		#
		# group_label_entry = Label(top, text = groupname )
		# group_label_entry.place(relx = 0.55, rely = 0.3, anchor = CENTER)

		date_label = Label(Create_meeting.top, text = "Date (dd/mm/yyyy) : " )
		date_label.place(relx = 0.2, rely = 0.4, anchor = CENTER)

		Create_meeting.date_label_entry = Entry(Create_meeting.top )
		Create_meeting.date_label_entry.place(relx = 0.6, rely = 0.4, anchor = CENTER)

		# date_button = Button(Create_meeting.top, text = "Select date", command = lambda p = parent : Create_meeting.setDate(parent.root))
		# date_button.place(relx = 0.8, rely = 0.4, anchor = CENTER)

		location_label = Label(Create_meeting.top, text = "Location : " )
		location_label.place(relx = 0.25, rely = 0.5, anchor = CENTER)

		location_button = Button(Create_meeting.top, text = "Select Location" , command = Create_meeting.setLocation)
		location_button.place(relx = 0.55, rely = 0.5, anchor = CENTER)

		time_from_label = Label(Create_meeting.top, text = "Time From : " )
		time_from_label.place(relx = 0.25, rely = 0.6, anchor = CENTER)

		Create_meeting.hour_var = StringVar(Create_meeting.top)
		Create_meeting.hour_var.set("00")
		Create_meeting.min_var = StringVar(Create_meeting.top)
		Create_meeting.min_var.set("00")
		from_hour = OptionMenu(Create_meeting.top, Create_meeting.hour_var, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 23)
		from_hour.place(relx = 0.55, rely = 0.6, anchor = CENTER)

		from_min = OptionMenu(Create_meeting.top, Create_meeting.min_var, 0, 15, 30, 45)
		from_min.place(relx = 0.8, rely = 0.6, anchor = CENTER)

		time_to_label = Label(Create_meeting.top, text = "Time to : " )
		time_to_label.place(relx = 0.25, rely = 0.7, anchor = CENTER)

		Create_meeting.to_hour_var = StringVar(Create_meeting.top)
		Create_meeting.to_hour_var.set("00")
		Create_meeting.to_min_var = StringVar(Create_meeting.top)
		Create_meeting.to_min_var.set("00")
		to_hour = OptionMenu(Create_meeting.top, Create_meeting.to_hour_var, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 23)
		to_hour.place(relx = 0.55, rely = 0.7, anchor = CENTER)

		to_min = OptionMenu(Create_meeting.top, Create_meeting.to_min_var, 0, 15, 30, 45)
		to_min.place(relx = 0.8, rely = 0.7, anchor = CENTER)

		create_button = Button(Create_meeting.top, text = "Create Meeting" , command = Create_meeting.confirm_popup)
		create_button.place(relx = 0.5, rely = 0.85, anchor = CENTER)
