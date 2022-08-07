# package imports
import pgeocode
import streamlit as st
import pandas as pd
import numpy as np
# local imports
from models.db_model import db_model
from queries.weather_queries import WEATHER_QUERIES as queries

db = db_model()

def get_lag_long():
    nomi = pgeocode.Nominatim('us')
    query_results = db.run_sql(queries['GET_POSTAL_CODES'])
    postal_codes = [postal_code[0] for postal_code in query_results]
    place_map = {}
    lat_long_arr = []
    for postal_code in postal_codes:
        current_place = nomi.query_postal_code(postal_code)
        if 'latitude' not in list(current_place.keys()) or 'longitude' not in list(current_place.keys()):
            continue 
        if pd.isna(current_place['latitude']) is True or pd.isna(current_place['longitude']) is True:
            continue
        place_map[postal_code] = current_place
        curr_lat_long = []
        curr_lat_long.append(current_place.latitude)
        curr_lat_long.append(current_place.longitude)
        lat_long_arr.append(np.array(curr_lat_long))
    return place_map, np.array(lat_long_arr)

def main():
    db.run_sql(queries['USE_DB'], print_results=True)
    st.title('US Weather Forecasts')
    place_map, lat_long_arr = get_lag_long()
    df = pd.DataFrame(lat_long_arr, columns=['lat', 'lon'])
    #print(df.head())
    st.map(df)
    # for i in place_map:
    #     print(place_map[i])
    
    # df = pd.DataFrame(
    #  np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    #  columns=['lat', 'lon'])
    # print(df.head())
    # st.map(df)


if __name__ == '__main__':
    main()
