import praw
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
        
    return sp

submissionTitles = []
tracks = []
sorted_tracks = []

 
def get_song_names():

    #Eclipse cant print out some characters that come up when pulling
    #things from reddit, run in console
    print("Pulling songs from reddit...")
    for submission in reddit.subreddit('listentothis').top(time_filter = 'day', limit=10):

        #Later sort and extract the artist and song name and then store THOSE into some arrays/variables
        #Also python's arrays are called lists, whats up with that?
        
        #Appending each title to submissionTitles
        #split splits the string at the character set
        if "-" in submission.title:
            splitName = submission.title 
            splitName = splitName.split('[')[0]
            splitName = splitName.split('(')[0]
            submissionTitles.append(splitName)
            #submissionTitles.append(submission.title) 
    #Printing out to make sure we got the right output
    #print(submissionTitles)
    
def get_track_id(track_dict):
 
    track_dict = track_dict['tracks']
    track_dict = track_dict['items']
    if (len(track_dict) == 0):
        print("Could not find song on Spotify")
    else:
        track_dict = track_dict[0]
        tracks.append(track_dict['id'])
        
    
def get_user(sp):
    user_id = sp.current_user()
    user_id = user_id['id']
    return user_id

def get_playlist_id(sp):

    numPlaylist = 0
    i = 0
    playlist_id = sp.current_user_playlists()
    playlist_list = playlist_id['items']
    numPlaylist = len(playlist_list)

    # prints out playlist names and their index
    while(i < numPlaylist):   
        playlist_dict = playlist_list[i]
        print(playlist_dict['name'] + " " , i)
        i = i + 1
    print("Which playlist would you like to add to?")
    playlist_index = input()
    playlist_index = int(playlist_index)
    playlist_id = playlist_list[playlist_index]
    playlist_id = playlist_id['id']  
    
    
    
    return playlist_id
        
def searchAdd(sp):
    item = 0
    while(item < len(submissionTitles)):
        searchTerm = submissionTitles[item]
        print("Searching spotify for " + searchTerm)
        track_dict = sp.search(searchTerm, limit = 1, type = "track")
        track_id = get_track_id(track_dict)
        tracks.append(track_id)
        item = item + 1
    print(tracks)
    
def trackAdd(sp, playlist_id):
    sorted_tracks = filter(None, tracks)
    print(sorted_tracks)
    username = get_user(sp)
    sp.user_playlist_add_tracks(username, playlist_id, sorted_tracks)
    print ("Success!")
        

def main():
    
    #Logs into spotify
    sp = spotifyLogin()
    #Prints out your public playlists and asks user which one you would like to add to
    playlist_id = get_playlist_id(sp)
    #Gets song names and populates submissionTitles list with searchable items
    get_song_names()
    #Searches for and gets track_id then populates track list with ids to add to playlist
    searchAdd(sp)
    trackAdd(sp, playlist_id)
    


if __name__ == "__main__":
        main()
    
    
    
    
    