import json
from datetime import datetime

import paho.mqtt.client as mqtt

from database import connect_db

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/energy/telemetry"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker!")
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"Listening to topic: {MQTT_TOPIC}")
    else:
        print(f"MQTT connection failed: {reason_code}")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        timestamp = datetime.fromisoformat(data["timestamp"])

        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS industrial_telemetry (
                        id BIGSERIAL PRIMARY KEY,
                        asset_id TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        avg_power_kw_15m DOUBLE PRECISION,
                        demand_kw DOUBLE PRECISION,
                        energy_kwh_15m DOUBLE PRECISION,
                        source TEXT,
                        received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )

                cursor.execute(
                    """
                    INSERT INTO industrial_telemetry (
                        asset_id,
                        timestamp,
                        avg_power_kw_15m,
                        demand_kw,
                        energy_kwh_15m,
                        source
                    )
                                        VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (asset_id, timestamp, avg_power_kw_15m, demand_kw, energy_kwh_15m)
                    DO NOTHING
                    """,
                    (
                        data["asset_id"],
                        timestamp,
                        data["avg_power_kw_15m"],
                        data["demand_kw"],
                        data["energy_kwh_15m"],
                        data.get("source", "unknown"),
                    ),
                )

        print(
            f"Saved to PostgreSQL: {data['asset_id']} "
            f"| power={data['avg_power_kw_15m']} kW"
        )

    except Exception as error:
        print(f"Could not save message: {error}")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="industrial-energy-subscriber-test-2",
    )

    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}...")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    print("Subscriber running. Press Ctrl+C to stop.")
    client.loop_forever()


if __name__ == "__main__":
    main()