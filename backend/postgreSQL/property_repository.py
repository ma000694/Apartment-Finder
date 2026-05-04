# this file handles all the SQL logic, communicating with the database

import csv

from .connection import get_connection
from .property_data_class import Property

csv_file = "test_insert.csv" # test declaration TODO:remember to remove
def insert_all_from_csv(csv_file):
    """Takes in a string parameter csv_file containing the name of the target csv file to insert into the database. Duplicate values are updated. Prints all rows upon completion."""
    
    conn = get_connection() # function to get connection
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
        amenities TEXT,
        UNIQUE (building_name, unit_name, address)
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
    with open(csv_file, "r") as f:
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
                ADD CONSTRAINT unique_property UNIQUE (building_name, unit_name, address);
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
        ON CONFLICT (building_name, unit_name, address)
        DO UPDATE SET
            beds = EXCLUDED.beds,
            baths = EXCLUDED.baths,
            rent = EXCLUDED.rent,
            sqft = EXCLUDED.sqft,
            availability = EXCLUDED.availability,
            url = EXCLUDED.url,
            amenities = EXCLUDED.amenities
        WHERE (
            properties.beds IS DISTINCT FROM EXCLUDED.beds
            OR properties.baths IS DISTINCT FROM EXCLUDED.baths
            OR properties.rent IS DISTINCT FROM EXCLUDED.rent
            OR properties.sqft IS DISTINCT FROM EXCLUDED.sqft
            OR properties.availability IS DISTINCT FROM EXCLUDED.availability
            OR properties.url IS DISTINCT FORM EXCLUDED.url
            OR properties.amenities IS DISTINCT FROM EXCLUDED.amenities
        )
    """)

    cur.execute("SELECT * FROM properties")
    rows = cur.fetchall()
    for row in rows:
        print(row) # each row is a tuple

    conn.commit()
    cur.close()
    conn.close()

def get_all_properties():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM properties")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def fetch_property(id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM table_name WHERE id = %s",(id,))
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    return results

def fetch_properties(ids_list):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM table_name WHERE id = ANY(%s)",(ids_list,))
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    return results

def insert_property(prop: Property):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO properties (
            building_name, unit_name, address,
            beds, baths, rent, sqft,
            availability, url, amenities
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (building_name, unit_name, address)
        DO UPDATE SET
            beds = EXCLUDED.beds,
            baths = EXCLUDED.baths,
            rent = EXCLUDED.rent,
            sqft = EXCLUDED.sqft,
            availability = EXCLUDED.availability,
            url = EXCLUDED.url,
            amenities = EXCLUDED.amenities
        WHERE (
            properties.beds IS DISTINCT FROM EXCLUDED.beds
            OR properties.baths IS DISTINCT FROM EXCLUDED.baths
            OR properties.rent IS DISTINCT FROM EXCLUDED.rent
            OR properties.sqft IS DISTINCT FROM EXCLUDED.sqft
            OR properties.availability IS DISTINCT FROM EXCLUDED.availability
            OR properties.url IS DISTINCT FORM EXCLUDED.url
            OR properties.amenities IS DISTINCT FROM EXCLUDED.amenities
        )
        RETURNING id;
    """, (
        prop.building_name,
        prop.unit_name,
        prop.address,
        prop.beds,
        prop.baths,
        prop.rent,
        prop.sqft,
        prop.availability,
        prop.url,
        prop.amenities
    ))

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()
    return new_id
#TODO maybe print functions for readability?