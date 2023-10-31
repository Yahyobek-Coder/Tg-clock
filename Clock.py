import asyncio
import datetime
import subprocess
import sys
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

# Print a fancy banner
print("""\033[31m
▄▄▄█████▓  ▄████     ▄████▄   ██▓     ▒█████   ▄████▄   ██ ▄█▀
▓  ██▒ ▓▒ ██▒ ▀█▒   ▒██▀ ▀█  ▓██▒    ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ 
▒ ▓██░ ▒░▒██░▄▄▄░   ▒▓█    ▄ ▒██░    ▒██░  ██▒▒▓█    ▄ ▓███▄░ 
░ ▓██▓ ░ ░▓█  ██▓   ▒▓▓▄ ▄██▒▒██░    ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ 
  ▒██▒ ░ ░▒▓███▀▒   ▒ ▓███▀ ░░██████▒░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄
  ▒ ░░    ░▒   ▒    ░ ░▒ ▒  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒
    ░      ░   ░      ░  ▒   ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░
  ░      ░ ░   ░    ░          ░ ░   ░ ░ ░ ▒  ░        ░ ░░ ░ 
               ░    ░ ░          ░  ░    ░ ░  ░ ░      ░  ░   
                    ░                         ░                 
\033[32mDeveloper: @Dasturchi1111\n\n""")

# API credentials
api_id = 770157316
api_hash = "1e6ca420184a701db1f8a1301df99288"

# Input for the phone number or bot token
phone_number = input("Please enter your phone number (or bot token): ")

# Create a TelegramClient instance
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter code: '))
        except SessionPasswordNeededError:
            password = input('Enter password: ')
            await client.sign_in(password=password)

    # Input for setting a custom nickname
    nick = input("\033[32mNickname: \033[32m")

    while True:
        current_time = datetime.datetime.today().strftime(nick + " | %H:%M |")
        await client(UpdateProfileRequest(first_name=current_time))
        await asyncio.sleep(60)  # Update every minute

# Run the event loop with the main function
with client:
    try:
        import aiocron
    except ImportError:
        print("aiocron module not found. Installing aiocron...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiocron"])
        print("aiocron installation complete.")
    client.loop.run_until_complete(main())
