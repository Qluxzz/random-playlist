# random-playlist
This script creates random Spotify playlists

# Example
 random-playlist.py --amount 10 --artist "Tom Petty" --username 'your-username-here'
 
 This above example would create a random playlist with 10 tracks by Tom Petty

# Installation
This script depends on 
* spotipy, python wrapper for the spotify web api
* tqdm, used for progress bars
* Spotify Web Api Key which can be found here https://developer.spotify.com/my-applications/#!/
* config file called 'settings.ini' which should look like this:

```
[DEFAULT]
SPOTIPY_CLIENT_ID = 'your client id'
SPOTIPY_CLIENT_SECRET = 'your client secret'
SPOTIPY_REDIRECT_URI = 'your redirect uri'
```