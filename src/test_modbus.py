
import asyncio
from pymodbus.client import AsyncModbusTcpClient


async def main():
    client = AsyncModbusTcpClient("127.0.0.1", port=5020)

    connected = await client.connect()

    if not connected:
        print("Could not connect to the Modbus device.")
        return

    print("Connected to Modbus device!")

    result = await client.read_holding_registers(
        address=0,
        count=3,
        device_id=1,
    )

    if result.isError():
        print("Error reading registers:", result)
    else:
        print("Modbus register values:", result.registers)
        print("Register 0: Average power (scaled by 1000)")
        print("Register 1: Demand (scaled by 1000)")
        print("Register 2: Energy (scaled by 1000)")

    client.close()


asyncio.run(main())
