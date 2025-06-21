import random
from discord.ext import commands
from utils.logger import Logger

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bonghit(self, ctx):
        ma_id = '<@1043352917312278528>'
        emoji = self.bot.get_emoji(977020269682106419)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'{ma_id} {ctx.author} has redeemed a bong hit!')
        Logger.log(f'{ctx.author}->bonghit ')

    @commands.command()
    async def barehug(self, ctx):
        dan_id = '<@936869866995068998>'
        emoji = self.bot.get_emoji(1044799777906364456)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'{dan_id}, {ctx.author} would like a bare hug!')
        Logger.log(f'{ctx.author}->barehug ')

    @commands.command()
    async def sendnoods(self, ctx):
        noods_id = '<@317156727877533699>'
        emoji = self.bot.get_emoji(1015359917135245335)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'Oh, the glorious {noods_id}, collector of clues, {ctx.author} summons you!')
        Logger.log(f'{ctx.author}->noods ')

    @commands.command()
    async def hydrate(self, ctx):
        nessa_id = '<@265980702175002634>'
        blu_id = '<@962502262285017109>'
        stck_id = '<@262638246838796299>'
        emoji = self.bot.get_emoji(1020245994941710366)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'{blu_id}, {stck_id}, and {nessa_id}  {ctx.author} says DRINK SOME WATER!')
        Logger.log(f'{ctx.author}->drink water ')

    @commands.command()
    async def dothedew(self, ctx):
        ryn_id = '<@275139099415937024>'
        emoji = self.bot.get_emoji(1041221122085105805)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f"{ryn_id}, {ctx.author} has Mountain Dew to fuel your ongoing battle with bot stability!")
        Logger.log(f'{ctx.author}->dew ')

    @commands.command()
    async def pushups(self, ctx):
        dan_id = '<@936869866995068998>'
        emoji = self.bot.get_emoji(962177233634594826)
        await ctx.message.add_reaction(emoji)

        try:
            with open('pushups.txt', 'r') as f:
                ids = f.readlines()
            names = ' '.join([line.strip() for line in ids])
            msg = f'{names} and {dan_id}, {ctx.author} has redeemed 5 Push Ups!'
            await ctx.send(msg)
            Logger.log(f'{ctx.author}->pushups ')
        except Exception as e:
            Logger.log(f'pushups command failed: {e}')

async def setup(bot):
    await bot.add_cog(Fun(bot))
