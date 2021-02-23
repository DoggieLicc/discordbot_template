import os, sys, time

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

import discord, json, time
from discord.ext import commands


TOKEN = ""

def get_prefix(client, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return "$"
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

client.remove_command("help")

def get_uptime():
    return round(time.time() - startTime)

@client.event
async def on_command_error(ctx, error):
    print('{}: {}\n{}\n'.format(ctx.message.author, ctx.message.content, error))
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await embed_send(ctx, "Error!",'That command doesn\'t exist!', 0xFF3232)
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await embed_send(ctx,"Error!",'Missing arguments in command!', 0xFF3232)
    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await embed_send(ctx, "Error!",
            'You don\'t have permission(s) "{}" to do that command!' \
            .format(','.join(error.missing_perms)), 0xFF3232)
    elif isinstance(error, discord.ext.commands.NoPrivateMessage):
        await embed_send(ctx, "Error!",
            'You can\'t run this command in a private message!', 0xFF3232)
    else:
        pass

@client.event
async def on_guild_join(guild):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "$"
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)


@client.event
async def on_guild_remove(guild):
    try:
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f, sort_keys=True, indent=2)
    except:
        pass


@client.event
async def on_ready():
    global startTime
    await client.change_presence(activity=discord.Game(name="Hello world!"))
    print("Ready!\n")
    startTime = time.time()


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        try:
            get_prefix(client, message)
        except:
            with open("json/prefixes.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(message.guild.id)] = "$"
            with open("json/prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=2)
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
    try:
        await client.process_commands(message)
    except:
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(message.guild.id)] = "$"
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)
        await client.process_commands(message)

@client.command(aliases=["prefix"])
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
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
        text="Command sent by {}".format(ctx.author),
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=embed)


@client.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Help:", color=0x00FF40)
    with open("json/commands.json", "r") as f:
        commands = json.load(f)
    for key, value in commands.items():
        embed.add_field(name=key, value=value, inline=False)
    embed.set_author(name="Discord Bot!")
    embed.set_footer(
        text="Command sent by {}".format(ctx.author),
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=embed)

@client.command(aliases=["ping"])
async def info(ctx):
    embed=discord.Embed(title='Info', color=0x00FF40)
    embed.add_field(name='Bot Creator:',
        value=\
        '[DoggieLicc](https://github.com/DoggieLicc/discord.py_templates)',
        inline=Fals
    embed.add_field(name='Bot Uptime:',
        value='{} seconds'.format(get_uptime()), inline=False)
    embed.add_field(name='Ping:',
        value='{} ms'.format(round(1000*(client.latency)), inline=False))
    embed.set_footer(text="Command sent by {}".format(ctx.message.author),
        icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

try:
    client.run(TOKEN)
except:
    print("Token is missing or incorrect!")
    time.sleep(60)
