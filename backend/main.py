import asyncio
import logging
from app.bot import SlackBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        bot = SlackBot()
        logger.info("Starting Slack bot...")
        await bot.start()
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 