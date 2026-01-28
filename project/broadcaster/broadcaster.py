import os
import asyncio
import nats
import requests

DISCORD_URL = os.getenv("DISCORD_URL")
NATS_URL = os.getenv("NATS_URL")

async def main():
    nc = await nats.connect(NATS_URL)

    async def callback(msg):
        data = msg.data.decode()
        requests.post(DISCORD_URL, json={"content": data})

    await nc.subscribe("todos", cb=callback, queue="workers")
    await asyncio.Future()
    
asyncio.run(main())
