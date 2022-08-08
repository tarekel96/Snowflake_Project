# package imports
import enum
import pgeocode
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import sys
# local imports
from models.db_model import db_model
from queries.weather_queries import WEATHER_QUERIES as queries

db = db_model()

def get_lat_long():
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

def get_forecast_places():
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

def get_history_places():
    nomi = pgeocode.Nominatim('us')
    query_results = db.run_sql(queries['HIST_DATA_BY_POSTAL'])
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
        places[postal_code]['TOT_PRECIPITATION_IN'] = query_results[index][5]
        places[postal_code]['TOT_SNOWFALL_IN'] = query_results[index][6]
    return places

def st_plot_map():
    db.run_sql(queries['USE_DB'], print_results=True)
    st.title('US Weather Forecasts')
    lat_long_arr = get_lat_long()
    df = pd.DataFrame(lat_long_arr, columns=['lat', 'lon'])
    st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
    #  initial_view_state=pdk.ViewState(
    #      latitude=37.76,
    #      longitude=-122.4,
    #      zoom=11,
    #      pitch=50,
    #  ),
     layers=[
        #  pdk.Layer(
        #     'HexagonLayer',
        #     data=df,
        #     get_position='[lon, lat]',
        #     radius=200,
        #     elevation_scale=4,
        #     elevation_range=[0, 1000],
        #     pickable=True,
        #     extruded=True,
        #  ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
    ))

    #st.map(df)

def gen_forecast_csv() -> pd.DataFrame:
    db.run_sql(queries['USE_DB'], print_results=True)
    places = get_forecast_places()
    data = [np.array(list(places[i].values())) for i in places]
    columns = [i for i in list(places['19375'].keys())]
    df = pd.DataFrame(data, columns=columns)
    print(df.head())
    df.to_csv(sys.path[0] + '/data.csv')
    return df

def gen_hist_csv() -> pd.DataFrame:
    db.run_sql(queries['USE_DB'], print_results=True)
    places = get_history_places()
    data = [np.array(list(places[i].values())) for i in places]
    columns = [i for i in list(places[list(places.keys())[0]].keys())]
    df = pd.DataFrame(data, columns=columns)
    print(df.head())
    df.to_csv(sys.path[0] + '/data.csv')
    return df

def main():
    # history_df = gen_hist_csv()
    st_plot_map()

if __name__ == '__main__':
    main()
