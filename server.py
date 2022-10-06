from config import client_id, redirect_uri, authorization_base_url, token_url, scope, response_type, protected_uri, headers
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
import json
import pkce
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    json_formatted = {}
    return render_template('index.html', json_formatted=json_formatted)

@app.route("/demo", methods=["GET"])
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider
    using an URL with a few key OAuth parameters.
    """

    # generate PKCE codes
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    session["code_verifier"] = code_verifier
    session["code_challenge"] = code_challenge

    oauth2 = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth2.authorization_url(authorization_base_url)

    # State is used to prevent CSRF
    session['oauth_state'] = state
    return redirect(authorization_url+'&code_challenge='+code_challenge+"&response_type="+response_type+'&code_challenge_method=S256')


""" Step 2: User authorization.

This happens in the browser and is part of User-IdP flow.
"""

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the IdP provider to the registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    # Retrieve code verifier from initial step
    code_verifier = session.get("code_verifier", None)

    # Parse Authcode from callback
    code = request.args.get("code")

    oauth2 = OAuth2Session(client_id, state=session['oauth_state'])
    token = oauth2.fetch_token(token_url, client_id=client_id, code=code, code_verifier=code_verifier, verify=False, include_client_id=True)

    # At this point we can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /api/resources
    session['oauth_token'] = token

    return redirect(url_for('.callApi'))


@app.route("/api/resource", methods=["GET"])
def callApi():
    """Step 4: Fetching a protected resource using the OAuth 2 token.
    """
    
    oauth2 = OAuth2Session(client_id, token=session['oauth_token'])
    oauth2.headers.update(headers)
    r = oauth2.get(protected_uri).content

    try: 
        json_response = json.loads(r.decode("utf-8"))
        json_formatted = json.dumps(json_response, indent=2)
    except json.decoder.JSONDecodeError:
        json_response = {"JSON decoding Error": "API returned empty result, error, or bad JSON"}
        json_formatted = json.dumps(json_response, indent=2)

    return render_template("index.html", json_formatted=json_formatted)

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
