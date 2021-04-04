from discord.ext import commands

import discord
import asqlite


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('ExampleCog init')

    @commands.command()
    async def say(self, ctx, *, msg):
        """Repeats your message!"""

        await ctx.send(msg)

    @commands.command(aliases=['setprefix'])
    @commands.guild_only()
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    async def prefix(self, ctx, *, prefix):
        """Sets a custom prefix for a server! You need **Manage Server** permissions for this!"""

        async with asqlite.connect('data.db', check_same_thread=False) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('REPLACE INTO prefixes VALUES(?, ?)', (ctx.guild.id, prefix))
            await conn.commit()
        embed = discord.Embed(title='Custom prefix set!',
                              description=f'Custom prefix `{prefix}` has been set for {ctx.guild.name}!')
        await ctx.send(embed=embed)
        await self.bot.load_prefixes(self.bot)


def setup(bot):
    bot.add_cog(ExampleCog(bot))
