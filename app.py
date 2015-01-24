from flask import Flask
from pymongo import MongoClient
import os
import shutil

app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/run')
def run():
    project_name = "project1"
    shutil.copytree("test", project_name)
    os.system("multimech-run " + project_name)
    return 'OK!'


if __name__ == '__main__':
    app.run()