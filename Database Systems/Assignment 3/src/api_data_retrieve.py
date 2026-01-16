import csv
import mysql.connector

def insert_actors(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [(row['nconst'], row['primaryName']) for row in reader]

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Actors (actor_id, name) VALUES (%s, %s)",
        rows
    )
    conn.commit()

def insert_movies(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            genres = row['genres'] if row['genres'] else ''
            start_year = int(row['startYear']) if row['startYear'] else None
            rows.append((row['tconst'], row['primaryTitle'], start_year, genres))

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Movies (movie_id, title, start_year, genres) VALUES (%s, %s, %s, %s)",
        rows
    )
    conn.commit()

def insert_movies_actors(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            characters = row.get('characters', '')
            if characters == r'\N' or not characters.strip():
                characters = ''
            rows.append((row['tconst'], row['nconst'], characters))

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Movies_Actors (movie_id, actor_id, characters) VALUES (%s, %s, %s)",
        rows
    )
    conn.commit()

def insert_directors(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [(row['nconst'], row['primaryName']) for row in reader]

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Directors (director_id, name) VALUES (%s, %s)",
        rows
    )
    conn.commit()

def insert_movies_directors(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [(row['tconst'], row['nconst']) for row in reader]

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Movies_Directors (movie_id, director_id) VALUES (%s, %s)",
        rows
    )
    conn.commit()

def insert_ratings(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            avg_rating = float(row['averageRating']) if row['averageRating'] else None
            rows.append((row['tconst'], avg_rating))

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Ratings (movie_id, average_rating) VALUES (%s, %s)",
        rows
    )
    conn.commit()


def main():
    conn = mysql.connector.connect(
        host='localhost',
        port=3305,
        user='username',
        password='password',
        database='database_name'
    )

    DATA_PATH = 'data/filtered_data/filtered_'

    insert_actors(conn, f'{DATA_PATH}actors.csv')
    insert_movies(conn, f'{DATA_PATH}movies.csv')
    insert_movies_actors(conn, f'{DATA_PATH}movies_actors.csv')
    insert_directors(conn, f'{DATA_PATH}directors.csv')
    insert_movies_directors(conn, f'{DATA_PATH}movies_directors.csv')
    insert_ratings(conn, f'{DATA_PATH}ratings.csv')

    conn.close()

if __name__ == "__main__":
    main()
