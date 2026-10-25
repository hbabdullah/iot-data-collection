
import pandas as pd
from database import connect_db

# Read electricity data from the CSV file
data = pd.read_csv("data/electricity.csv")

# Connect to PostgreSQL
connection = connect_db()

try:
    with connection.cursor() as cursor:
        for _, row in data.iterrows():
            cursor.execute(
                """
                INSERT INTO electricity_readings
                    (timestamp, voltage, current, power)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row["timestamp"],
                    row["voltage"],
                    row["current"],
                    row["power"],
                ),
            )

    connection.commit()
    print(f"Successfully saved {len(data)} readings to PostgreSQL!")

finally:
    connection.close()
