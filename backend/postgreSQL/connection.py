import psycopg2

# connect to database
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="read8511",
        port=5432
    )