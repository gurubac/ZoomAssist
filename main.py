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


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AUTH = os.getenv('AUTHORIZATION')

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
    result = [new['personal_meeting_url'], new['first_name'], new['last_name'], new['created_at']]
    return result


def createMeeting():
    conn = http.client.HTTPSConnection("api.zoom.us")

    payload = "{\"topic\": \"test meeting\"}"

    headers = {
        #test
        'authorization': "Bearer " + AUTH,
        'content-type': "application/json"
        }

    conn.request("POST", "/v2/users/me/meetings", payload, headers)

    res = conn.getresponse()
    data = res.read()

    y = data.decode("utf-8")
    print(y)
    new = json.loads(y)
    result = [new['join_url']]
    return result



    

bot = commands.Bot(
    command_prefix = ('.'),
    help_command=None
    )
bot.remove_command('help')
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)



id = bot.get_guild(GUILD)

@bot.group(
    invoke_without_command=True
)
async def help(ctx):
    embed = discord.Embed(title = "help", description = "Use .help <command> for extended information")
    embed.add_field(name = "Normal Commands", value = "meeting, status, schedule")
    if ctx.message.author.server_permissions.administrator:
        embed.add_field(name = "Administrator Commands", value = "setschedule, setTime")
    await ctx.send(embed = embed)

@help.command()
async def meeting(ctx):
    embed = discord.Embed(title = "__Meeting__", description = "Generates a Zoom meeting link.", color = ctx.author.color)
    embed.add_field(name = "**Syntax:**", value = "!meeting  -  Sets meeting time to default time.\n!meeting <subject>  -  Sets meeting time to subject's scheduled timeframe.")
    await ctx.send(embed = embed)

@help.command()
async def status(ctx):
    embed = discord.Embed(title = "__Status__", description = "Checks status of Zoom meeting.",color = ctx.author.color)
    embed.add_field(name = "**Syntax:**", value = "!status")
    await ctx.send(embed = embed)

@help.command()
async def schedule(ctx):
    embed = discord.Embed(title = "__Schedule__", description = "Displays schedule for meetings.",color = ctx.author.color)
    embed.add_field(name = "**Syntax:**", value = "!zoomschedule  - lists entire schedule.\n!zoomschedule <subject>  -  lists schedule for specified subject.")
    await ctx.send(embed = embed)

@help.command()
async def setschedule(ctx):
    embed = discord.Embed(title = "__Set Schedule__", description = "For Admins only.\nModify planned schedule for Zoom meetings.",color = ctx.author.color)
    embed.add_field(name = "**Syntax:**", value = ".setschedule")
    await ctx.send(embed = embed)

@help.command()
async def settime(ctx):
    embed = discord.Embed(title = "__Set Time__", description = "For Admins only.\nSet default meeting time for Zoom meetings.",color = ctx.author.color)
    embed.add_field(name = "**Syntax:**", value = ".setTime")
    await ctx.send(embed = embed)

@bot.command(
    aliases=["setschedule", "sets", "changeschedule", "changesched", "setSchedule", "setS"] 
)
async def echo(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Enter and add a schedule for your Zoom meetings!\nMake sure to include the course and timeframes!\nEx): Math1A, MTWRF, 2:30, 3:30",
        description="This request will __time out__ in 1 minute!",
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
            rows = sched.split(',')
            print(rows)
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([rows])
            return sched
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout.", delete_after=15)

global default
@bot.command()
async def setTime(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Enter a **single** default time frame for your Zoom meetings!\nPlease Use Hour and Minute Fornat!\nEx): 2:30, 0:50, ,1:45, etc.",
        description="This request will __time out__ in 20 seconds!",
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=20,
            check= lambda message: message.author == ctx.author and message.channel == ctx.channel
        ) 
        if msg:
            await sent.delete()
            await msg.delete()
            await ctx.send("Set default meeting time to: " + msg.content)
            # global defaultTime 
            defaultTime = ((msg.content)+":00")
            defaultTimeObj = datetime.datetime.strptime(defaultTime.strip(), '%H:%M:%S')
            default = ((defaultTimeObj.hour*3600) + (defaultTimeObj.minute*60) + (defaultTimeObj.second))
            saveTime = open('time.txt', 'w')
            saveTime.write(str(default))
            saveTime.close()
            return default
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout.", delete_after=15)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

live = False
@bot.event
async def on_message(message):
    global live
    global e
    global elapsedTime
    global originalTimeInSec
    global meetingTime

    await bot.process_commands(message)
    
    if live == False:
        if message.content.startswith("!meeting"):
            collection = createMeeting()

            await message.channel.send("Hello! Please wait, your Zoom meeting link is being generated!")
            time.sleep(2)
            await message.channel.send(collection[0])
            with open('data.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)

                timeFormat = '%H:%M:%S'
                for row in reader:
                    if row[0] in message.content:

                        stringStartTime = str(row[2]+":00")
                        stringEndTime = str(row[3]+":00")
                        startTimeObj = datetime.datetime.strptime(stringStartTime.strip(), timeFormat)
                        endTimeObj = datetime.datetime.strptime(stringEndTime.strip(), timeFormat)

                        meetingTime = (((endTimeObj.hour - startTimeObj.hour)*3600)+((endTimeObj.minute-startTimeObj.minute)*60)+(endTimeObj.second-startTimeObj.second))

                    elif (row[0] not in message.content and message.content==("!meeting")):
                        getTime = open('time.txt','r')
                        temp = getTime.readline()
                        meetingTime = int(temp)
                        getTime.close()
                        break

            live = True

            e = datetime.datetime.now()

            originalTimeInSec = (e.hour * 3600) + (e.minute * 60) + e.second
        elif message.content == ("!status"):
            await message.channel.send(f"There are no ongoing meetings.")

    elif live == True:

        global currentTimeInSec
        current = datetime.datetime.now()
        currentTimeInSec = (current.hour * 3600) + (current.minute * 60) + current.second

        sec = (currentTimeInSec - originalTimeInSec)
        ty_res = time.gmtime(sec)
        res = time.strftime("%H:%M:%S",ty_res)


        newTimeInSec = ((e.hour)*3600) + ((e.minute)*60) + (e.second) + meetingTime
        if live:
            if (currentTimeInSec > newTimeInSec):
                live = False
            elif (currentTimeInSec <= newTimeInSec):
                elapsedTime = "This meeting has been live for " + str(res)
                if message.content == ("!status"):
                    if (currentTimeInSec <= newTimeInSec):
                        await message.channel.send(elapsedTime)

    if message.content == ("!stop"):
        await bot.close()
    elif message.content.startswith("!zoomschedule"):
        with open('data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                if row[0] in message.content:
                    await message.channel.send(f"Here is your meeting details in the order of subject, date, start/end time!")
                    await message.channel.send(f'\t`Subject: {row[0].strip()} - Days: {row[1].strip()} - Start Time: {row[2].strip()} - End Time: {row[3].strip()} `')
                elif row[0] not in message.content and message.content==("!zoomschedule"):
                    await message.channel.send(f'\t`Subject: {row[0]} - Days: {row[1]} - Start Time: {row[2]} - End Time: {row[3]} `')
                    for line in reader:
                        await message.channel.send(f'\t`Subject: {line[0]} - Days: {line[1]} - Start Time: {line[2]} - End Time: {line[3]} `')
                    

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)