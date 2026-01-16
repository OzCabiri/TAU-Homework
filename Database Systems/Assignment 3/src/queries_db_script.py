import mysql.connector

def query_1(conn, genre):
    """
    Full-text search: Find movies with a certain genre
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT title
            FROM Movies
            WHERE MATCH(genres) AGAINST (%s IN NATURAL LANGUAGE MODE)
        """
        cursor.execute(sql, (genre,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_1: {e}")
        raise
    finally:
        cursor.close()

def query_2(conn, character_name):
    """
    Full-text search: Find actors who played a certain character
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT DISTINCT a.name
            FROM Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            WHERE MATCH(ma.characters) AGAINST (%s IN NATURAL LANGUAGE MODE)
        """
        cursor.execute(sql, (character_name,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_2: {e}")
        raise
    finally:
        cursor.close()

def query_3(conn, actor_name):
    """
    Full-text search: Find a movie by actor's name
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT a.name, m.title
            FROM Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            Join Movies m ON ma.movie_id = m.movie_id
            WHERE MATCH(a.name) AGAINST (%s IN NATURAL LANGUAGE MODE)
        """
        cursor.execute(sql, (actor_name,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_3: {e}")
        raise
    finally:
        cursor.close()

def query_4(conn, N):
    """
    Complex Query: Find the top N actors with the most movie appearances
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT a.name, COUNT(*) AS movie_count
            FROM Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            GROUP BY a.actor_id
            ORDER BY movie_count DESC
            LIMIT %s
        """
        cursor.execute(sql, (N,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_4: {e}")
        raise
    finally:
        cursor.close()

def query_5(conn, N):
    """
    Complex Query: Find the top N  actor-director collaborations
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT a.name, d.name, COUNT(*) AS collaborations
            FROM Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            JOIN Movies_Directors md ON ma.movie_id = md.movie_id
            JOIN Directors d ON md.director_id = d.director_id
            GROUP BY a.actor_id, d.director_id
            ORDER BY collaborations DESC
            LIMIT %s
        """
        cursor.execute(sql, (N,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_5: {e}")
        raise
    finally:
        cursor.close()

def query_6(conn):
    """
    Complex Query: Find actors who played in above-average rated movies
    """
    cursor = conn.cursor()
    try:
        sql = """
            SELECT DISTINCT a.name
            FROM Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            JOIN Ratings r ON ma.movie_id = r.movie_id
            WHERE r.average_rating > (
            SELECT AVG(average_rating) FROM Ratings
            )
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error in query_6: {e}")
        raise
    finally:
        cursor.close()
