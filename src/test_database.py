
from database import connect_db

try:
    connection = connect_db()
    print("Successfully connected to PostgreSQL!")
    connection.close()
except Exception as error:
    print("Connection failed:")
    print(error)
