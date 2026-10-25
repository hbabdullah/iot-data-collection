
import pandas as pd
from pathlib import Path

file_path = Path("data/electricity.csv")

if file_path.exists():
    data = pd.read_csv(file_path)

    print("=== Electricity Data Summary ===")
    print("Total electricity readings:", len(data))
    print("Average Power:", round(data["power"].mean(), 2), "W")
    print("Average Voltage:", round(data["voltage"].mean(), 2), "V")
    print("Average Current:", round(data["current"].mean(), 2), "A")
    print("Highest Power:", data["power"].max(), "W")
    print("Lowest Power:", data["power"].min(), "W")
    print("Power Range:", round(data["power"].max() - data["power"].min(), 2), "W")

    print("\nSystem check completed successfully!")
else:
    print("Error: Electricity data file not found.")
