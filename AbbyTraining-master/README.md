# AbbyTraining

An elegant online training website

[Demo Online](http://abbyDemo.cloudapp.net)
    
    username: admin
    password: admin

Run locol demo service

    ./start.sh
    ./start.sh -f # To force rebuild virtual environment

Run testcases

    ./run_test.sh

Create database

    python manage.py syncdb

Frontend

	cd frontend
	npm install
	# if link error about c lib in MAC, install XCode7, then try again
	npm -g install bower gulp
	bower install
	# JQuery >= 2.2.1
	gulp serve