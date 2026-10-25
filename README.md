# IoT Data Collection System

## Project Description
This project simulates electricity readings, stores and analyzes the data, and visualizes power measurements using Python.

## Features
- Simulated electricity readings
- CSV data storage
- PostgreSQL database storage
- Database connection and data retrieval
- Average voltage, current, and power calculations
- Highest and lowest power calculations
- Power range calculation
- Missing data checks
- Power readings graph

## Technologies Used
- Python
- Pandas
- Matplotlib
- PostgreSQL
- MQTT library (Paho MQTT)
- CSV

## How to Run

Run the main analysis program:

```bash
py src\main.py
```

Run the summary program:

```bash
py src\summary.py
```

Run the electricity simulator:

```bash
py iot_simulator.py
```

Run the graph program:

```bash
py src\plot_data.py
```

Save CSV readings to PostgreSQL:

```bash
py src\save_to_database.py
```

View readings stored in PostgreSQL:

```bash
py src\view_database.py
```
