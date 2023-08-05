# Steps to setup the project

## First create a virtual environment
```
python -m venv env
```
## To activate the env
### for linux 
```
source env/bin/activate
```
### for windows
```
env\Scripts\activate.bat
```
## git clone the link [erpProject](https://github.com/Arup20MA20010/erpSourceProject.git)
```
git clone https://github.com/Arup20MA20010/erpSourceProject.git
```
## Move to the directory erpSourceProject
```
cd erpSourceProject
```
## Install the requirements
```
pip install -r requirements.txt
```
## To run the server
```
python manage.py runserver
```
## After running the server you can go to the link
## To go to the admin Panel you can go to localhost:3000/admin
## To create superuser for the admin panel
```
python manage.py createsuperuser
```
## Whenever you clone,pull the repo, delete the files in the migrations folder except the init.py file and run the following commands.
```
python manage.py makemigrations
python manage.py migrate
```
### Now you are all set to go


### The requirements.txt will updated with time and so will be the readme.