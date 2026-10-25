import pandas as pd
from datetime import datetime
from pathlib import Path

print("Welcome to the IoT Data Collection System!")
print("System is starting...")
print("Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 40)

file_path = Path("data/electricity.csv")

if file_path.exists():
    data = pd.read_csv(file_path)
else:
    print("Error: Electricity data file not found.")
    exit()

print("\nElectricity Data:")
print("Here are the collected electricity readings:")
print(data)
print("\n--- Average Results ---")
print("\nAverage Power:", round(data["power"].mean(), 2), "W")
print("Average Voltage:", round(data["voltage"].mean(), 2), "V")
print("Average Current:", round(data["current"].mean(), 2), "A")
print("Missing power readings:", data["power"].isnull().sum())
print("Missing voltage readings:", data["voltage"].isnull().sum())
print("Missing current readings:", data["current"].isnull().sum())
print("Total electricity readings:", len(data))
print("Highest Power:", data["power"].max(), "W")
print("Lowest Power:", data["power"].min(), "W")
print("Power Range:", round(data["power"].max() - data["power"].min(), 2), "W")
print("\nSystem check completed successfully!")