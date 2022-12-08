from flask import Flask,jsonify,request,session,redirect
import hashlib
from app import db

class User:
    def start_session(self, user):
        del user['h_password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')
        
        user = {
            "username"  : username,
            "email" : email,
            "h_password" : password1,
        }

        user['h_password'] = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        
        if db["Webmaster"].find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400

        if db["Webmaster"].find_one({ "username": user['username'] }):
            return jsonify({ "error": "Username address already in use" }), 400
        
        ## Add password verification
        
        if db["Webmaster"].insert_one(user):
            return self.start_session(user)
        
        return jsonify({ "error": "Signup failed" }),400
    
    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        username = request.form.get('username')
        password = request.form.get('password')
        user = db["Webmaster"].find_one({"username": username},{"_id":0,"username":1, "h_password":1})

        if user and hashlib.sha256(password.encode('utf-8')).hexdigest() == user["h_password"]:
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401