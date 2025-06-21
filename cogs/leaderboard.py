import ast
import pandas as pd
from lxml import html
from requests_html import AsyncHTMLSession
from tabulate import tabulate
from discord.ext import commands
from utils.logger import Logger

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        await ctx.send("Getting gains")
        url = 'http://localhost:42069/leaderboards-isRaw=%3CisRaw%3E'
        session = AsyncHTMLSession()
        page = await session.get(url)
        tree = html.fromstring(page.text)
        p_elements = tree.xpath('//p/text()')

        if not p_elements:
            await ctx.send("No data found")
            return

        try:
            data = pd.DataFrame(ast.literal_eval(p_elements[0]).items(), columns=['Member', 'Gains'])
            data.index += 1
            data['Gains'] = data['Gains'].astype(str)
            top_md = tabulate(data.head(50), headers='keys', tablefmt='plain', showindex=True)

            for chunk in [top_md[i:i + 1750] for i in range(0, len(top_md), 1750)]:
                await ctx.send(f"```Gains leaderboard:``````{chunk}```")

            await ctx.send("brought to you by Ryan at https://wcs.buisiness/portfolio \nrefreshes every saturday")
        except Exception as e:
            Logger.log(f"Leaderboard fetch failed: {e}")
            await ctx.send("Error loading leaderboard")

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
