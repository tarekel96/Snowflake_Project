import os
from dotenv import load_dotenv
from snowflake.connector import connect

load_dotenv()

username = os.environ.get('SNOWFLAKE_USERNAME')
password = os.environ.get('SNOWFLAKE_PASSWORD')
account = os.environ.get('SNOWFLAKE_ACCOUNT')


con = connect(
    user=username,
    password=password,
    account=account
)

print(con)