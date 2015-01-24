from flask import Flask
from flask import request
from pymongo import MongoClient
import os
import shutil

app = Flask(__name__)
client = MongoClient('localhost', 27017)

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
    # Sanity check
    if not project_name:
        return 'Invalid project name!', 403
    # Create the test folder if is a new project
    if not os.path.isdir("tests/" + project_name):
        shutil.copytree("tests/sample", "tests/" + project_name)
    # Read app url and write to link.txt
    link = os.popen('dokku url ' + project_name).read()
    f = open('tests/link.txt', 'w')
    f.write(link)

    # Run the tests
    os.system("cd tests/ && multimech-run " + project_name)
    return 'test done!'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)