import os
import discord
from dotenv import load_dotenv

load_dotenv()
#load_dotenv('---.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
#print(TOKEN)
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)