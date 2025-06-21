import asyncio
from bot.bot_client import RiffRaffBot
from config.config import Config


async def main():
    bot = RiffRaffBot()
    await bot.start(Config.TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot manually stopped.")
