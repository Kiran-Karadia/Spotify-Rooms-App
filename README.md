# Spotify-Rooms-App

App that allows mutiple people to join a 'room'. The room will be playing a song from the Host via Spotify.
In the room people can play/pause the music, as well as vote to skip the current song.
Host of the room can edit settings such as allowing guests to play/pause and the number of votes needed to skip

(Host must have a premium spotify account)


To run the app (WINDOWS):
1. Create a folder somewhere you'd like to store the project
2. Open a command prompt, cd to the folder and use 
```
git clone https://github.com/Kiran-Karadia/Spotify-Rooms-App.git 
```
3. Create a new environment using 
```
conda create --name *name_of_env* python 
```
4. Activate the environment with
```
conda activate *name_of_env* 
```
5. Change the current directory to the spotify_rooms_app folder using 
```
cd C:\...\...\...\Spotify-Rooms-App\spotify_rooms_app 
```
6. Once in the correct cd, install requirements using 
```
pip install -r requirements.txt 
```
7. Navigate to spotify/credentials.py and update the CLIENT_ID and CLIENT_SECRET variables with your own.
  * To find these, go to https://developer.spotify.com/dashboard/ and log in with your premium spotify account
  * Create a new app
  * On the dashboard of the app, you will find the Client ID and Client Secret (32 characters long each)
  * Click on EDIT SETTNGS and under Redirect URIs put http://127.0.0.1:8000/spotify/redirect (The same as REDIRECT_URI in credentials.py) 
  * Make sure to save the settings
  
8. To run the server, cd to where manage.py is located (the same location as step 5) and use 
```
python manage.py runserver 
```
9. On a browser, go to 127.0.0.1:8000

