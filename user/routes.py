from flask import Flask, render_template, request,redirect
from app import app
from .models import User
@app.route('/signup',methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        msg,status = User().signup()
        print(msg)
        return render_template("cms.html")
    return render_template("register.html")

@app.route('/signout')
def logout_page():
    return User().signout()

@app.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        msg, status =  User().login()
        print(status)
        if (status != 200):
            return redirect('/')
       
    
    return render_template("login.html")
