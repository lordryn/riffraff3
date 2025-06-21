import discord
from discord.ext import commands
from config.config import Config
from utils.logger import Logger

class RiffRaffBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=Config.BOT_PREFIX, intents=intents)

    async def setup_hook(self):
        Logger.log("Setting up bot...")

        # Load cogs
        for cog in [
            'cogs.general',
            'cogs.raffle',
            'cogs.fun',
            'cogs.tickets',
            'cogs.leaderboard',
            'cogs.admin',
            'cogs.welcome',
            'cogs.events'
        ]:
            try:
                await self.load_extension(cog)
                Logger.log(f"Loaded extension: {cog}")
            except Exception as e:
                Logger.log(f"Failed to load {cog}: {e}")
