import os
import pandas as pd

RAW_DATA_PATH = 'data/raw_data/'
PROCESSED_DATA_PATH = 'data/processed_data/'

os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def process_actors(df):
    df = df[df['primaryProfession'].str.contains('actor|actress', case=False, na=False)]
    df = df[['nconst', 'primaryName']]
    df.to_csv(f'{PROCESSED_DATA_PATH}actors.csv', index=False)

def process_movies(df):
    df = df[df['titleType'] == 'movie']
    df = df[['tconst', 'primaryTitle', 'startYear', 'genres']]
    df.to_csv(f'{PROCESSED_DATA_PATH}movies.csv', index=False)

def process_movies_actors(df):
    df = df[df['category'].isin(['actor', 'actress'])]
    df = df[['tconst', 'nconst', 'characters']]
    df.to_csv(f'{PROCESSED_DATA_PATH}movies_actors.csv', index=False)

def process_directors(df):
    df = df[df['primaryProfession'].str.contains('director', case=False, na=False)]
    df = df[['nconst', 'primaryName']]
    df.to_csv(f'{PROCESSED_DATA_PATH}directors.csv', index=False)

def process_movies_directors(df):
    df = df[df['category'] == 'director']
    df = df[['tconst', 'nconst']]
    df.to_csv(f'{PROCESSED_DATA_PATH}movies_directors.csv', index=False)

def process_ratings(df):
    df = df[['tconst', 'averageRating']]
    df.to_csv(f'{PROCESSED_DATA_PATH}ratings.csv', index=False)


if __name__ == "__main__":
    df1 = pd.read_csv(f'{RAW_DATA_PATH}name.basics.tsv', sep='\t')
    df2 = df1.copy()
    process_actors(df1)
    process_directors(df2)

    df1 = pd.read_csv(f'{RAW_DATA_PATH}title.basics.tsv', sep='\t')
    process_movies(df1)

    df1 = pd.read_csv(f'{RAW_DATA_PATH}title.principals.tsv', sep='\t')
    df2 = df1.copy()
    process_movies_actors(df1)
    process_movies_directors(df2)

    df1 = pd.read_csv(f'{RAW_DATA_PATH}title.ratings.tsv', sep='\t')
    process_ratings(df1)