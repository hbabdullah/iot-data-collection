# IoT Data Collection System

## Project Description

This project demonstrates an IoT data collection pipeline using a real industrial electrical energy dataset. It processes energy measurements, publishes telemetry through MQTT, stores incoming data in PostgreSQL, and provides a simulated Modbus TCP device for reading measurement registers.

The project uses Python to demonstrate data processing, industrial communication protocols, persistent storage, and basic analysis.

## Features

- Processes real industrial energy data from a Parquet dataset.
- Converts selected energy measurements into a processed CSV file.
- Publishes telemetry messages using MQTT.
- Receives MQTT messages and stores them in PostgreSQL.
- Simulates a Modbus TCP device with holding registers.
- Reads and tests Modbus register values.
- Analyzes electricity readings and generates power graphs.

## Technologies Used

- Python
- Pandas
- PyArrow
- Paho MQTT
- Mosquitto MQTT broker
- PostgreSQL
- Psycopg
- Modbus TCP using PyModbus
- Matplotlib
- CSV and Parquet

## Project Structure

```text
iot-data-collection/
├── data/
│   ├── fact_energy_15m.parquet
│   ├── processed_energy.csv
│   └── electricity.csv
├── src/
│   ├── process_dataset.py
│   ├── mqtt_publisher.py
│   ├── mqtt_subscriber.py
│   ├── database.py
│   ├── modbus_device.py
│   ├── test_modbus.py
│   ├── main.py
│   ├── summary.py
│   ├── plot_data.py
│   ├── save_to_database.py
│   └── view_database.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

Install Python and PostgreSQL. Install and run a Mosquitto MQTT broker locally for MQTT communication.

Install the Python dependencies:

```bash
py -m pip install -r requirements.txt
```

Configure your PostgreSQL connection using a `.env` file in the project root. Do not commit database passwords or other secrets to GitHub.

Example `.env` structure:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iot_database
DB_USER=postgres
DB_PASSWORD=your_password
```

Replace `your_password` with your local PostgreSQL password.

## How to Run

Run the following commands from the project root directory.

### 1. Process the industrial dataset

```bash
py src/process_dataset.py
```

This reads the Parquet dataset and creates `data/processed_energy.csv`.

### 2. Start the MQTT subscriber

In one terminal:

```bash
py src/mqtt_subscriber.py
```

The subscriber listens on the topic `industrial/energy/telemetry` and stores received measurements in PostgreSQL.

### 3. Publish telemetry through MQTT

In a second terminal:

```bash
py src/mqtt_publisher.py
```

The publisher sends a sample of processed industrial energy measurements to the MQTT broker.

### 4. Start the simulated Modbus TCP device

In another terminal:

```bash
py src/modbus_device.py
```

The device listens on `127.0.0.1:5020`.

### 5. Test Modbus register reading

With the Modbus device running, execute:

```bash
py src/test_modbus.py
```

The test connects to the device and reads three holding registers.

### 6. Run the existing analysis tools

Main analysis:

```bash
py src/main.py
```

Summary:

```bash
py src/summary.py
```

Generate a graph:

```bash
py src/plot_data.py
```

Save the existing CSV readings to PostgreSQL:

```bash
py src/save_to_database.py
```

View the existing electricity readings:

```bash
py src/view_database.py
```

## MQTT Communication

- Broker: `127.0.0.1`
- Port: `1883`
- Topic: `industrial/energy/telemetry`
- Protocol: MQTT
- Quality of Service: QoS 1

Telemetry messages include the asset ID, timestamp, average power, demand, energy, and data source.

## PostgreSQL Database

The `industrial_telemetry` table stores:
A unique constraint prevents duplicate industrial readings from being stored when the same MQTT messages are published more than once.

| Column | Description |
|---|---|
| `id` | Unique record ID |
| `asset_id` | Industrial asset identifier |
| `timestamp` | Measurement timestamp |
| `avg_power_kw_15m` | Average power in kW |
| `demand_kw` | Demand in kW |
| `energy_kwh_15m` | Energy in kWh over 15 minutes |
| `source` | Data source |
| `received_at` | Database reception timestamp |

The project also contains an existing `electricity_readings` table for voltage, current, and power readings. Voltage and current are not provided by the industrial dataset used in the MQTT pipeline, so those fields remain empty for these records.

## Modbus TCP Register Mapping

The simulated device exposes three holding registers. Values are scaled by 1,000 and rounded to integers.

| Register | Measurement | Unit before scaling |
|---|---|---|
| 0 | Average power | kW |
| 1 | Demand | kW |
| 2 | Energy | kWh |

The Modbus server uses port `5020` to avoid requiring the privileged default port.

## Dataset

The project uses the industrial energy dataset hosted on Hugging Face:

https://huggingface.co/datasets/renumics/industrial-asset-level-electrical-energy-dataset

The selected signals include total energy, total demand, and average power. These measurements come from the real dataset; the Modbus device is simulated.

## Security and Limitations

- Keep `.env` and database credentials private.
- The MQTT broker and Modbus device are configured for local testing.
- The Modbus server simulates a device rather than connecting to physical industrial equipment.
- Voltage, current, and temperature are not claimed as measured values from the selected industrial dataset.

## Project Status

The dataset processing, MQTT publishing, PostgreSQL storage, and Modbus register reading have been tested locally.
