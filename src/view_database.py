
import pandas as pd
from database import connect_db

connection = connect_db()

try:
    query = """
        SELECT id, timestamp, voltage, current, power
        FROM electricity_readings
        ORDER BY timestamp;
    """

    data = pd.read_sql_query(query, connection)

    print("\nElectricity Readings from PostgreSQL")
    print("=" * 70)
    print(data.to_string(index=False))
    print("=" * 70)
    print(f"Total readings: {len(data)}")

finally:
    connection.close()
