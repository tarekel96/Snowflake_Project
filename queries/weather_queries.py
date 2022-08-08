WEATHER_QUERIES = {
    'USE_DB': 
                '''
                USE WEATHERSOURCE_TILE_SAMPLE_SNOWFLAKE_SECURE_SHARE_1641488329256;
                ''',
    'GET_POSTAL_CODES': 
                '''    
                SELECT DISTINCT
                        POSTAL_CODE
                FROM 
                        standard_tile.forecast_day
                WHERE
                        COUNTRY = 'US';
                ''',
        'DATA_BY_POSTAL':'''
                SELECT DISTINCT 
                        POSTAL_CODE, AVG_TEMPERATURE_AIR_2M_F, AVG_HUMIDITY_RELATIVE_2M_PCT, AVG_PRESSURE_2M_MB, 
                        AVG_WIND_SPEED_10M_MPH, PROBABILITY_OF_PRECIPITATION_PCT, PROBABILITY_OF_SNOW_PCT
                FROM standard_tile.forecast_day
                WHERE COUNTRY = 'US';
                '''
}