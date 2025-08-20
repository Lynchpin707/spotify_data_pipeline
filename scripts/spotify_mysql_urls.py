import re

def load_database(sp, txt_path, connection, cursor):
    
    # Read track URLs from file
    file_path = txt_path
    with open(file_path, 'r') as file:
        track_urls = file.readlines()
    cursor.execute('truncate table spotify_tracks; ')
    # Process each URL
    for track_url in track_urls:
        track_url = track_url.strip()  # Remove any leading/trailing whitespace
        try:
            # Extract track ID from URL
            track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

            # Fetch track details from Spotify API
            track = sp.track(track_id)

            # Extract metadata
            track_data = {
                'Track Name': track['name'],
                'Artist': track['artists'][0]['name'],
                'Album': track['album']['name'],
                'Release_date':track['album']['release_date'],
                'Popularity': track['popularity'],
                'Duration (minutes)': track['duration_ms'] / 60000
            }

            # Insert data into MySQL
            insert_query = """
            INSERT INTO spotify_tracks (track_name, artist, album, Release_date, popularity, duration_minutes)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                track_data['Track Name'],
                track_data['Artist'],
                track_data['Album'],
                track_data['Release_date'],
                track_data['Popularity'],
                track_data['Duration (minutes)']
            ))
            connection.commit()

            print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

        except Exception as e:
            print(f"Error processing URL: {track_url}, Error: {e}")


    print("All tracks have been processed and inserted into the database.")
