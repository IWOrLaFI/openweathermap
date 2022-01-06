Be sure to use the Python version > 3.9.0.
To install the application:
-----------
# clone the repository

created new folder and opened terminal there
enter command:

$ git clone https://github.com/IWOrLaFI/openweathermap.git

***

$ cd openweathermap

***
 Create a virtualenv and activate it:
-
$ python3 -m venv venv

$ source venv/bin/activate

Or on Windows cmd:
-
$ py -3 -m venv venv

$ venv\Scripts\activate.bat

***
Install all needed libraries, provided in requirements.txt:
-
$ pip install -r requirements.txt

***
Open folder src
-
$ cd src
***
For update db
-
$ python3 main.py
***
Run server
-
$ python3 app.py

***
Test requests
-
$ python3 request_samples.py


