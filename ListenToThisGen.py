import praw
import sys
import configparser
import spotipy
import spotipy.util as util


#Read from the config file for our credentials and keys

config = configparser.ConfigParser()
config.read('config.ini')

#R_ for reddit, these are our credentials pulled from the config file
R_USERNAME = config.get('reddit', 'r_username')
R_PASSWORD = config.get('reddit', 'r_password')
R_ID = config.get('reddit', 'r_client_id')
R_SECRET = config.get('reddit', 'r_client_secret')
R_AGENT = config.get('reddit', 'r_user_agent')

#Reddit initializer
reddit = praw.Reddit(client_id = R_ID, 
                     client_secret = R_SECRET,
                     user_agent =  R_AGENT)

# THe S_ denotes spotify
S_USERNAME = config.get('spotify', 's_username')
S_SCOPE = config.get('spotify', 's_scope')
S_CLIENT_ID = config.get('spotify', 's_client_id')
S_CLIENT_SECRET = config.get('spotify', 's_client_secret')
S_REDIRECT_URI = config.get('spotify', 's_redirect_uri')

#Gets access token to work with Spotify API
token = util.prompt_for_user_token(S_USERNAME, S_SCOPE, S_CLIENT_ID, S_CLIENT_SECRET, S_REDIRECT_URI)



#Spotify login, will check to see if credentials for token work
def spotifyLogin():
    print("Attempting to login to Spotify...")
    if token:
        sp = spotipy.Spotify(auth=token)
        print("Logged into spotify")
        
                  
    else:
        print("Can't get token, login fail")
        
def redditLogin():
    #for now just testing if credentials are working
    #Eclipse cant print out some characters that come up when pulling
    #things from reddit, run in console
    print("Pulling info from reddit...")
    for submission in reddit.subreddit('listentothis').top(limit=10):
        print(submission.title)
    
    
    
        
    

def main():
    
    spotifyLogin()
    redditLogin()
        
    

if __name__ == "__main__":
        main()
    
    
    
    
    