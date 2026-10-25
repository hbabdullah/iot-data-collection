
import time
import random
from datetime import datetime

print("IoT Electricity Data Simulator Started")

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    voltage = round(random.uniform(220, 240), 2)
    current = round(random.uniform(1, 10), 2)
    power = round(voltage * current, 2)

    print(
        f"Time: {timestamp} | "
        f"Voltage: {voltage} V | "
        f"Current: {current} A | "
        f"Power: {power} W"
    )

    time.sleep(3)
