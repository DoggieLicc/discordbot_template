import os, sys, time

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

import discord, json
from discord.ext import commands

TOKEN = "token_here"

def get_prefix(client, message):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

client.remove_command("help")

@client.event
async def on_guild_join(guild):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "!"
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)


@client.event
async def on_guild_remove(guild):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, sort_keys=True, indent=2)


@client.event
async def on_ready():
    # Set the bot's status on discord
    await client.change_presence(activity=discord.Game(name="Hello world!"))
    print("Ready!")


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        embed = discord.Embed(
            title="Pinged!",
            description="The set prefix is {}".format(get_prefix(client,
            message)),
            color=0xFFFFFE,
        )
        embed.set_footer(
            text="Command sent by {}".format(message.author),
            icon_url=message.author.avatar_url,
        )
        await message.channel.send(embed=embed)
    await client.process_commands(message)


@client.command(pass_context=True)
async def setprefix(ctx, prefix):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    if (prefixes[str(ctx.guild.id)]) == prefix:
        await embed_send(
            ctx, "Error!", 'Prefix is already "{}"'.format(prefix), 0xFF3232
        )
        return
    prefixes[str(ctx.guild.id)] = prefix
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, sort_keys=True, indent=2)
    await embed_send(ctx, "Prefix set!", 'Prefix set to "{}"'.format(prefix))


async def embed_send(ctx, title, description, color=0xFFFFFE):
    embed = discord.Embed(description=description, title=title, color=color)
    embed.set_footer(
        text="Command sent by {}".format(ctx.message.author),
        icon_url=ctx.message.author.avatar_url,
    )
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Help:", color=0x00FF40)
    with open("json/commands.json", "r") as f:
        commands = json.load(f)
        print(commands)
    for key, value in commands.items():
        embed.add_field(name=key, value=value, inline=False)
    embed.set_author(name="Discord Bot!")
    embed.set_footer(
        text="Command sent by {}".format(ctx.message.author),
        icon_url=ctx.message.author.avatar_url,
    )
    await ctx.send(embed=embed)


client.run(TOKEN)
