# [= TORCH v0.0.1a-1.0 =]

from flask import Flask, render_template, request, jsonify, session, send_file
from flask_session import Session
import pymongo, os, threading
from cachelib.file import FileSystemCache
from datetime import timedelta

# [= Import modules =]
import modules.main_module as main_module

# [= Global Variables =]

# Allowed languages list
allowed_languages_list = ["IT", "EN"]

# Database
dbclient = pymongo.MongoClient("mongodb://localhost:27017/") # Client connection string
db = dbclient["torch"] # Main database connection

# Collections
users_collection = db["users"]

language = {} # Create language dictionary

# [= Main directories =]

APP_ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Main
STATIC_DIRECTORY = os.path.join(APP_ROOT_DIRECTORY, "static") # Static directory necessary for Flask
TEMPLATES_DIRECTORY = os.path.join(APP_ROOT_DIRECTORY, "templates") # HTML templates directory necessary for Flask
SESSIONS_DIRECTORY = os.path.join(APP_ROOT_DIRECTORY, "sessions") # Session directory necessary for flask_session
MODULES_DIRECTORY = os.path.join(APP_ROOT_DIRECTORY, "modules") # Modules directory
LANGUAGES_DIRECTORY = os.path.join(APP_ROOT_DIRECTORY, "languages") # Languages files directory
# Static main directories
PICTURES_DIRECTORY = os.path.join(STATIC_DIRECTORY, "pictures") # Pictures main directory inside static directory for better use with jinja2
# Pictures directories
MAIN_PICTURES_DIRECTORY = os.path.join(PICTURES_DIRECTORY, "main") # Main pictures directory, contains pictures like logo

# [= Create directories if not exists =]

# Main directories
if os.path.exists(STATIC_DIRECTORY) == False: os.mkdir(STATIC_DIRECTORY)
if os.path.exists(TEMPLATES_DIRECTORY) == False: os.mkdir(TEMPLATES_DIRECTORY)
if os.path.exists(SESSIONS_DIRECTORY) == False: os.mkdir(SESSIONS_DIRECTORY)
if os.path.exists(MODULES_DIRECTORY) == False: os.mkdir(MODULES_DIRECTORY)
if os.path.exists(LANGUAGES_DIRECTORY) == False: os.mkdir(LANGUAGES_DIRECTORY)
# Static main directories
if os.path.exists(PICTURES_DIRECTORY) == False: os.mkdir(PICTURES_DIRECTORY)
# Pictures directories
if os.path.exists(MAIN_PICTURES_DIRECTORY) == False: os.mkdir(MAIN_PICTURES_DIRECTORY)

# [= Main settings =]

app = Flask(__name__)
app.secret_key = "541Cnajn-?!mkamQ!99))amca-.asdaca6ggfgjhyt3BSnCISU"
SESSION_TYPE = "cachelib"
SESSION_SERIALIZATION_FORMAT = "json"
SESSION_CACHELIB = FileSystemCache(cache_dir=SESSIONS_DIRECTORY, threshold=500)
PERMANENT_SESSION_LIFETIME = timedelta(hours=9)
SESSION_REFRESH_EACH_REQUEST = True
app.config.from_object(__name__)
Session(app)

# [= Homepage =]

# Homepage
@app.route("/", methods = ["GET"])
def homepage():
    # Language setting
    if "language" not in session:
        try:
            if "it" in request.headers.get("Accept-Language") or "IT" in request.headers.get("Accept-Language"): session["language"] = "IT" # Italian language
            else: session["language"] = "EN" # English language
        except TypeError: session["language"] = "EN" # Set english by default if language headers is not recognized
    
    return render_template("home.html")

# Login
@app.route("/login", methods = ["POST"])
def login():
    # Check if user is already logged
    if "logged" in session:
        # If isn't an Ajax request type
        if request.headers.get("Content-type") != "application/json": return render_template("error.html")
        # If is an Ajax request type
        else: return jsonify({"response": "error"})
    
    username = str(request.json["p_username"]).strip()
    password = str(request.json["p_password"]).strip()
    
    # Get user data
    user = users_collection.find_one({"username": username, "password": password})
    
    # Check if username and password is correct, if not response with a "stealth" response type (no location reloading or replacement in javascript)
    if user == None: return jsonify({"response": "no"})
    
    # Proceed with login functions
    session["username"] = username
    session["logged"] = True
    session["name"] = user["name"]
    session["surname"] = user["surname"]
    session["language"] = user["language"]
    session["access"] = user["access"]
    
    return jsonify({"response": "ok"})

# Logout
@app.route("/logout", methods = ["POST"])
def logout():
    # Check if user isn't logged
    if "logged" not in session:
        # If isn't an Ajax request type
        if request.headers.get("Content-type") != "application/json": return render_template("error.html")
        # If is an Ajax request type
        else: return jsonify({"response": "error"})
    
    # Proceed with logout functions
    
    session.pop("logged")
    session.pop("username")
    session.pop("name")
    session.pop("surname")
    session.pop("access")
    
    return jsonify({"response": "ok"})

# [= Goods =]
@app.route("/goods", methods = ["GET"])
def goods():
    # Check if user isn't logged
    if "logged" not in session or "goods" not in session["access"]:
        # If isn't an Ajax request type
        if request.headers.get("Content-type") != "application/json": return render_template("error.html")
        # If is an Ajax request type
        else: return jsonify({"response": "error"})
    
    return render_template("goods.html")

# [= Main pages =]

# Set language
@app.route("/setlanguage", methods = ["GET"])
def setlanguage():
    lang = str(request.args.get("p_language")).upper().strip()
    
    # Check if language string is correct
    if lang not in allowed_languages_list: return jsonify({"response": "error"})
    
    session["language"] = lang
    
    # Modify database record if user is logged in
    if "logged" in session:
        users_collection.update_one({"username": session["username"]}, {"$set": {"language": lang}})
    
    return jsonify({"response": "ok"})

# Get language
@app.route("/getlanguage", methods = ["GET"])
def getlanguage():
    return jsonify(main_module.get_language_dict(session["language"], language))

# [= Context Processor =]
@app.context_processor
def langcontextpage(): # Pass language dict to jinja2
    return dict(language = language)

# [= Error Page =]
@app.route("/error")
def error():
    return render_template("error.html")

# Error handling
@app.errorhandler(404)
def error404(e):
    return render_template("error.html")
@app.errorhandler(405)
def error405(e):
    return render_template("error.html")

# [= Application start =]

language = main_module.load_languages_files(LANGUAGES_DIRECTORY) # Start language dictionary
if __name__ == "__main__":
    app.run()