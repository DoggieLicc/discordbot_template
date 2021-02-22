import os, sys
try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

import discord
from discord.ext import commands

TOKEN = ""

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    print('Ready!')
    await client.change_presence(activity=discord.Game(name="Hello world!"))

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(TOKEN)
