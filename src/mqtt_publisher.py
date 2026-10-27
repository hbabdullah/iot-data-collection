
import json
import time
from pathlib import Path

import pandas as pd
import paho.mqtt.client as mqtt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed_energy.csv"

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/energy/telemetry"

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    # Read a small sample instead of loading the whole processed dataset.
    df = pd.read_csv(DATA_PATH, nrows=20)

    if df.empty:
        raise ValueError("No processed energy readings were found.")

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="industrial-energy-publisher",
    )

    print(f"Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}...")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        for _, row in df.iterrows():
            payload = {
                "asset_id": str(row["asset_id"]),
                "timestamp": str(row["time"]),
                "avg_power_kw_15m": float(row["avg_power_kw_15m_total"]),
                "demand_kw": float(row["demand_kw_total"]),
                "energy_kwh_15m": float(row["energy_kwh_15m_total"]),
                "source": "real_industrial_energy_dataset",
            }

            result = client.publish(
                MQTT_TOPIC,
                json.dumps(payload),
                qos=1,
            )
            result.wait_for_publish()

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print("Publish failed:", result.rc)
            else:
                print("Published:", json.dumps(payload))

            time.sleep(1)

    finally:
        client.loop_stop()
        client.disconnect()

    print("MQTT publishing finished.")

if __name__ == "__main__":
    main()
