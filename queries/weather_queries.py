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
                '''
}