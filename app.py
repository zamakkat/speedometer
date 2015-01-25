from flask import Flask
from flask import request
from firebase import firebase
import sqlite3
import os
import shutil
import json

app = Flask(__name__)
firebase = firebase.FirebaseApplication('https://vivid-torch-3095.firebaseio.com', authentication=None)

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
    test_result = run(project_name)
    firebase.post('/commit_details', test_result)
    return test_result, 200

@app.route('/pull/<project_name>')
def fetch_repo(project_name):
    if os.system('cd ~/external/%s' %(project_name)) != 0:
        return 'repo not existed or cannot be accessed, try using /clone instead', 403
    elif os.system('cd ~/external/%s && git pull origin master' %(project_name)) != 0:
        return 'repo cannot be pulled. Please check repo setting', 403
    elif os.system('cd ~/external/%s && git push boostiodokku master' %(project_name)) != 0:
        return 'cannot deploy the new project. Test your deployment first dude!', 403
    test_result = run(project_name)
    firebase.post('/commit_details', test_result)
    return test_result, 200

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
    f.close()

    # Run the tests
    os.system("cd tests/ && multimech-run " + project_name)

    # Get final data
    response = data(project_name)
    return response

def data(project_name):
    conn = sqlite3.connect('tests/boostio.db')
    c = conn.cursor()
    c.execute('''
        SELECT MIN(scriptrun_time) FROM mechanize_results
        WHERE project_name='%s'
        AND mechanize_global_configs_id=
            ( SELECT MAX(mechanize_global_configs_id) FROM mechanize_results WHERE project_name='%s' )
        ''' %(project_name, project_name))
    min_time = c.fetchall()
    print min_time[0][0]
    c.execute('''
        SELECT AVG(scriptrun_time) FROM mechanize_results
        WHERE project_name='%s'
        AND mechanize_global_configs_id=
            ( SELECT MAX(mechanize_global_configs_id) FROM mechanize_results WHERE project_name='%s' )
        ''' %(project_name, project_name))
    avg_time = c.fetchall()
    print avg_time[0][0]
    c.execute('''
        SELECT MAX(scriptrun_time) FROM mechanize_results
        WHERE project_name='%s'
        AND mechanize_global_configs_id=
            ( SELECT MAX(mechanize_global_configs_id) FROM mechanize_results WHERE project_name='%s' )
        ''' %(project_name, project_name))
    max_time = c.fetchall()
    print max_time[0][0]
    commit_info = os.popen('cd ~/external/%s && git log -1 --pretty=format:"%%h,%%cn,%%ce,%%cd,%%s"' %(project_name)).read()

    commit = commit_info.split(',')
    chash = commit[0]
    author_name = commit[1]
    author_email = commit[2]
    date = commit[3]
    message = commit[4]

    run_response = {'commit': { 'hash': chash, 'author_name': author_name, 'author_email': author_email, 'date': date, 'message': message },'stats': { 'avg': avg_time[0][0], 'min': min_time[0][0], 'max': max_time[0][0]}}
    return run_response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)