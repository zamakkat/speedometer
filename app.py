from flask import Flask
from flask import request
from pymongo import MongoClient
import os
<<<<<<< HEAD
import shutil
=======
>>>>>>> 3c510331bfb37d3c79142c686af94bb7c21bb15b

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

@app.route('/clone', methods=['POST', 'GET'])
def clone_new_repo():
    repo_name = request.form['name']
    repo_url = request.form['url']
    if os.system('git clone ' + repo_url + ' ' + '../external/'+repo_name) != 0:
        return 'repo existed or cannot create folder, try using /pull/<repo_name> instead', 403
    elif os.system('cd ../external/%s && git remote add boostiodokku dokku@localhost:%s' %(repo_name, repo_name)):
        return 'failed to add repository remote, please try again!', 403
    elif os.system('git push boostiodokku master') != 0:
        return 'cannot deploy the new project. Test your deployment first dude!', 403
    return 'done!', 200

@app.route('/pull/<project_name>')
def fetch_repo(project_name):
    if os.system('cd ../external/%s' %(project_name)) != 0:
        return 'repo not existed or cannot be accessed, try using /clone instead', 403
    elif os.system('git pull origin master') != 0:
        return 'repo cannot be pulled. Please check repo setting', 403
    elif os.system('git push boostiodokku master') != 0:
        return 'cannot deploy the new project. Test your deployment first dude!', 403
    return 'repo updated', 200

if __name__ == '__main__':
    app.debug = True
    app.run()