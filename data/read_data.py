
import pandas as pd

file_path = "data/electricity.csv"

data = pd.read_csv(file_path)

print("Electricity Data:")
print(data)

print("\nAverage Voltage:", round(data["voltage"].mean(), 2), "V")
print("Average Current:", round(data["current"].mean(), 2), "A")
print("Average Power:", round(data["power"].mean(), 2), "W")
