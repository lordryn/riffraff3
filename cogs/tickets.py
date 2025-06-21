import discord
from discord.ext import commands
from config.config import Config
from utils.logger import Logger

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx, *, message):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("This command can only be used in direct messages with the bot.")
            return

        guild = self.bot.get_guild(Config.SERVER_ID)
        category = discord.utils.get(guild.categories, name=Config.TICKET_CATEGORY_NAME)
        role = discord.utils.get(guild.roles, id=Config.TICKET_HANDLER_ROLE_ID)
        handlers = [r for r in guild.roles if r.name == Config.TICKET_HANDLER_ROLE_NAME]

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{ctx.author.id}",
            category=category,
            topic=f"Ticket from {ctx.author}",
            reason=f"Ticket init: {message}"
        )

        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
        for handler in handlers:
            await ticket_channel.set_permissions(handler, read_messages=True, send_messages=True)

        await ticket_channel.send(
            f"{ctx.author.mention} has initiated a ticket. {role.mention} please respond in this channel.\nMessage: {message}"
        )

async def setup(bot):
    await bot.add_cog(Tickets(bot))
