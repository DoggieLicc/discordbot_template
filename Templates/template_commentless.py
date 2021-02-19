import os, sys
os.chdir(os.path.dirname(sys.argv[0]))

import discord
from discord.ext import commands

TOKEN = ""

client = commands.Bot(command_prefix = '.')
await client.change_presence(activity=discord.Game(name="Hello world!"))
client.remove_command('help')

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(TOKEN)
