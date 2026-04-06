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

# create properties table if doesn't exist already
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

# create temporary staging table in order to filter duplicates
cur.execute("""
CREATE TEMP TABLE staging_table(
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

# open csv file and copy into temp table
with open("test_insert.csv", "r") as f:
    cur.copy_expert(
        """
        COPY staging_table(building_name,unit_name,address,beds,baths,rent,sqft,availability,url,amenities)
        FROM STDIN WITH CSV HEADER
        """,
        f
    )

# set conflict constraint to determine duplicates
# executes anonymous code block and ensure that constraint doesn't already exist
cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'unique_property'
        ) THEN
            ALTER TABLE properties
            ADD CONSTRAINT unique_property UNIQUE (url);
        END IF;
    END $$;
""")

# upsert from temp table into properties table
# if there are conflicts, update the row instead of making a new one
cur.execute("""
    INSERT INTO properties (
    building_name, unit_name, address, beds, baths,
    rent, sqft, availability, url, amenities
    )
    SELECT
        building_name, unit_name, address, beds, baths,
        rent, sqft, availability, url, amenities
    FROM staging_table
    ON CONFLICT (url)
    DO UPDATE SET
        building_name = EXCLUDED.building_name,
        unit_name = EXCLUDED.unit_name,
        address = EXCLUDED.address,
        beds = EXCLUDED.beds,
        baths = EXCLUDED.baths,
        rent = EXCLUDED.rent,
        sqft = EXCLUDED.sqft,
        availability = EXCLUDED.availability,
        amenities = EXCLUDED.amenities
    WHERE (
        properties.building_name,
        properties.unit_name,
        properties.address,
        properties.beds,
        properties.baths,
        properties.rent,
        properties.sqft,
        properties.availability,
        properties.amenities
    ) IS DISTINCT FROM (
        EXCLUDED.building_name,
        EXCLUDED.unit_name,
        EXCLUDED.address,
        EXCLUDED.beds,
        EXCLUDED.baths,
        EXCLUDED.rent,
        EXCLUDED.sqft,
        EXCLUDED.availability,
        EXCLUDED.amenities
    );
""")

cur.execute("SELECT * FROM properties")
rows = cur.fetchall()
for row in rows:
    print(row) # each row is a tuple

conn.commit()
cur.close()
conn.close()