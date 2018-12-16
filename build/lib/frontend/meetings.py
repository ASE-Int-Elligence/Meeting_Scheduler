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

class Meetings(object):

    def __init__(self, kinter, root):
        self.frame = kinter
        self.root = root

    def showLocation(self, key):
        pass

    def add_todo_entry(self, key):

        text = self.todo_entry.get()
        self.text_fields.append(text)
        var = IntVar()
        self.check_vars.append(var)
        check_button = Checkbutton(self.top, text = self.text_fields[-1], variable = self.check_vars[-1])
        check_button.place( relx = 0.2, rely = self.todo_num , anchor = W)
        self.check_buttons.append(check_button)
        self.todo_num += 0.1
        try:
            print("kjhkjsdfhdsjkknfjkdjfk")
            r = requests.post("http://127.0.0.1:5000/create_todoitem", data = json.dumps({'meeting_id': self.meetings_info[key]["meetingID"],
            "checked" : var.get(), "iteminfo" : self.text_fields[-1] }))
            print("jkhsfkjsdfhjk")
            if r.status_code == 200:
                self.item_ids.append(r.content)
            else:
                messagebox.showinfo("Error", "Unable to add to-do entry")
        except:
            messagebox.showinfo("Error", "Connection issues while creating to-do")

    def save_todo(self, key):
        req = {}
        for i in range( len(self.text_fields) ):
            req[ int(self.item_ids[i]) ] = {"meeting_id" : self.meetings_info[key]["meetingID"], "checked" :self.check_vars[i].get(),
             "iteminfo" : self.text_fields[i]}
        try:
            print(req)
            r = requests.post("http://127.0.0.1:5000/save_todoitem", data = json.dumps(req))
            if r.status_code == 200:
                # self.item_ids.append(r.content)
                pass
            else:
                messagebox.showinfo("Error", "Unable to save to-do list")
        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Error while trying to save to-do list")

    def readtodo(self):
        todo = []

        for i in range(len(self.text_fields)):
            todo.append([self.text_fields[i], self.check_vars[i].get()])
            print(todo[i])
        return todo

    def addtodos(self, res):
        for i in res:
            text = i["iteminfo"]
            self.text_fields.append(text)
            var = IntVar()
            if i["checked"] == "YES":
                i["checked"] = 1
            else:
                i["checked"] = 0
            var.set(i["checked"])
            self.check_vars.append(var)
            check_button = Checkbutton(self.top, text = self.text_fields[-1], variable = self.check_vars[-1])
            check_button.place( relx = 0.2, rely = self.todo_num , anchor = W)
            self.check_buttons.append(check_button)
            self.todo_num += 0.05


    def createtodo(self, key):
        self.top = Toplevel()
        self.todo_num = 0.1
        self.check_buttons = []
        self.check_vars = []
        self.text_fields = []
        self.item_ids = []

        try:
            # print(req)
            r = requests.post("http://127.0.0.1:5000/get_todoitem", data = json.dumps({"meeting_id" : self.meetings_info[key]["meetingID"]}))
            if r.status_code == 200:
                res = json.loads(r.content)
                self.addtodos(res)
            else:
                messagebox.showinfo("Error", "Unable to save to-do list")
        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Error while trying to save to-do list")

        self.top.title("Todo List ")
        self.top.geometry("600x600")
        self.todo_entry = Entry(self.top)
        self.todo_entry.place(relx = 0.5, rely = 0.85, anchor = CENTER)
        todo_button = Button(self.top, text = "Add to-do entry", command = lambda p = key : self.add_todo_entry(p))
        todo_button.place(relx = 0.8, rely = 0.85, anchor = CENTER)
        save_todo = Button(self.top, text = "Save todo", command = lambda p = key : self.save_todo(p))
        save_todo.place(relx = 0.6, rely = 0.9, anchor = CENTER)

    def checkIn(self, key):
        try:
            r = requests.post("http://127.0.0.1:5000/render_location", data=json.dumps({'lat': self.meetings_info[key]["lat"],
            "lng" : self.meetings_info[key]["lng"]}))
            print(r.status_code)
            #if r.status_code == 200:
                # print("meetings", r.content)
                # self.meetings_info = json.loads(r.content)
            print(r)
            print("SOJHoSDAD",r.content)
            webbrowser.open(r)
            #else:
            #messagebox.showinfo("Error", "display meetings retuned error")
        except Exception as e:
            print (e)
            messagebox.showinfo("Error", "Error while displaying meetings")

    def load_page(self):
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        self.meetings_info = {}
        self.label_frames = []
        print("username meetings", self.root.userid)
        try:
            r = requests.post("http://127.0.0.1:5000/display_meetings", data=json.dumps({'username': self.root.userid}))
            if r.status_code == 200:
                print("meetings", r.content)
                self.meetings_info = json.loads(r.content)
            else:
                messagebox.showinfo("Error", "display meetings retuned error")
        except:
            messagebox.showinfo("Error", "Error while displaying meetings")

        for key in self.meetings_info.keys():
            meeting_info = self.meetings_info[ key ]
            labelframe = LabelFrame( self.frame, text = "Title : "+meeting_info['meetingname'] )
            labelframe.pack( fill = "both",expand = "yes")
            self.label_frames.append( labelframe)
            left = Label( self.label_frames[-1], width = 50, text = "From Time : "+meeting_info["starttime"] )
            left.place( relx = 0.5, rely = 0.25, anchor = CENTER)
            left = Label( self.label_frames[-1], width = 50, text = "To Time : "+meeting_info["endtime"] )
            left.place( relx = 0.5, rely = 0.3, anchor = CENTER)
            loc_button = Label(labelframe, text = meeting_info["meetingLoc"])
            loc_button.place(relx = 0.5, rely = 0.4, anchor = CENTER)
            loc_button = Button(labelframe, text = "Check-In", command = lambda p = key : self.checkIn(key))
            loc_button.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            todo_button = Button(labelframe, text = "Show to-do list", command = lambda p = key : self.createtodo(key))
            todo_button.place(relx = 0.5, rely = 0.6, anchor = CENTER)
