import os
import pandas as pd

PROCESSED_DATA_PATH = 'data/processed_data/'
FILTERED_DATA_PATH = 'data/filtered_data/'

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
os.makedirs(FILTERED_DATA_PATH, exist_ok=True)

def save_filtered_data(df, filename):
    df.to_csv(f'{FILTERED_DATA_PATH}filtered_{filename}.csv', index=False)

if __name__ == "__main__":
    # Step 1: Load movies and ratings, then keep only movies that have ratings
    movies_df = pd.read_csv(f'{PROCESSED_DATA_PATH}movies.csv')
    ratings_df = pd.read_csv(f'{PROCESSED_DATA_PATH}ratings.csv')
    # Inner join to keep only movies that have ratings
    movies_with_ratings = movies_df.merge(ratings_df[['tconst']], on='tconst', how='inner')
    # Remove movies without genres
    movies_with_ratings = movies_with_ratings[
                            movies_with_ratings['genres'].notna() & 
                            (movies_with_ratings['genres'] != '\\N') & 
                            (movies_with_ratings['genres'] != '')]
    
    movies_with_ratings = movies_with_ratings.tail(500)
    lst_movies = movies_with_ratings['tconst'].tolist()
    save_filtered_data(movies_with_ratings, 'movies')

    # Step 2: Keep rows from Ratings, Movies-Actors, Movies-Directors if tconst in lst_movies else remove
    ratings_df = ratings_df[ratings_df['tconst'].isin(lst_movies)]
    save_filtered_data(ratings_df, 'ratings')

    movies_actors_df = pd.read_csv(f'{PROCESSED_DATA_PATH}movies_actors.csv')
    movies_actors_df = movies_actors_df[movies_actors_df['tconst'].isin(lst_movies)]
    
    movies_directors_df = pd.read_csv(f'{PROCESSED_DATA_PATH}movies_directors.csv')
    movies_directors_df = movies_directors_df[movies_directors_df['tconst'].isin(lst_movies)]

    # Step 3: Keep only nconst that appears in both actors and movies_actors
    actors_df = pd.read_csv(f'{PROCESSED_DATA_PATH}actors.csv')
    actors_nconst = set(actors_df['nconst'])
    movies_actors_nconst = set(movies_actors_df['nconst'])
    common_actors = actors_nconst.intersection(movies_actors_nconst)
    
    actors_df = actors_df[actors_df['nconst'].isin(common_actors)]
    movies_actors_df = movies_actors_df[movies_actors_df['nconst'].isin(common_actors)]
    movies_actors_df = movies_actors_df.drop_duplicates()
    save_filtered_data(actors_df, 'actors')
    save_filtered_data(movies_actors_df, 'movies_actors')
    
    # Keep only nconst that appears in both directors and movies_directors
    directors_df = pd.read_csv(f'{PROCESSED_DATA_PATH}directors.csv')
    directors_nconst = set(directors_df['nconst'])
    movies_directors_nconst = set(movies_directors_df['nconst'])
    common_directors = directors_nconst.intersection(movies_directors_nconst)
    
    directors_df = directors_df[directors_df['nconst'].isin(common_directors)]
    movies_directors_df = movies_directors_df[movies_directors_df['nconst'].isin(common_directors)]
    movies_directors_df = movies_directors_df.drop_duplicates()
    save_filtered_data(directors_df, 'directors')
    save_filtered_data(movies_directors_df, 'movies_directors')