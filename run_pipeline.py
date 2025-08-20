from scripts.get_tracks_from_playlist import get_tracks_from_playlist
from scripts.spotify_mysql_urls import load_database
from scripts.playlist_analysis import analyze
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector


client_id = 'b881f8e3edf24ac5aa17df3352df79ad'
client_pwd = '3a38115ea36b4278a522ed0f5106d130'
playlist_id = '5JVMLPn4iQHJmF0B7hbiwV'
txt_path ="./sources/playlist_tracks.txt"

#MySQL database connection credintials
db_user='spotifyproject'       # Replace with your MySQL username
db_pwd='spotifyproject'   # Replace with your MySQL password
db='spotify_db'  

db_config = {
        'host': 'localhost', 
        'user': 'spotifyproject',      
        'password': 'spotifyproject',   
        'database': 'spotify_db'     
    }

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_pwd  
    ))
    get_tracks_from_playlist(sp, playlist_id, txt_path)
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    load_database(sp, txt_path, connection, cursor)
    cursor.close()
    analyze(connection)
    connection.close()

if __name__ == "__main__":
    main()