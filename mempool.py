import discord
import requests
import asyncio
from datetime import datetime
# Replace 'TOKEN' with your actual bot token
TOKEN = ''
FEES_API_URL = 'https://mempool.space/api/v1/fees/recommended'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def update_activity():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            response = requests.get(FEES_API_URL)
            data = response.json()
            fastest_fee = data.get('fastestFee')
            half_hour_fee = data.get('halfHourFee')
            hour_fee = data.get('hourFee')

            now = datetime.now()
            print(f"{now} - fastestFee: {fastest_fee}, halfHourFee: {half_hour_fee}, hourFee: {hour_fee}")

            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f" {fastest_fee} sat |  {half_hour_fee} sat |  {hour_fee} sat"
            )
            await client.change_presence(activity=activity)
        except Exception as e:
            now = datetime.now()
            print(f"{now} - Error fetching fees data: {e}")
        
        # Update every 1 seconds
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print(f'Bot is ready as {client.user}')

client.loop.create_task(update_activity())
client.run(TOKEN)