from flask import Flask,jsonify,request,session,redirect
import hashlib
from app import db

class User:
    def start_session(self, user):
        del user['h_password']
        session['logged_in'] = True
        session['user'] = user
        return user, 200

    def signup(self):

        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if not (username and email and password1 and password2):
            return "Please fill in the form", 400
        user = {
            "username"  : username,
            "email" : email,
            "h_password" : password1,
        }

        
        if db["Webmaster"].find_one({ "email": user['email'] }):
            return "Email address already in use", 400

        if db["Webmaster"].find_one({ "username": user['username'] }):
            return "Username address already in use", 400
        
        if (len(password1)<8):
            return "Password is too short", 400
        
        if (password1 != password2):
            return "Password didn't match", 400
        
        user['h_password'] = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        db["Webmaster"].insert_one(user)
        return "Signup Successfully",200
    
    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        username = request.form.get('username')
        password = request.form.get('password')
        h_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = db["Webmaster"].find_one({"username": username, "h_password":h_password},{"_id":0,"username":1, "h_password":1})

        if user:
            return self.start_session(user)
        
        return "Invalid login credentials", 401