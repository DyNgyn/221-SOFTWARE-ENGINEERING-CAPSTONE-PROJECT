from flask import Flask, render_template, request, session,redirect,url_for, jsonify, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from random import randint
from datetime import timedelta
import os
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '7a9097f3b37240fe8dbc99bc'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
app.config["UPLOAD_PATH"] = app.root_path + "/static/img/upload/"
client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
webmaster = db["Webmaster"]
content = db["Content"]


from user import routes

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap


@app.route('/')
@app.route('/home')
def home_page():
    all_data = content.find({})
    return render_template("homepage.html",info = all_data)

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/member')
def member_page():
    return render_template("about.html")

@login_required
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
        image = request.files.get("image",None)
        print(app.root_path)
        if image:
            image.save(os.path.join(app.config["UPLOAD_PATH"], image.filename))
        
        if (pid!="0"):
            content.update_one({"id":pid},{"$set":{"Header": header, "Link": link, "Description": description,"Img": "1"}})
            message = f"Update Project {header} Succesfully"
            return render_template("cms.html",info = content.find_one({"id": pid}),message=message)
    return render_template("cms.html",info = project_document,message=message)




