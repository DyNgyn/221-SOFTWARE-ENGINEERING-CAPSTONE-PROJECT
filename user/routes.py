from flask import Flask, render_template, request,redirect, flash
from app import app
from .models import User
from time import sleep
@app.route('/register',methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        msg,status = User().signup()
        if (status != 200):
            flash(msg)
        else:
            return redirect("/login")
    return render_template("register.html")

@app.route('/signout')
def logout_page():
    return User().signout()

@app.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        status =  User().login()
        print(status[1])
        return redirect('/')
       
    
    return render_template("login.html")

