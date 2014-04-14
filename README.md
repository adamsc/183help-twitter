183help-twitter
===============

A twitter bot for EECS 183

Use
===

Requirements
------------
* Python 2.7
* git
* [tweepy](https://github.com/tweepy/tweepy#installation)

Installation
------------
Simply do `git clone git@github.com:adamsc/183help-twitter.git`

Register
--------
To run the program, you must first register as a twitter developer. To do so, visit the [developer application site](https://apps.twitter.com/), login, and create a new application.

In your new application, go to Permissions, and change the acccess level to "Read and Write". Then, go to the API Keys tab, and press "Regenerate API Keys". Then, on the API Keys tab, press "Create my access token". Then press the "Test OAuth" button in the upper right corner, it will take you a page showing your "Consumer key", "Consumer secret", "Access token" and "Access token secret". Leave this page open, you will need it later.

Configuration
-------------
In the file 183help_twitter/183help.cfg, update the credentials to those you received from the "Register" step above.

Run
---
To run the application, run the file `eecs183help_twitter.py` either from the command line or your IDE.
