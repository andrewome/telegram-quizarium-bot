import os
import logging
from quizarium.QuizariumGameInstance import QuizariumGameInstance
from store import Store
from dotenv import load_dotenv
from telethon import TelegramClient, sync, events
from telethon.tl.types import PeerUser, PeerChannel, PeerChat
from telethon.tl.custom import Message

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
store = Store("./store.json")
store.load()
quizariumInstances = {}

@client.on(events.NewMessage)
async def handler(event):
    global self_id, channels_to_respond, store
    messageObj = event.message

    # Get chat id
    peer = messageObj.to_id
    if isinstance(peer, PeerChannel):
        chat_id = peer.channel_id
    if isinstance(peer, PeerUser):
        chat_id = peer.user_id
    if isinstance(peer, PeerChat):
        chat_id = peer.chat_id

    # Respond to chat events
    msg = messageObj.message

    # Get self_id if does not exist
    if self_id == None:
        client = event.client
        user = await client.get_me()
        self_id = user.id
    
    # Handle command
    if msg == "+respondtochannel":
        if event.from_id == self_id:
            channels_to_respond.add(chat_id)
            await event.reply("Responding to this channel!")

    # If from quizarium and inside channels that are given green light to respond to.
    if event.from_id == QUIZARIUM_BOT_ID and chat_id in channels_to_respond:
        if chat_id not in quizariumInstances:
            quizariumInstances[chat_id] = QuizariumGameInstance()
        await quizariumInstances[chat_id].parse(msg, store, messageObj)
        await messageObj.reply("Hello quizarium bawt")
        
client.start()
print("Started!")
client.run_until_disconnected()
