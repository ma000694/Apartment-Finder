import time
import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from geopy.geocoders import Nominatim

def clean_data(csv_path):
    full_df = pd.read_csv(csv_path) #reading csv file

    #spliting dataframes between amenities and other data points
    df = full_df.iloc[:,:]
    amenities_df = full_df.iloc[:,9:]

    #loop through all amenities to put into 1 list
    temp_df = pd.DataFrame()
    for index, values in amenities_df.iterrows():
        my_list = [values.unique()[:-1]]
        temp_df = pd.concat([temp_df, pd.Series(my_list)], ignore_index = True) #adding list into dataframe in each iteration

    #recombining main df with modified amenities df
    df = pd.concat([df, temp_df], axis = 1, ignore_index = True)

    #renaming columns
    column_list = ["Name", "Floor Plan", "Address", "Bedrooms", "Bathrooms", "Price", "Size", "Availability", "Link", "Amenities", "AmenitiesID"]
    column_dic = {}
    for i in range(len(column_list)):
        column_dic[df.columns.values[i]] = column_list[i]

    df = df.rename(columns = column_dic)

        #replacing each value in Bedrooms column with numerical value
    idx = 0
    for value in df["Bedrooms"]:
        if value == "Studio":
            df.iloc[idx, 3] = "0"
        else:
            df.iloc[idx, 3] = value[0]
        idx += 1

    #replacing each value in Price column with numerical value
    idx = 0
    for value in df["Price"]:
        end_id = value.find("-")
        try:
            df.iloc[idx, 5] = pd.to_numeric(value[1:end_id], errors = 'coerce')
        except TypeError:
            df.iloc[idx, 5] = value[1:end_id]
        idx += 1

    # if price is not divided for each indivudal, do it manually
    ids = df[df["Price"] > 2000].index
    for id in ids:
        df.iloc[id, 5] /= pd.to_numeric(df.iloc[id, 3])

    #making each value numeric - if error occurs replaces value with NaN
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
    df['Bathrooms'] = pd.to_numeric(df['Bathrooms'], errors='coerce')
    df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors='coerce')

    df = df.dropna().reset_index(drop = True) #removing all none types

    return df


def find_distance(df):
    geolocator = Nominatim(user_agent="apartment-finder") 

    central_address = "207 Church Street SE, Minneapolis, MN 55455" #Lind Hall
    central_location = geolocator.geocode(central_address) #grabs location

    address_list = []

    lat_list = []
    long_list = []

    for address in df["Address"]:
        time.sleep(1) #Nominatim allow max 1 inquiry per second, prevents timeout error

        #if address is not already used grab the coordinates of the address
        if address not in address_list: 
            location = geolocator.geocode(address)
            address_list.append(address) #to check if it has been used
            
        try:
            lat_list.append(location.latitude)
            long_list.append(location.longitude)
        except (AttributeError): #will edit later
            lat_list.append(-1)
            long_list.append(-1)

    distance_list = []

    for i in range(len(lat_list)):
        distance = ((central_location.latitude - lat_list[i])**2 + (central_location.latitude - lat_list[i])**2)**0.5 #calculating distance between Lind Hall and given apartment
        distance_list.append(distance * 10**5 * 1.11 / 1609.34) #distance in miles

    distance_df = pd.concat([df.reset_index(), pd.Series(lat_list), pd.Series(long_list), pd.Series(distance_list)], axis=1)

    distance_df = distance_df[["index", "Bedrooms", "Bathrooms", "Size", "Price", 2]]
    distance_df.columns.values[-1] = "Distance"

    return distance_df

def create_similarilty_matrix(csv_path):
    df = clean_data(csv_path)

    distance_df = find_distance(df)

    #adding weights
    distance_df["Bathrooms"] *= 5
    distance_df["Price"] /= 25
    distance_df["Size"] /= 500
    distance_df["Distance"] *= 40

    #calculating similarity using euclidean distance
    user_similarity = euclidean_distances(distance_df[["Bedrooms", "Bathrooms", "Size", "Price", "Distance"]])
    print(len(user_similarity[0])) 

    temp_df = pd.DataFrame(user_similarity)
    temp_df.to_csv("similarity.csv", header=False, index=False)

    columns = ' FLOAT, '.join([str(i) for i in range(len(user_similarity[0] ))])

    upload_to_postgreSQL(columns, "similarity.csv")

    print("Similarity Matrix uploaded to database.")
    return None


def upload_to_postgreSQL(columns, csv_path):
    conn = psycopg2.connect(
        host="localhost",
        database="oscar",
        user="postgres",
        password="mypassword",
        port=5432
    )

    cur = conn.cursor()

    # columns is a string like '0 FLOAT, 1 FLOAT, ...'
    # We want to create a table with columns col0, col1, ...
    col_defs = ', '.join([f'col{i} FLOAT' for i in range(len(columns.split(",")))])
    cur.execute(f"""
    DROP TABLE recommendations;
    CREATE TABLE IF NOT EXISTS recommendations (
        {col_defs}
    )""")

    with open(csv_path, "r") as f:
        cur.copy_expert(
            f"COPY recommendations FROM STDIN WITH DELIMITER ','",
            f
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    print(create_similarilty_matrix("backend/umn_apartment_data.csv"))
