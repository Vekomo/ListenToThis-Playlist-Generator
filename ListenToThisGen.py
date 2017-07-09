import praw
import sys
import configparser
import spotipy
import spotipy.util as util


#Read from the config file for our credentials and keys

config = configparser.ConfigParser()
config.read('config.ini')

# THe S_ denotes spotify, R_ for the reddit credentials
S_USERNAME = config.get('spotify', 's_username')
S_SCOPE = config.get('spotify', 's_scope')
S_CLIENT_ID = config.get('spotify', 's_client_id')
S_CLIENT_SECRET = config.get('spotify', 's_client_secret')
S_REDIRECT_URI = config.get('spotify', 's_redirect_uri')

#Gets access token to work with Spotify API
token = util.prompt_for_user_token(S_USERNAME, S_SCOPE, S_CLIENT_ID, S_CLIENT_SECRET, S_REDIRECT_URI)

#IF token request was succesful, "Do stuff". ELSE print out why failed
if token:
    sp = spotipy.Spotify(auth=token)   
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token")
print (results)
    
    
    
    
    