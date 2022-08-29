from logging import exception
from venv import create
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json

app = Flask(__name__)

client_id = "28c278acdfcc4e9d88122d5a107cf369"
client_secret = "6f6eb1ef16b045e2bf86a59b278b014e"

app.secret_key = "dyVkhnMvxd"
app.config['SESSION_COOKIE_NAME'] = "Cookies"

@app.route('/')
def login():
    sp_oauth = authorizeUser()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = authorizeUser()
    session.clear()
    # Saving the token information for the login with the cookies
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('user_data', _external=True))

@app.route('/getUserPlaylists')
def user_data():
    try:
        token_info = session.get("token_info", None)
        if not token_info:
            raise "exception"
    except:
        print("User has not logged in")
        return redirect(url_for('login', _external=False))
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = authorizeUser()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    global user
    user = spotipy.Spotify(auth=token_info['access_token'])
    return user.current_user_playlists(limit=50, offset=0)
    

def authorizeUser():
    return SpotifyOAuth(
        client_id = "28c278acdfcc4e9d88122d5a107cf369",
        client_secret = "6f6eb1ef16b045e2bf86a59b278b014e",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read, playlist-read-collaborative, app-remote-control, user-read-playback-state, user-read-email, user-top-read, user-follow-read, user-read-currently-playing, playlist-read-private"
    )


# get_emotion_data: String (user input) -> dict
def get_emotion_data(text):
    # Get emotion from ML model (incomplete, waiting on function)
    emotion = "" # placeholder for predict_emotion(text)
    
    # Open JSON file
    f = open(emotion + '_data.json')
    
    # Dictionary representing JSON object
    data = json.load(f)

    f.close()

    return data
