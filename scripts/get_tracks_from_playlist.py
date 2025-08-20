import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

def get_tracks_from_playlist(sp, playlist_id, txt_path) :

    all_tracks = []
    results = sp.playlist_tracks(playlist_id)
    all_tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        all_tracks.extend(results['items'])

    # Save track URLs in a txt file
    with open(txt_path, "w", encoding="utf-8") as f:
        for item in all_tracks:
            track = item['track']
            if track:  # Ensure the track object is not None
                track_url = track['external_urls']['spotify']
                f.write(track_url + "\n")