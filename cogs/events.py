import discord
from discord.ext import commands, tasks
from config.config import Config
from utils.logger import Logger
from datetime import datetime, time as dt_time, timezone
import pytz
import json
from pathlib import Path

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TIMEZONE = pytz.timezone(Config.TIMEZONE)
        self.scheduled_day = 1
        self.scheduled_time = dt_time(hour=2, minute=0, tzinfo=timezone.utc)

        self.send_daily_reset.start()
        self.send_weekly_reset.start()
        self.send_weekly_announcement.change_interval(time=self.scheduled_time)
        self.send_weekly_announcement.start()

    @commands.Cog.listener()
    async def on_ready(self):
        Logger.log(f"{self.bot.user} has connected to Discord!")
        await self.bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Misfit Marauders"
        ))

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author == self.bot.user:
    #         return
    #     await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        Logger.log(f"{ctx.guild.name} > {ctx.author} > {ctx.command}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        Logger.log(f"Deleted: {message.content} by {message.author} in {message.channel}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            with open("leave.txt", "r") as f:
                leave_lines = f.readlines()
            channel = self.bot.get_channel(976928345897963600)
            msg = f"<@{member.id}> ({member.name}/{member.nick}) {random.choice(leave_lines)}"
            await channel.send(msg)
            Logger.log(f"{member.nick}->left")
        except Exception as e:
            Logger.log(f"on_member_remove error: {e}")

    @tasks.loop(minutes=1)
    async def send_daily_reset(self):
        now = datetime.utcnow()
        if now.hour == 0 and now.minute == 0:
            chan = self.bot.get_channel(Config.RESET_CHANNEL_ID)
            await chan.send("A daily reset has occurred!")

    @tasks.loop(minutes=1)
    async def send_weekly_reset(self):
        now = datetime.utcnow()
        if now.weekday() == 2 and now.hour == 0 and now.minute == 0:
            chan = self.bot.get_channel(Config.RESET_CHANNEL_ID)
            await chan.send("A weekly reset has occurred!")

    def load_raffle_config(self):
        try:
            with open(Path(Config.RAFFLE_CONFIG_FILE), 'r') as f:
                return json.load(f)
        except Exception as e:
            Logger.log(f"Failed to load raffle config: {e}")
            return {}

    def get_raffle_dates(self):
        now = datetime.now(self.TIMEZONE)
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(weeks=1)
        return start.strftime("%B %d, %Y"), end.strftime("%B %d, %Y")

    @tasks.loop(time=dt_time(hour=2, minute=0, tzinfo=timezone.utc))
    async def send_weekly_announcement(self):
        if datetime.now(timezone.utc).weekday() == self.scheduled_day:
            config = self.load_raffle_config()
            start_date, end_date = self.get_raffle_dates()
            try:
                msg = config["message"].format(
                    start_date=start_date,
                    end_date=end_date,
                    prize=config["prize"],
                    emoji=config["emoji"]
                )
                chan = self.bot.get_channel(Config.ANNOUNCEMENT_CHANNEL_ID)
                raffle_chan = self.bot.get_channel(Config.WEEKLY_CHANNEL_ID)
                if raffle_chan:
                    await raffle_chan.send(msg)
                if chan:
                    await chan.send("Weekly cit build tick! @everyone")
            except Exception as e:
                Logger.log(f"send_weekly_announcement failed: {e}")

async def setup(bot):
    await bot.add_cog(Events(bot))
