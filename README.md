# Spotify-Rooms-App

App that allows mutiple people to join a 'room'. The room will be playing a song from the Host via Spotify.
In the room people can play/pause the music, as well as vote to skip the current song.
Host of the room can edit settings such as allowing guests to play/pause and the number of votes needed to skip

(Host must have a premium spotify account)


To run the app:
1. Create a folder somewhere you'd like to store the project
2. Use git clone https://github.com/Kiran-Karadia/Spotify-Rooms-App.git
3. Create a new environment using conda create --name *name_of_env* python
4. Activate the environment with conda activate *name_of_env*
5. Change the current directory to the spotify_rooms_app folder using cd C:\...\...\...\Spotify-Rooms-App\spotify_rooms_app
7. Install requirements using pip install -r requirements.txt
8. To run the server, use python manage.py 0.0.0.0:8000
9. To go to the app over LAN, use the IPv4 Address of the device running the server. 
10. This can be found by using the command ipconfig in a command prompt)
11. Example the the address : 192.168.0.xx:8000 (where xx is specific to device running the server)
