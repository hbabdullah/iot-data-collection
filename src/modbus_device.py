
import asyncio
from pathlib import Path

import pandas as pd
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed_energy.csv"

HOST = "127.0.0.1"
PORT = 5020


def scaled_value(row, column):
    value = row.get(column, 0)
    if pd.isna(value):
        return 0
    return max(0, min(65535, round(float(value) * 1000)))


async def main():
    df = pd.read_csv(DATA_PATH, nrows=1)

    if df.empty:
        raise ValueError("The processed energy dataset is empty.")

    row = df.iloc[0]

    # Provide enough registers for the three measurements.
    registers = [
        scaled_value(row, "avg_power_kw_15m_total"),
        scaled_value(row, "demand_kw_total"),
        scaled_value(row, "energy_kwh_15m_total"),
    ]

    device = ModbusDeviceContext(
       hr=ModbusSequentialDataBlock(1, registers)
    )
    context = ModbusServerContext(devices=device, single=True)

    print("Simulated industrial Modbus TCP device")
    print(f"Asset: {row['asset_id']}")
    print(f"Listening on {HOST}:{PORT}")
    print("Holding registers: 0=average power, 1=demand, 2=energy")
    print("Register values are scaled by 1000.")
    print("Press Ctrl+C to stop.")

    await StartAsyncTcpServer(
        context=context,
        address=(HOST, PORT),
    )


if __name__ == "__main__":
    asyncio.run(main())
