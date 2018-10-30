from flask import Flask, render_template, flash, redirect, url_for, request, Response
from __init__ import app

app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def home():
	return Response("Hello World!")

if __name__ == '__main__':
	app.run(host='0.0.0.0')