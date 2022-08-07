from models.db_model import db_model
from queries.weather_queries import WEATHER_QUERIES as queries

def main():
    db = db_model()
    db.run_sql(queries['USE_DB'], print_results=True)
    

if __name__ == '__main__':
    main()
