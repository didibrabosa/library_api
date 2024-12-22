import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres_db",
        database="library",
        user="admin",
        password="password"
    )
    return conn