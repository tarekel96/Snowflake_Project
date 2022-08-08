# package imports
import enum
import pgeocode
import streamlit as st
import pandas as pd
import numpy as np
import sys
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
    return np.array(lat_long_arr)

def get_places():
    nomi = pgeocode.Nominatim('us')
    query_results = db.run_sql(queries['DATA_BY_POSTAL'])
    postal_codes = [postal_code[0] for postal_code in query_results]
    places = {}
    for index, postal_code in enumerate(postal_codes):
        current_place = nomi.query_postal_code(postal_code)
        if 'latitude' not in list(current_place.keys()) or 'longitude' not in list(current_place.keys()):
            continue 
        if pd.isna(current_place['latitude']) is True or pd.isna(current_place['longitude']) is True:
            continue
        current_place = dict(current_place)
        places[postal_code] = current_place
        # print(query_results[index])
        places[postal_code]['AVG_TEMPERATURE'] = query_results[index][1]
        places[postal_code]['AVG_HUMIDITY'] = query_results[index][2]
        places[postal_code]['AVG_PRESSURE'] = query_results[index][3]
        places[postal_code]['AVG_WIND_SPEED'] = query_results[index][4]
        places[postal_code]['PROBABILITY_PERCIPITATION'] = query_results[index][5]
        places[postal_code]['PROBABILITY_SNOW'] = query_results[index][6]
    return places

def st_plot_map():
    st.title('US Weather Forecasts')
    lat_long_arr = get_lag_long()
    df = pd.DataFrame(lat_long_arr, columns=['lat', 'lon'])
    st.map(df)

def main():
    db.run_sql(queries['USE_DB'], print_results=True)
    places = get_places()
    data = [np.array(list(places[i].values())) for i in places]
    columns = [i for i in list(places['19375'].keys())]
    for i in columns:
        print(i)
    df = pd.DataFrame(data, columns=columns)
    print(df.head())
    df.to_csv(sys.path[0] + '/data.csv')

if __name__ == '__main__':
    main()
