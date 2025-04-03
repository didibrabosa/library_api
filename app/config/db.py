import psycopg2


def get_db_connection():
    db_connection = psycopg2.connect(
        host="library_database",
        database="library",
        user="admin",
        password="password",
        port=5432
    )
    return db_connection
