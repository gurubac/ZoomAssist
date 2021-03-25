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
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@client.event
async def on_message(message):
    id = client.get_guild(GUILD)


    if message.content.find("!hello") != -1:
        await message.channel.send("Hi")
    elif message.content == ("!stop"):
        await client.close()



client.run(TOKEN)