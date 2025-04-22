import asyncio
import logging
from app.slack_bot import SlackBot


logging.basicConfig(level=logging.INFO)

async def main():
    bot = SlackBot()
    await bot.start()

if __name__ == "__main__":
    # Run the async main function using asyncio.run()
    asyncio.run(main()) 