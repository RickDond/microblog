from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

import datetime, os

load_dotenv()

def create_app():
    app = Flask(__name__)
    cliente = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = cliente.microblog
    content = app.db["entries"]
    content_list = []

    @app.route("/", methods=["GET","POST"])
    def home():

        if request.method == "POST":
            entry_content = request.form.get("content")
            content_date = datetime.datetime.today()
            
            content.insert_one(
                {
                "entry_content":entry_content, 
                "entry_date":content_date.strftime("%Y-%m-%d"),
                "entry_logdate": content_date.strftime("%Y-%m-%d %H:%M:%S"),
                })
        content_list = [ (e["entry_content"],e["entry_date"], e["entry_logdate"] ) for e in app.db["entries"].find()]

        return render_template("home.html", entries=reversed(content_list))
    return app