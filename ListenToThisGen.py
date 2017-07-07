import praw
import sys
import configparser
import spotipy
import spotipy.util as util

username = ""
scope = ''
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost'

#Gets access token to work with Spotify API
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

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
    
    
    
    
    