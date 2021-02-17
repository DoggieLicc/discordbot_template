import os, sys, time
os.chdir(os.path.dirname(sys.argv[0]))

import discord
from discord.ext import commands

TOKEN = ""

client = commands.Bot(command_prefix = '.')
client.change_presence(activity=discord.Game(name="Hello world!"))

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(TOKEN)
