import sqlite3
import re
from discord.ext import commands
from tqdm.contrib import discord

from utils.logger import Logger

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "commands.db"

    @commands.command(name='newcmd')
    async def newcmd(self, ctx, cmd_name: str, *, args: str):
        pattern = r'"(.+?)"\s+"(.+?)"'
        match = re.fullmatch(pattern, args)
        if match:
            phrase = match.group(1)
            user_names = [u.strip() for u in match.group(2).split(',')]
        else:
            await ctx.send("Invalid format. Use: \"phrase\" \"user1, user2\"")
            return

        user_ids = []
        for name in user_names:
            member = discord.utils.get(ctx.guild.members, nick=name) or discord.utils.get(ctx.guild.members, name=name)
            if member:
                user_ids.append(str(member.id))

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS commands (name TEXT, phrase TEXT, user_ids TEXT)''')
        cur.execute('INSERT INTO commands VALUES (?, ?, ?)', (cmd_name, phrase, ','.join(user_ids)))
        con.commit()
        con.close()

        await ctx.send(f'Command {cmd_name} added.')

    @commands.command(name='commcmd')
    async def commcmd(self, ctx, cmd_name: str):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT * FROM commands WHERE name = ?', (cmd_name,))
        row = cur.fetchone()
        con.close()

        if row:
            name, phrase, user_ids = row
            mentions = [f'<@{uid}>' for uid in user_ids.split(',')]
            await ctx.send(f"{', '.join(mentions)}, {phrase}")
        else:
            await ctx.send(f"Command {cmd_name} not found.")

    @commands.command(name='commremove')
    async def commremove(self, ctx, cmd_name: str, *, user_names: str):
        user_names = [u.strip() for u in user_names.split(',')]
        user_ids = []
        for name in user_names:
            member = discord.utils.get(ctx.guild.members, nick=name) or discord.utils.get(ctx.guild.members, name=name)
            if member:
                user_ids.append(str(member.id))

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT * FROM commands WHERE name = ?', (cmd_name,))
        row = cur.fetchone()
        if row:
            _, phrase, ids_str = row
            updated_ids = [i for i in ids_str.split(',') if i not in user_ids]
            cur.execute('UPDATE commands SET user_ids = ? WHERE name = ?', (','.join(updated_ids), cmd_name))
            con.commit()
            await ctx.send(f'Removed users from {cmd_name}.')
        else:
            await ctx.send(f'Command {cmd_name} not found.')
        con.close()

    @commands.command(name='commadd')
    async def commadd(self, ctx, cmd_name: str, user_name: str):
        member = discord.utils.get(ctx.guild.members, nick=user_name) or discord.utils.get(ctx.guild.members, name=user_name)
        if not member:
            await ctx.send("User not found.")
            return

        uid = str(member.id)
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT * FROM commands WHERE name = ?', (cmd_name,))
        row = cur.fetchone()
        if row:
            name, phrase, ids_str = row
            ids = ids_str.split(',')
            if uid not in ids:
                ids.append(uid)
                cur.execute('UPDATE commands SET user_ids = ? WHERE name = ?', (','.join(ids), cmd_name))
                con.commit()
                await ctx.send(f'User added to command {cmd_name}.')
        else:
            await ctx.send(f'Command {cmd_name} not found.')
        con.close()

    @commands.command(name='commhelp')
    async def commhelp(self, ctx):
        await ctx.send("""```Command System Help:
!newcmd hello "Hello!" "Alice, Bob"
!commadd hello Charlie
!commcmd hello
!commremove hello Alice
```""")

async def setup(bot):
    await bot.add_cog(Admin(bot))
