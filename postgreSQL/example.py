# PostgreSQL driver
# opens database connections, sends SQL queries, receives results
import psycopg2
# built-in Pyton csv module
import csv

# creates connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="Apartment Finder",
    user="postgres",
    password="mypassword",
    port=5432
)

# create a cursor object (what sends SQL commands)
cur = conn.cursor()

# execute() sends SQL to PostgreSQL

# create a table
# table structure: id SERIAL PRIMARY KEY
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    name TEXT
)
""")

# insert a row
cur.execute("INSERT INTO users(name) VALUES(%s)", ("Alice",))

# save changes
conn.commit()

# runs a SELECT query
# * means all columns
cur.execute("SELECT * FROM users")
# retrieve query results
rows = cur.fetchall()

for row in rows:
    print(row) # each row is a tuple

# open csv file
# with open("data.csv", newline="") as f:
#     reader = csv.reader(f)
#     next(reader) # skip a row (the header usually)

#     for row in reader:
#         address = row[0] # accessing individual columns
#         price = int(row[1])
#         bedrooms = int(row[2])

#         print(address, price, bedrooms)

cur.close() # close cursor
conn.close() # close database connection