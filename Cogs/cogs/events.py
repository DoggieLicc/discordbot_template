import discord
from discord.ext import commands

import asqlite


async def load_prefixes(bot):
    bot.prefixes = {}
    async with asqlite.connect('data.db', check_same_thread=False) as conn:
        async with conn.cursor() as cursor:
            for row in await cursor.execute('SELECT guild, prefix FROM prefixes'):
                bot.prefixes[row[0]] = row[1]
            await cursor.close()
        await conn.close()


def g_prefix(bot, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return bot.default_prefix
    return bot.prefixes.get(message.guild.id, bot.default_prefix)


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.prefixes = {}
        bot.load_prefixes = load_prefixes
        bot.g_prefix = g_prefix
        bot.command_prefix = g_prefix
        print('EventsCog init')

    @commands.Cog.listener()
    async def on_ready(self):
        await load_prefixes(self.bot)
        print(f'\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n')
        print(f'Successfully logged in and booted...!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == f'<@!{self.bot.user.id}>' or message.content == f'<@{self.bot.user.id}>':
            set_prefix = g_prefix(self.bot, message)
            embed = discord.Embed(title=f'Pinged!', description=f'The set prefix is `{set_prefix}`', color=0x46ff2e)
            embed.set_footer(
                text='Command sent by {}'.format(message.author),
                icon_url=message.author.avatar_url,
            )
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(EventsCog(bot))
