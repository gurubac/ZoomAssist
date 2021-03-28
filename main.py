import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import subprocess
import pyautogui
import time
import pandas as pd
import datetime
import requests
import json
import http.client
import asyncio
import csv

#bot = commands.Bot(command_prefix=".")

load_dotenv()
#load_dotenv('---.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AUTH = os.getenv('AUTHORIZATION')
#DISCORDCHANNEL = os.getenv('DISCORD_CHANNEL')

isMeetingLive = None

def myInfo():
    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer " + AUTH,
        'content-type': "application/json"
        }

    conn.request("GET", "https://api.zoom.us/v2/users/me", headers=headers)

    res = conn.getresponse()
    data = res.read()
    
    y = data.decode("utf-8")
    new = json.loads(y)
    #print(type(y))
    #print(y)
    result = [new['personal_meeting_url'], new['first_name'], new['last_name'], new['created_at']]
    return result


def createMeeting():
    conn = http.client.HTTPSConnection("api.zoom.us")

    #payload = "{\"topic\":\"string\",\"type\":\"integer\",\"start_time\":\"string [date-time]\",\"duration\":\"integer\",\"schedule_for\":\"string\",\"timezone\":\"string\",\"password\":\"string\",\"agenda\":\"string\",\"recurrence\":{\"type\":\"integer\",\"repeat_interval\":\"integer\",\"weekly_days\":\"string\",\"monthly_day\":\"integer\",\"monthly_week\":\"integer\",\"monthly_week_day\":\"integer\",\"end_times\":\"integer\",\"end_date_time\":\"string [date-time]\"},\"settings\":{\"host_video\":\"boolean\",\"participant_video\":\"boolean\",\"cn_meeting\":\"boolean\",\"in_meeting\":\"boolean\",\"join_before_host\":\"boolean\",\"mute_upon_entry\":\"boolean\",\"watermark\":\"boolean\",\"use_pmi\":\"boolean\",\"approval_type\":\"integer\",\"registration_type\":\"integer\",\"audio\":\"string\",\"auto_recording\":\"string\",\"enforce_login\":\"boolean\",\"enforce_login_domains\":\"string\",\"alternative_hosts\":\"string\",\"global_dial_in_countries\":[\"string\"],\"registrants_email_notification\":\"boolean\"}}"
    payload = "{\"topic\": \"test meeting\"}"

    headers = {
        'authorization': "Bearer " + AUTH,
        'content-type': "application/json"
        }

    conn.request("POST", "/v2/users/me/meetings", payload, headers)

    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))

    y = data.decode("utf-8")
    print(y)
    new = json.loads(y)
    result = [new['join_url']]
    return result

#createMeeting()


    

#myInfo()

#discord getting info
#client = discord.Client()
#bot = discord.Client()
bot = commands.Bot(command_prefix=".")
#channel = client.get_channel(DISCORDCHANNEL)
id = bot.get_guild(GUILD)
#print(channel)
#print(id)

@bot.command(
    aliases=["setschedule", "sets", "changeschedule", "changesched", "setSchedule", "setS"]
)
async def echo(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Set the schedule for your Zoom meetings!\nMake sure to type in all courses and timeslots!\nEx: Math1A: MTWRF 9am-1030am, Math1B: TR 5pm-7pm",
        description="This request will time out in 1 minute!",
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=59,
            check= lambda message: message.author == ctx.author and message.channel == ctx.channel
        ) 
        if msg:
            await sent.delete()
            await msg.delete()
            await ctx.send(msg.content)
            global sched 
            sched = (msg.content)
            print(sched)
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([sched])
            return sched
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout.", delete_after=15)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    # print(
    #     f'{client.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})\n'
    # )

# @client.event
# async def on_message(message):
#     if message.content.find("!hello") != -1:
#         await message.channel.send("Hi")
#     elif message.content == ("!stop"):
#         await client.close()

#collection = myInfo()
#collection = createMeeting()
#print(collection)
#print(type(collection))

# @bot.event
# async def on_message(message):
#     await bot.process_commands(message)
#     if message.content.find("!meeting") != -1:
#         await message.channel.send("Hello " + collection[1] + " " + collection[2] + ", here is your zoom link created at " + collection[3] + "!")
#         time.sleep(2)
#         await message.channel.send(collection[0])
#     elif message.content == ("!stop"):
#         await bot.close()
#     elif message.content.startswith("!zoom s"):
#         f = open('schedule.txt', 'r')
#         await message.channel.send(f"Your scheduled Zoom meetings are on: " + f.read())


live = False
@bot.event
async def on_message(message):
    global live
    global e
    global elapsedTime
    global originalTimeInSec
    await bot.process_commands(message)
    
    if live == False:
        if message.content.find("!meeting") != -1:
            collection = createMeeting()
            #await message.channel.send("Hello " + collection[1] + " " + collection[2] + ", here is your zoom link created at " + collection[3] + "!")
            await message.channel.send("Hello! Please wait, your Zoom meeting link is being generated!")
            time.sleep(2)
            await message.channel.send(collection[0])
            #time.sleep(2)
            #await message.channel.send(collection[0])
            live = True
            # start = datetime.datetime.now().time()
            # print(start)
            e = datetime.datetime.now()
            #print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
            #print(e.hour)
            #convert original time to seconds
            originalTimeInSec = (e.hour * 3600) + (e.minute * 60) + e.second
        elif message.content == ("!status"):
            await message.channel.send(f"There are no ongoing meetings.")

    elif live == True:
        # if message.content == ("!status"):
        #     await message.channel.send(elapsedTime)
            #await ctx.channel.send(elapsedTime)
        # newHour = e.hour + 2
        # newMinute = e.minute + 30
        # newSecond = e.second + 30

        global currentTimeInSec
        current = datetime.datetime.now()
        currentTimeInSec = (current.hour * 3600) + (current.minute * 60) + current.second

        sec = (currentTimeInSec - originalTimeInSec)
        ty_res = time.gmtime(sec)
        res = time.strftime("%H:%M:%S",ty_res)

        # if message.content == ("!status"):
        #     await message.channel.send(f"There are no ongoing meetings.")

        newTimeInSec = ((e.hour)*3600) + ((e.minute)*60) + (e.second+3)
        if live:
            if (currentTimeInSec > newTimeInSec):
                live = False
                # if message.content == ("!status"):
                #     await message.channel.send(f"There are no currently meetings.")

            elif (currentTimeInSec <= newTimeInSec):
                
                # elapsedHour = newHour - current.hour
                # elapsedMinute = newMinute - current.minute
                # elapsedSecond = newSecond - current.second

                #convert current time to seconds
                # currentTimeInSec = (current.hour * 3600) + (current.minute * 60) + current.second

                # sec = (currentTimeInSec - originalTimeInSec)
                # ty_res = time.gmtime(sec)
                # res = time.strftime("%H:%M:%S",ty_res)

                elapsedTime = "This meeting has been live for " + str(res)
                #print(elapsedTime)
                if message.content == ("!status"):
                    if (currentTimeInSec <= newTimeInSec):
                        await message.channel.send(elapsedTime)

    if message.content == ("!stop"):
        await bot.close()
    elif message.content.startswith("!zoom s"):
        #flag = True
        specials = '"'
        with open('data.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                row = [value.replace(specials, '') for value in row]
                row = str(row)
                writer = csv.writer(csvfile)
                writer.writerow([row])
                print(row[0])
                if row[0] in message.content:
                    await message.channel.send(f"Here is your meeting details in the order of subject, date, start/end time!")
                    await message.channel.send(row)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)