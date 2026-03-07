import time
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
            df.iloc[idx, 5] = pd.to_numeric(value[1:end_id])
        except:
            df.iloc[idx, 5] = None
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
        #can use a rotating api key to bypass rate limit - but need something that uses api keys
        
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


def recommend_apartments(csv_path, name):
    df = clean_data(csv_path)
    
    id = df[df["Name"] == name].index[0] #choosing the id of the apartment you want to find recommendations for
    req = df.iloc[id,3] #grabbing # of bedrooms in given id

    #defining df of all numeric values that has the same amount of bedrooms as a given id
    matching_df = df[df['Bedrooms'] == req].copy().drop_duplicates("Address")
    matching_df = matching_df[['Address', 'Bedrooms', 'Bathrooms', 'Size', 'Price']]

    distance_df = find_distance(matching_df)

    #adding weights
    distance_df["Bathrooms"] *= 5
    distance_df["Price"] /= 25
    distance_df["Size"] /= 500
    distance_df["Distance"] *= 40

    #calculating similarity using euclidean distance
    user_similarity = euclidean_distances(distance_df[["Bedrooms", "Bathrooms", "Size", "Price", "Distance"]])

    #finding similar apartments to given id
    similar_apartments = user_similarity[id]

    similar_apartments_indices = np.argsort(similar_apartments)[1:] #shows most similar apartments (ignoring the apartment itself)
    similar_apartments = distance_df.index[similar_apartments_indices] #grabbing indexes of similar apartments

    rec_df = df.loc[distance_df.loc[similar_apartments]["index"]]

    #creating csv file with all info on recommended apartments
    rec_df.to_csv("recommendations.csv")

    return rec_df["Name"][:5]

if __name__ == "__main__":
    print(recommend_apartments("umn_apartment_data.csv", "The Quad on Delaware"))