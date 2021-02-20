# Change current wordking directory to script "home" directory
# Important if going to use files or custom modules
import os, sys
try: 
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

# Import discord.py and its commands module'
import discord
from discord.ext import commands

# Token for discord bot
TOKEN = ""

# Replace the . to use different prefix for commands
client = commands.Bot(command_prefix = '.')

# Set the bot's status on discord, and removes default help command
client.remove_command('help')

# Event that triggers when bot is ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Hello world!'))
    print('Ready!')

# To process commands
@client.event
async def on_message(message):
    await client.process_commands(message)

# Runs bot using token
client.run(TOKEN)
