
## Getting started
1. Clone
1. Install `visrtualenv`
```
$ pip install virtualenv
$ virtualenv venv
```
1. Install `Flask`
```
$ pip install Flask
```
1. Isntall `pymongo`
```
$ pip install pymongo
```
1. Install `MongoDB`
```
$ brew update
$ brew install mongodb
```

## Developing
1. Create a `data/db` folder in root.
1. Start MongoDB server
```
$ mongod --dbpath /path/to/project/folder/data/db
```
1. Run the app
```
python app.py
```