import psycopg2
import csv

# connect to database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="read8511",
    port=5432
)

cur = conn.cursor() # create cursor

# create table if doesn't exist already
cur.execute("""
CREATE TABLE IF NOT EXISTS properties(
    id SERIAL PRIMARY KEY,
    building_name TEXT,
    unit_name TEXT,
    address TEXT,
    beds SMALLINT,
    baths SMALLINT,
    rent INTEGER,
    sqft INT,
    availability DATE,
    url TEXT,
    amenities TEXT
)
""")

# open csv file and copy into postgresql
with open("umn_apartment_data.csv", "r") as f:
    cur.copy_expert(
        """
        COPY properties(building_name,unit_name,address,beds,baths,rent,sqft,availability,url,amenities)
        FROM STDIN WITH CSV HEADER
        """,
        f
    )

cur.execute("SELECT * FROM properties")
rows = cur.fetchall()
for row in rows:
    print(row) # each row is a tuple

conn.commit()
cur.close()
conn.close()