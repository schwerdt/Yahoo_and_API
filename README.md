Yahoo_and_API
=============
The goal of this project is to interact with the Yahoo Finance API and
get some data about stock trading history for a specific stock.  


To use the using_requests branch, you'll probably want to set up a
virtual environment and install the dependencies using pip:


virtualenv .
source bin/activate
pip install -r requirements.txt


Then, to use yahoo_api.py:


python yahoo_api.py 2014-08-01 2014-10-01


If everything works as expected you'll get output that looks
something like this showing the weekly volume for the week
ending on the date indicated:


2014-10-06: 36222700
2014-09-29: 32607400
2014-09-22: 27641500
2014-09-15: 28448000
2014-09-08: 21675200
2014-09-02: 23068500
