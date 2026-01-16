import mysql.connector

def create_tables(conn):
    cursor = conn.cursor()

    # Actors
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Actors (
                actor_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Actors table: {e}")
        raise

    # Movies
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Movies (
                movie_id VARCHAR(20) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                start_year INT,
                genres VARCHAR(255)
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Movies table: {e}")
        raise
    
    # Directors
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Directors (
                director_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Directors table: {e}")
        raise

    # Movies-Actors
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Movies_Actors (
                movie_id VARCHAR(20),
                actor_id VARCHAR(20),
                characters VARCHAR(255),
                PRIMARY KEY (movie_id, actor_id, characters),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                FOREIGN KEY (actor_id) REFERENCES Actors(actor_id)
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Movies_Actors table: {e}")
        raise

    # Movies-Directors
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Movies_Directors (
                movie_id VARCHAR(20),
                director_id VARCHAR(20),
                PRIMARY KEY (movie_id, director_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                FOREIGN KEY (director_id) REFERENCES Directors(director_id)
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Movies_Directors table: {e}")
        raise

    # Ratings
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ratings (
                movie_id VARCHAR(20) PRIMARY KEY,
                average_rating FLOAT,
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
            );
        """)
    except mysql.connector.Error as e:
        print(f"Error creating Ratings table: {e}")
        raise

    try:
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error committing transaction: {e}")
        raise

def create_indices(conn):
    cursor = conn.cursor()

    statements = [
        # Full-text indices
        "ALTER TABLE Actors ADD FULLTEXT(name);",
        "ALTER TABLE Movies ADD FULLTEXT(genres);",
        "ALTER TABLE Movies_Actors ADD FULLTEXT(characters);",
        # Join / aggregation indices
        "CREATE INDEX idx_movies_actors_actor_id ON Movies_Actors(actor_id);",
        "CREATE INDEX idx_movies_actors_movie_id ON Movies_Actors(movie_id);",
        "CREATE INDEX idx_movies_directors_movie_id ON Movies_Directors(movie_id);",
        "CREATE INDEX idx_movies_directors_director_id ON Movies_Directors(director_id);",
        "CREATE INDEX idx_ratings_average_rating ON Ratings(average_rating);"
    ]

    for stmt in statements:
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as e:
            print(f"Index creation skipped or failed for statement: {stmt} - Error: {e}")

    try:
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error committing index creation: {e}")
        raise


def main():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3305,
            user='username',
            password='password',
            database='database_name'
        )
        print("Successfully connected to database.")
        create_tables(conn)
        create_indices(conn)
        print("Database setup completed successfully.")
    except mysql.connector.Error as e:
        print(f"Database error in main: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()