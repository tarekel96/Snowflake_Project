import os
from dotenv import load_dotenv
from snowflake.connector import connect

class db_model():
        # constructor
        def __init__(self) -> None:
                load_dotenv()
                self.username = os.environ.get('SNOWFLAKE_USERNAME')
                self.password = os.environ.get('SNOWFLAKE_PASSWORD')
                self.account = os.environ.get('SNOWFLAKE_ACCOUNT')
                self.db_connection = connect(
                        user=self.username,
                        password=self.password,
                        account=self.account
                )
                self.cursor = self.db_connection.cursor()
        
        # private methods
        def _get_db_con(self):
                return self.db_connection
        def _get_db_cursor(self):
                return self.cursor
        # public methods
        def run_sql(self, query, single_row=False, print_results=False):
                exe = self.cursor.execute(query)
                if print_results is True:
                        print(f"Execution: {exe}")
                if single_row is True:
                        result = self.cursor.fetchone()
                        if print_results is True:
                                print(f"Result: {result}")
                        return result
                results = self.cursor.fetchall()
                if print_results is True:
                        print(f"Results: {results}")
                return results
