import os
import sys

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except OSError:
    pass

import discord
import json
from discord.ext import commands

with open('config.json') as config:
    secrets = json.load(config)

intents = discord.Intents.default()
intents.members = secrets['MEMBER_INTENTS']
intents.presences = secrets['PRESENCE_INTENTS']

bot = commands.Bot(case_insensitive=True, command_prefix=secrets['DEFAULT_PREFIX'], intents=intents,
                   activity=discord.Game(name='Hello World!'))

bot.secrets = secrets
bot.default_prefix = secrets['DEFAULT_PREFIX']
bot.prefixes = {}

if __name__ == '__main__':
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')

bot.run(bot.secrets['BOT_TOKEN'], bot=True, reconnect=True)
