from flask import Flask, render_template, request, session,redirect, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import timedelta
import os
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a9097f3b37240fe8dbc99bc'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
app.config["UPLOAD_PATH"] = app.root_path + "/static/img/upload/"
client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
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

@app.context_processor
def utility_processor():
    number_of_project =content.count_documents({})
    return dict(number = number_of_project)

@app.route('/')
@app.route('/home')
def home_page():
    all_data = content.find({})
    return render_template("usr/homepage.html",info = all_data)

@app.route('/about')
def about_page():
    data = db["About"].find_one({})
    print(data["Intention"])
    data["Intention"] = data["Intention"].split('\r\n')
    print(data["Intention"])
    return render_template("usr/about.html", info=data)

@app.route('/project/<pid>', methods = ['GET'])
def project_page(pid):
    project_content = content.find_one({"id": pid})
    project_content["Description"] = project_content["Description"].split('\r\n')
    return render_template("usr/project.html", info= project_content)

@app.route('/cms', methods = ['GET', 'POST'])
@app.route('/cms/<pid>', methods = ['GET', 'POST'])
@login_required
def cms_page(pid="1"):
    project_id = str(pid)
    project_document = {"id":project_id,"Header": "", "Link": "", "Description":"","Summary":"","Img":""}
    if (project_id !="0"):
        project_document = content.find_one({"id": project_id})
    number_of_project =content.count_documents({})

    if request.method == "POST":
        header = request.form["header"]
        link = request.form["link"]
        summary = request.form["summary"]
        description = request.form["description"]
        action = request.form.get("submit",None)
        if not action:
            return delete_web()
        else:
            image = request.files.get("image",None)
            filename = project_document["Img"]
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["UPLOAD_PATH"], filename))
            if (pid != "0"):
                content.update_one({"id":project_id},{"$set":{"Header": header, "Link": link, "Description": description,"Summary": summary, "Img": filename}})
                flash(f"Update Project {header} Succesfully")
            else:
                project_id = str(number_of_project+1)
                content.insert_one({"id":project_id,"Header": header, "Link": link, "Description": description,"Summary": summary,"Img": filename})
                flash(f"Insert Project {header} Succesfully")
            return render_template("webmaster/cms.html",info = content.find_one({"id": project_id}))
    return render_template("webmaster/cms.html",info = project_document)



@app.route('/cms-about', methods = ['GET', 'POST'])
@login_required
def cms_about():
    if request.method == "POST":
        summary = request.form["summary"]
        intent = request.form["intent"]
        timeline = request.form["timeline"]
        db["About"].update_one({},{"$set":{"Summary": summary, "Intention": intent, "Timeline": timeline}})
        flash("Update Page Succesfully")
        return render_template("webmaster/cms_about.html", info = db["About"].find_one({}))

    homepage_data = db["About"].find_one({})
    return render_template("webmaster/cms_about.html", info=homepage_data)

def delete_web():
    num = content.count_documents({})
    if (num > 4):
        latest_web_id = str(num)
        content.delete_one({"id":latest_web_id})
    return redirect('/cms')