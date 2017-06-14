competispy
===================


The competispy app enables its users to run some interesting queries against a championships inscriptions database. Its main focus is to split the inscriptions by age categories when such incscriptions come mixed in the same file.

It has been happily used in for the Master Spanish Swimming championships.

----------


Pre-Requisites
-------------

The app uses a MongoDB database to store all the competition data. In order to run a personal instance of the app, a MongoDB database must be accesible.

> **Note:**

> - A free MongoDB can be obtained at [mlab webpage](https://mlab.com "mlab").

The app is written in python 2.7, so its interpreter must be installed.
The app requirements are:

 - pymongo (database access)
 - mako (templates rendering)
 - cherrypy (web server)

All of them can be easily installed with pip


----------
Configuration
-------------------

Simply add your database data into the *default_database_keys* file.


Running the app
-------------------
Run the following command from the terminal:

    python application.py

Open a web-browser and navigate to http://localhost:8080


Adding a championship to the database
-------------------

TODO!!
The following API seems to be a perfect solution for pdf parsing:
http://pdfextractoronline.com/tabex-pdf-api/

Its TXT output is readable by the importer
