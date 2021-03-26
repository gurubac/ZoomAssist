import os
import discord
from dotenv import load_dotenv
import subprocess
import pyautogui
import time
import pandas as pd
from datetime import datetime
import requests
import json
import http.client

load_dotenv()
#load_dotenv('---.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AUTH = os.getenv('AUTHORIZATION')
DISCORDCHANNEL = os.getenv('DISCORD_CHANNEL')

def myInfo():
    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer " + AUTH,
        'content-type': "application/json"
        }

    conn.request("GET", "https://api.zoom.us/v2/users/me", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def createMeeting():
    conn = http.client.HTTPSConnection("api.zoom.us")

    payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"recurrence\":{\"type\":\"integer\",\"repeat_interval\":\"integer\",\"weekly_days\":\"string\",\"monthly_day\":\"integer\",\"monthly_week\":\"integer\",\"monthly_week_day\":\"integer\",\"end_times\":\"integer\",\"end_date_time\":\"string [date-time]\"},\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\",\"cn_meeting\":\"boolean\",\"in_meeting\":\"boolean\",\"join_before_host\":\"boolean\",\"mute_upon_entry\":\"boolean\",\"watermark\":\"boolean\",\"use_pmi\":\"boolean\",\"approval_type\":\"integer\",\"registration_type\":\"integer\",\"audio\":\"string\",\"auto_recording\":\"string\",\"enforce_login\":\"boolean\",\"enforce_login_domains\":\"string\",\"alternative_hosts\":\"string\",\"global_dial_in_countries\":[\"string\"],\"registrants_email_notification\":\"boolean\"}}"
    #payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"recurrence\":{\"type\":\"integer\",\"repeat_interval\":\"integer\",\"weekly_days\":\"string\",\"monthly_day\":\"integer\",\"monthly_week\":\"integer\",\"monthly_week_day\":\"integer\",\"end_times\":\"integer\",\"end_date_time\":\"string [date-time]\"},\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\",\"cn_meeting\":\"boolean\",\"in_meeting\":\"boolean\",\"join_before_host\":\"boolean\",\"mute_upon_entry\":\"boolean\",\"watermark\":\"boolean\",\"use_pmi\":\"boolean\",\"approval_type\":\"integer\",\"registration_type\":\"integer\",\"audio\":\"string\",\"auto_recording\":\"string\",\"enforce_login\":\"boolean\",\"enforce_login_domains\":\"string\",\"alternative_hosts\":\"string\",\"global_dial_in_countries\":,\"registrants_email_notification\":\"boolean\"}}"

    headers = {
        'authorization': "Bearer " + AUTH,
        'content-type': "application/json"
        }

    conn.request("POST", "/v2/users/me/meetings", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

createMeeting()
#myInfo()

#discord getting info
client = discord.Client()
channel = client.get_channel(DISCORDCHANNEL)
id = client.get_guild(GUILD)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    # print(
    #     f'{client.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})\n'
    # )

@client.event
async def on_message(message):
    #id = client.get_guild(GUILD)
    str1 = str(message.author)
    if message.content.startswith("!hello"):
        await message.channel.send("Hi " + str1 + "!")
    elif message.content.startswith('!zoom m'):
        #if there are no meetings at specific time
            await message.channel.send(f'There are currently no live Zoom meetings.')
        #if there are meetings at specific time
            #await message.channel.send(f'A Zoom meeting is currently live!')
    elif message.content.startswith('!zoom s'):
        await message.channel.send(f'Your scheduled Zoom meetings are on ')
    elif message.content == ("!stop"):
        await client.close()


client.run(TOKEN)