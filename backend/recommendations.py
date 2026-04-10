import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sqlalchemy import create_engine

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

def recommend_apartments(csv_path, index):
    engine = create_engine('postgresql://postgres:1Oscar2006@localhost:5432/oscar')
    similarity_df = pd.read_sql_table('recommendations', con=engine)

    
    df = clean_data(csv_path)

    bedrooms = df.iloc[index,4]
    filtered_df = df[df["Bedrooms"] == bedrooms].drop_duplicates("Name")

    similar_apartments = similarity_df.iloc[index,filtered_df.index.values]
    ordered_apartments = similar_apartments.sort_values()[1:]
    id_list = []
    for key, val in ordered_apartments.items():
        id_list.append(int(key[3:]))
    id_list
    df = df.iloc[id_list, :]

    return df.iloc[:5, 0]

if __name__ == "__main__":
    print(recommend_apartments("backend/umn_apartment_data.csv", 0))
