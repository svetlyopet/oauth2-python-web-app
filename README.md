# Introduction 
Simple python application built with the Flask framework to demonstrate consumption of API's using the Authorization Code with PKCE flow.
Useful for PoC's and quick tests.

# Getting Started
Only prerequisite is to have python3 installed to run the application.

The configuration of the Oauth2 client and protected resource that the Application will try to call with the token is in config.py. 
client_id is provided by the IdP. The redirect_uri is set by the Developer in the IdP and should be set to http://localhost:5000/callback so
this application can catch the authcode.

# Build and Test
Clone this repo and create a new python virtual environment for the project:
```
cd oauth2-python-web-app
python3 -m venv venv
source $PWD/venv/bin/activate
```

Install dependancies:
```
pip install -r requirements.txt
```

Fill in the config.py file with your configuration.

Run the Application:
```
python3 server.py
```

Open a browser and go to http://localhost:5000/ 

Hitting the Run Test button will start the OAuth2 Authorization Code with PKCE flow.