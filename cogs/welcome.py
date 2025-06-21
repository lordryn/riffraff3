import discord
from discord.ext import commands
from config.config import Config

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.create_dm()
            await member.dm_channel.send(
                f"Hi {member.name}, welcome to the Misfit Marauders! If you have any problems or suggestions just message me and choose the related option."
            )
        except:
            pass

        channel = self.bot.get_channel(Config.WELCOME_CHANNEL_ID)
        runebot_channel = self.bot.get_channel(953105638559469599)
        ely_channel = self.bot.get_channel(961447651998580766)
        shake_channel = self.bot.get_channel(1064354681314361344)
        event_cal_channel = self.bot.get_channel(961058348436963398)
        leaderboard_channel = self.bot.get_channel(Config.LEADERBOARD_CHANNEL_ID)
        weekly_channel = self.bot.get_channel(Config.WEEKLY_CHANNEL_ID)
        citadel_channel = self.bot.get_channel(Config.ANNOUNCEMENT_CHANNEL_ID)
        faqs_channel = self.bot.get_channel(1065406928907423915)

        msg = f"""Hello {member.mention}, welcome to our Discord server! We are happy to have you here.

Feel free to join in on any events we have going on - you can find them under the events section of our discord {event_cal_channel.mention}. The calendar is pinned.

We also have 4 discord bots:
- {runebot_channel.mention} for GE price/stats
- {ely_channel.mention} & {shake_channel.mention} for player-to-player trade prices
- Our custom AI bot <@966117247355605012> that manages {leaderboard_channel.mention}, {weekly_channel.mention}, {citadel_channel.mention} and more.

See {faqs_channel.mention} for help. Use `!ticket <message>` in DM to open a support ticket.
"""
        await channel.send(msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == Config.RULES_MESSAGE_ID:
            guild = self.bot.get_guild(payload.guild_id)
            member = payload.member or guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=947331981027450891)
            if member:
                await member.add_roles(role)
                dir_name = f"Members/{member.id}({member.name})"
                print(f"new mem accept -> {dir_name}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
