import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, sync, events
from telethon.tl.types import PeerUser, PeerChannel, PeerChat

# Get constants
load_dotenv()
API = os.getenv("API")
APIHASH = os.getenv("APIHASH")
QUIZARIUM_BOT_ID = 155670507
SESSION_NAME = "bot_session"

# Logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Log in
client = TelegramClient(SESSION_NAME, API, APIHASH)

# Local storage
channels_to_respond = set()
self_id = None

@client.on(events.NewMessage)
async def handler(event):
    # Get chat id
    peer = event.message.to_id
    if isinstance(peer, PeerChannel):
        chat_id = peer.channel_id
    if isinstance(peer, PeerUser):
        chat_id = peer.user_id
    if isinstance(peer, PeerChat):
        chat_id = peer.chat_id

    # Respond to chat events
    msg = event.message.message
    client = event.client
    if msg == "+respondtochannel":
        user = await client.get_me()
        self_id = user.id
        if event.from_id == self_id:
            channels_to_respond.add(chat_id)
            print(channels_to_respond)
            await event.reply("Responding to this channel!")
                
    if event.from_id == QUIZARIUM_BOT_ID and chat_id in channels_to_respond:
        messageObj = event.message
        msg = messageObj.message
        await messageObj.reply("Hello quizarium bawt")
        print(msg)

client.start()
print("Started!")
client.run_until_disconnected()
