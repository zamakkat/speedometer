from flask import Flask
from flask import request
import sqlite3
import os
import shutil

app = Flask(__name__)
conn = sqlite3.connect('example.db')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/clone', methods=['POST', 'GET'])
def clone_new_repo():
    project_name = request.form['name']
    repo_url = request.form['url']
    if os.system('git clone %s ~/external/%s' %(repo_url,project_name)) != 0:
        return 'repo existed or cannot create folder, try using /pull/<project_name> instead', 403
    elif os.system('cd ~/external/%s && git remote add boostiodokku dokku@localhost:%s' %(project_name, project_name)):
        return 'failed to add repository remote, please try again!', 403
    elif os.system('cd ~/external/%s && git push boostiodokku master' %(project_name)) != 0:
        return 'cannot deploy the new project. Test your deployment first dude!', 403
    elif run(project_name):
        return 'done!', 200

@app.route('/pull/<project_name>')
def fetch_repo(project_name):
    if os.system('cd ~/external/%s' %(project_name)) != 0:
        return 'repo not existed or cannot be accessed, try using /clone instead', 403
    elif os.system('cd ~/external/%s && git pull origin master' %(project_name)) != 0:
        return 'repo cannot be pulled. Please check repo setting', 403
    elif os.system('cd ~/external/%s && git push boostiodokku master' %(project_name)) != 0:
        return 'cannot deploy the new project. Test your deployment first dude!', 403
    elif run(project_name):
        return 'repo updated', 200

@app.route('/run/<project_name>')
def run(project_name):
    if not project_name:
        return 'Invalid project name!', 403
    shutil.copytree("tests/sample", "tests/" + project_name)
    os.system("multimech-run tests/" + project_name)
    return 'test done!'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)