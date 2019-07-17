import os
from dotenv import load_dotenv
from telethon import TelegramClient, sync

# Get constants
load_dotenv()
API = os.getenv("API")
APIHASH = os.getenv("APIHASH")
SESSION_NAME = "bot_session"

client = TelegramClient(SESSION_NAME, API, APIHASH)

try:
    client.start()
    print(client.get_me())
finally:
    client.disconnect()
