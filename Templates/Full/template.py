# Change current working directory to script "home" directory
# Important if going to use files or custom modules
import os, sys, time

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

# Import discord.py and its commands module'
import discord, json, time
from discord.ext import commands

# Token for discord bot
TOKEN = ""

# For unique prefixes per server
def get_prefix(client, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return "$"
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

# Removes default help command
client.remove_command("help")

# Event that triggers on error
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

# When bot joins server set a default prefix
@client.event
async def on_guild_join(guild):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "$"
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)


# When bot joins server remove prefix from json
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


# Event that triggers when bot is ready
@client.event
async def on_ready():
    # Set the bot's status on discord
    await client.change_presence(activity=discord.Game(name="Hello world!"))
    print("Ready!\n")


# Event that triggers when message is sent
@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        # If bot is pinged, respond with set prefix
        if isinstance(message.channel, discord.channel.DMChannel):
            embed = discord.Embed(
                title="Pinged!",
                description="The set prefix is $",
                color=0xFFFFFE,
            )
            await message.channel.send(embed=embed)
            return
        try:
            embed = discord.Embed(
                title="Pinged!",
                description="The set prefix is {}".format(get_prefix(client,
                message)),
                color=0xFFFFFE,
            )
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

# Command that sets prefix for a server
@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, prefix):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    # If trying to set same prefix, respond with error
    if (prefixes[str(ctx.guild.id)]) == prefix:
        await embed_send(
            ctx, "Error!", 'Prefix is already "{}"'.format(prefix), 0xFF3232
        )
        return
    prefixes[str(ctx.guild.id)] = prefix
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, sort_keys=True, indent=2)
    await embed_send(ctx, "Prefix set!", 'Prefix set to "{}"'.format(prefix))


# Function to respond to commands with embeds
async def embed_send(ctx, title, description, color=0xFFFFFE):
    embed = discord.Embed(description=description, title=title, color=color)
    # Footer that shows user that sent the command
    embed.set_footer(
        text="Command sent by {}".format(ctx.author),
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=embed)


# Command that lists all commands in "commands.json"
@client.command()
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

# Runs bot using token
try:
    client.run(TOKEN)
except:
    print("Token is missing or incorrect!")
    time.sleep(60)
