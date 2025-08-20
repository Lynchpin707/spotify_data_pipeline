import pandas as pd
import matplotlib.pyplot as plt  # Add this import


def analyze(connection):

    query = "SELECT artist, release_date, popularity, duration_minutes FROM spotify_tracks;"
    df = pd.read_sql(query, connection)
    
    # Debug: Check data shape and basic info
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Sample data:\n{df.head()}")
    print(f"Null values:\n{df.isnull().sum()}")
    
    # ---- Top Artists ----
    print(f"\nUnique artists: {df['artist'].nunique()}")
    top_artists = (
        df['artist']
        .value_counts(normalize=True) * 100
    ).round(2).reset_index()
    top_artists.columns = ['Artist', 'Percentage']

    print("\n Top Artists:")
    print(top_artists.head(10))

        # Visualize Top Artists as a pie chart and save the plot
    plt.figure(figsize=(8, 8))
    plt.pie(
        top_artists['Percentage'][:10],
        labels=top_artists['Artist'][:10],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    plt.title('Top 10 Artists by Percentage')
    plt.tight_layout()
    plt.savefig('outputs/top_10_artists_pie.png')
    plt.close()

    # ---- Top Decades ----
    print(f"\nRelease date sample: {df['release_date'].head()}")
    print(f"Release date dtype: {df['release_date'].dtype}")
    
# Parse release_date to datetime, handling year, year-month, and year-month-day
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce', infer_datetime_format=True)
    print(f"Converted release_date dtype: {df['release_date'].dtype}")
    df['release_year'] = df['release_date'].dt.year
        
    df['decade'] = (df['release_year'] // 10) * 10
    top_decades = (
            df['decade']
            .value_counts(normalize=True) * 100
        ).round(2).reset_index()
    top_decades.columns = ['Decade', 'Percentage']

    print("\n Top Decades:")
    print(top_decades.head(10))

        # Visualize Top Decades and save the plot
    plt.figure(figsize=(8, 5))
    plt.bar(top_decades['Decade'].astype(str), top_decades['Percentage'], color='orange')
    plt.title('Top Decades by Percentage')
    plt.xlabel('Decade')
    plt.ylabel('Percentage') 
    plt.tight_layout()
    plt.savefig('outputs/top_decades_bar.png')
    plt.close()
        