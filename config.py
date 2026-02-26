import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Exchange rate API key
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')