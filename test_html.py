import json
from flask import Flask,request,Response
from flask import render_template
import webbrowser
import os
import json

from pathlib import Path
import sys
import logging
import pprint
import json


app = Flask(__name__,template_folder="templates")
@app.route("/")
def index():
    return render_template('chat_example.html')

            

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5001")
    app.run(host = "0.0.0.0",port = 5001)