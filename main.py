import asyncio
from collections import namedtuple
import signal
import discord
import os
import client
import config
import uptime

entries = []
for Login in config.ACCOUNTS:
    Entry = namedtuple('Entry', 'client, token')
    newClient = client.MyClient(Login.catching_channels)
    entries.append(
        Entry(client = newClient, token = Login.token)
    )
    

loop = asyncio.get_event_loop()
signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

uptime.keep_alive()

async def shutdown(signal, running_bots):
    print(f"Received exit signal {signal.name}...")
    [running_bot.cancel() for running_bot in running_bots]
    await asyncio.gather(*running_bots, return_exceptions=True)
    loop.stop()

async def wrapped_connect(entry):
    try:
        await entry.client.start(entry.token, bot = False)
        print('Logged in as {}'.format(entry))
    finally:
        print("Clean close of client")
        await entry.client.close()
        print('You are using the free version of the catcher by someone you know!')

try:
    running_bots = []
    for entry in entries:
        running_bots.append(loop.create_task(wrapped_connect(entry)))

    for s in signals:
        loop.add_signal_handler(s, lambda s = s: asyncio.create_task(shutdown(s, running_bots)))

    loop.run_forever()
finally:
    print('Program interruption')
    loop.close()
