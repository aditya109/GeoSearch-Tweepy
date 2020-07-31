# GeoSearch-Tweepy

## **Instructions For Usage**

**OS - Windows**

_Assuming you have python 3 and MySQL server installed._

## DB SETUP

1.  Start the MySQL server to check for logs and db creation.
    _Note your username, password_
2.  Create a database _twitter_ `CREATE DATABASE TWITTER`.
    _pic_
3.  Initiate the database usage. `USE TWITTER`
    _pic_
4.  Create a table within the **_TWITTER_** database. `CREATE TABLE TWITTERFEED2 (User ID VARCHAR(255), Date VARCHAR(255), Lat VARCHAR(255), Lng VARCHAR(255), Text VARCHAR(255));`
    _pic_
5.  Check if the table is proper or not. `DESC TWITTERFEED2;`
    _pic_

## SCRIPT SETUP

original script - GeoTweepy.py
my script - workup_file.py

1.  Open the unzipped folder and open `cmd` in the folder.
    _pic_
2.  Create a virtual environment in this folder. `virtualenv venv`
    _pic_
3.  Activate the environment. `.\venv\Scripts\activate`
    _pic_
4.  Install the packages in _requirements.txt_ `pip install -r requirements.txt`. This will install all your packages in the **_venv_** virtual environment.
    _pic_
5.  Open the workup\*file.py in any code editor. Make the following changes and check once. - [ ] Place your Twitter API consumer key, consumer secret, access token and access token secret in the place provided. - [ ] Check if the MySQL server is running on `localhost` with your \*\*\_username**\* and **_password_**. - [ ] Check if it contains a database **_twitter_** and the database is set in use. - [ ] Check if it contains the table **_twitterfeed2_\*\*.
    (Also the case does not matter for MySQL)
    (I have kept the code as original as possible so I created the server with given credentials only)
6.  Running the application `python workup_file.py`

Regarding the changes made by me,

- This script was facing problems while running on Python 2.7 environment so I tried upgrading the script to Python 3
- First I changed the way data was being parsed. I used json-loader to parse the status data.
- Created the a custom exception for indicating when the co-ordinates field was None and the code had to switch between co-ordinates field and bounding-box field.
- I have provided non-encoded format for writing into csv files as well.
  I have provided comments as and when required.
