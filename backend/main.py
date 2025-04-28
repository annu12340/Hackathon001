import asyncio
import logging
from app.bot import SlackBot

logging.basicConfig(level=logging.INFO)

async def main():
    bot = SlackBot()
    print("botbotbot",bot)
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main()) 