# ETL_demo_twitterv2

This is ETL process demo on Twitter, baiscally on streaming of twitter API v2.0.

This demo match the keyword in the comments of twitter, then process it as positive or negative, then set up a flask demo to simply show the result.

How to run:
1. pip3 install -r requirements.txt
install the libs

2. (optional)go to python3, then "import nltk" and "nltk.download('punkt')"
this works for the fist installing textblob, it needs the corpos to classfy the sentences.

3. modify the config.json, the "query" means the keyword, and give a new bearer Token in the token field. the default setting is "ETL_demo", and the default bearer token should be applied via developer.twitter.com

4.python3 flask_server.py

The flask server should run at 127.0.0.1:5000, then you can go to browser see the presenting results. 


