import mysql.connector
from queries_db_script import query_1, query_2, query_3, query_4, query_5, query_6

def main():
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost',
        port=3305,
        user='username',
        password='password',
        database='database_name'
    )

    # Full-text examples
    
    print("Query 1: Movies with genre 'Action'")
    result = query_1(conn, 'Action')
    for row in result:
        print(row[0].strip(','))
    print()

    print("Query 2: Actors who played character 'Robert'")
    result = query_2(conn, 'Robert')
    for row in result:
        print(row[0].strip(','))
    print()

    print("Query 3: Find movie by actor's name 'Stephen'")
    result = query_3(conn, 'Stephen')
    for row in result:
        print(f"{row[0].strip(',')} - {row[1].strip(',')}")
    print()

    # ----- Example usage of complex queries -----
    
    print("Query 4: Top 5 most prolific actors")
    result = query_4(conn, 5)
    for row in result:
        print(row[0].strip(','))
    print()

    print("Query 5: Top 5 actor-director collaborations")
    result = query_5(conn, 5)
    for row in result:
        print(f"{row[0].strip(',')} - {row[1].strip(',')} ({row[2]})")
    print()

    print("Query 6: Actors in above-average rated movies")
    result = query_6(conn)
    for row in result:
        print(row[0].strip(','))
    print()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
