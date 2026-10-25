
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

file_path = Path("data/electricity.csv")

if not file_path.exists():
    print("Error: Electricity data file not found.")
else:
    data = pd.read_csv(file_path)

    plt.figure(figsize=(10, 5))
    plt.plot(data.index + 1, data["power"], marker="o")

    plt.title("Electricity Power Readings")
    plt.xlabel("Reading Number")
    plt.ylabel("Power (W)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("data/power_chart.png")
    plt.show()

    print("Graph saved to data/power_chart.png")
