import psycopg2
import csv

# connect to database
conn = psycopg2.connect(
    host="localhost",
    database="Apartment Finder",
    user="postgres",
    password="mypassword",
    port=5432
)

cur = conn.cursor() # create cursor

# create table if doesn't exist already
cur.execute("""
CREATE TABLE IF NOT EXISTS apartments(
    id SERIAL PRIMARY KEY,
    address TEXT
    price INTEGER
    bedrooms SMALLINT
    bathrooms SMALLINT
    area INT
    availability_date DATE
    link TEXT
    amenities TEXT[]
)
""")

# open csv file and copy into postgresql
with open("properties.csv", "r") as f:
    cur.copy_expert(
        """
        COPY properties(address,price,bedrooms,bathrooms,area,availability_date,link,amenities)
        FROM STDIN WITH CSV HEADER
        """,
        f
    )

conn.commit()
cur.close()
conn.close()