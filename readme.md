# IdéSYS ERP server

This is a server application coded in python3 using flask framework.

Run

    export FLASK_ENV=development
    python3 server.py

## Google API

 - go in the google cloud platform
 - create a project
 - create a service account
 - download the keys
 - enable domain-wide delegation
 - code:
  - get the delegated credentials
  - make the API call

## TODO

 - email notification on user registration
 - refactor auth.views with the auth middleware
 - refactor the render template api views
 - upload in gdrive: create folder and upload file in a specific folder
 - resticted access to flask admin (flask admin is disabled)


# IdéSYS-ERP

This project is under development.

## Setup Google API

 - go in the google cloud platform
 - create a project
 - create a service account
 - download the keys
 - enable domain-wide delegation
 - code:
  - get the delegated credentials
  - make the API call
 - Enable GDrive API at https://console.developers.google.com/apis/api/drive.googleapis.com/overview


### POC

Step 1: use the python google api library and domain wide delegation to access google api

Step 2: use the http method (with JWT) to facilitate the change of programming language.

## TODO

 - register and login into IdéSYS-ERP webapp with a google account
