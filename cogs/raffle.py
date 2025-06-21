import random
import sqlite3
from discord.ext import commands
from config.config import Config
from utils.logger import Logger

class Raffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def raffle(self, ctx):
        msg_id = ctx.message.reference.message_id
        chan = ctx.channel
        msg = await chan.fetch_message(msg_id)

        users = set()
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.add(user.id)

        contestants = list(users)
        if not contestants:
            await ctx.send("No contestants found.")
            return

        winner = random.choice(contestants)
        result = f"Out of {len(contestants)} contestants, <@{winner}> has won the raffle!"
        await ctx.send(result)
        Logger.log(contestants)
        Logger.log(result)

    @commands.command()
    async def contestants(self, ctx):
        con = sqlite3.connect(Config.RAFFLE_DB_FILE)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM Name")
        entries = cursor.fetchall()
        con.close()

        names = [f'<@{name[0]}>' for name in entries]
        Logger.log(f"Contestants: {names}")
        await ctx.send("Contestants:\n" + "\n".join(names))

async def setup(bot):
    await bot.add_cog(Raffle(bot))
