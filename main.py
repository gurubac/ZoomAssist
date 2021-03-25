import os
import discord
from dotenv import load_dotenv

#new comment
#another comment

load_dotenv()
#load_dotenv('---.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()
#print(TOKEN)
@client.event
async def on_ready():
    print(f'Bot is Online.')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@client.event
async def on_message(message):
    #id = client.get_guild(GUILD)
    if message.content.startswith("!hello") != -1:
        await message.channel.send("Hi")
    elif message.content.startswith('!zoom m'):
        #if there are no meetings at specific time
            await message.channel.send(f'There are currently no Zoom meetings.')
        #if there are meetings at specific time
    elif message.content.startswith('!zoom s'):
        await message.channel.send(f'Your scheduled Zoom meeting is on ')
    elif message.content == ("!stop"):
        await client.close()




client.run(TOKEN)