from flask import Flask, render_template, request, session,redirect,url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from forms import SignUpForm
from random import randint
import hashlib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a9097f3b37240fe8dbc99bc'
client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
webmaster = db["Webmaster"]
content = db["Content"]
@app.route('/')
@app.route('/home')
def home_page():

    all_data = content.find({})
    return render_template("homepage.html",info = all_data)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        h_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        authenticate = webmaster.find_one({"username": username, "h_password": h_password})
        if authenticate:
            session['logged_in'] = True
            session['id'] = authenticate['adminID']
            session['username'] = authenticate['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('cms_page'))
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", message = msg)

@app.route('/register', methods =['GET', 'POST'])
def register_page():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        user_found = webmaster.find_one({"username": username})
        if user_found:
            msg = "This username has been used, please choose another username"
        elif not username or not password1 or not email or not password2:
            msg = 'Please fill out the form !'
        elif ("@gmail.com" not in email):
            msg = "Invalid Email Address"
        elif password1 != password2:
            msg = "Password not match"
        elif len(password1) < 8:
            msg = "Password too short"
        else:
            adminID = randint(10000000,99999999)
            h_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
            new_user = {"adminID": adminID, "h_password" : h_password, "password": password1, "username": username, "email": email}
            webmaster.insert_one(new_user)
            return redirect(url_for('login_page'))
        
    return render_template("register.html",message =msg)

@app.route('/logout')
def logout_page():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/member')
def member_page():
    return render_template("about.html")

@app.route('/cms', methods = ['GET', 'POST'])
@app.route('/cms/<pid>', methods = ['GET', 'POST'])
def cms_page(pid="1"):
    message =""
    project_id=str(pid)
    project_document = content.find_one({"id": pid})
    if request.method == "POST":
        header = request.form["header"]
        link = request.form["link"]
        description = request.form["description"]
        #image = request.files["image"]
        #if image:
        #    image.save(os.path.join(app.root_path, "static/uploads/", image.filename))
        #else:
        if (pid!="0"):
            content.update_one({"id":pid},{"$set":{"Header": header, "Link": link, "Description": description,"Img": "1"}})
            message = f"Update Project {header} Succesfully"
            return render_template("temp.html",info = content.find_one({"id": pid}),message=message)
    return render_template("temp.html",info = project_document,message=message)

