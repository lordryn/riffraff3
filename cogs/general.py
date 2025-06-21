from discord.ext import commands
from utils.logger  import Logger
from config.config import Config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def halp(self, ctx):
        cmds = """```Riff Raff Raffler by Lord Ryn
Designed for the Misfit Marauders Discord

<-general->
!halp - this menu (list of commands)
!raffle - chooses a user that reacts to a post (must reply to target)
!poll <amount> - 2 adds thumbs up/down, 3–10 uses number emojis
!leaderboard - shows top 20 from the leaderboard

<-community->
!bonghit, !pushups, !sendnoods, !dothedew, !hydrate, !barehug

<-admin->
!clear <amount>, !echo
```"""
        await ctx.send(cmds)

    @commands.command()
    async def poll(self, ctx, options: int):
        if options < 2 or options > 10:
            await ctx.send("Please choose between 2 and 10 options.")
            return

        emojis = {
            2: ['\N{THUMBS UP SIGN}', '\N{THUMBS DOWN SIGN}'],
            3: ["1️⃣", "2️⃣", "3️⃣"],
            4: ["1️⃣", "2️⃣", "3️⃣", "4️⃣"],
            5: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"],
            6: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"],
            7: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"],
            8: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"],
            9: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"],
            10: ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        }.get(options, [])

        for emoji in emojis:
            await ctx.message.add_reaction(emoji)

    @commands.command()
    async def clear(self, ctx, amount):
        await ctx.message.delete()
        Logger.log(f"{ctx.author}>clear>{amount}>{ctx.channel}")
        await ctx.message.channel.purge(limit=int(amount))

    @commands.command(description="Echos, developers only", pass_context=True)
    async def echo(self, ctx, echo_words: str):
        if ctx.author.id in Config.DEV_IDS:
            await ctx.send(echo_words)
        else:
            await ctx.send("Bot developers only :<")
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(General(bot))