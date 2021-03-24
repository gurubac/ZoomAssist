import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


keep_alive()
client.run(os.getenv('TOKEN'))