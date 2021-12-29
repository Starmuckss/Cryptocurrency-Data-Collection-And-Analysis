# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 08:48:21 2021

@author: HP
"""

import pandas as pd
import configparser
import json
import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetFullChannelRequest



api_id = 6303180
api_hash = '92eea81aec875d961c115365ed89df99'
phone = "+905079158056"
username = "Sefa Yapıcı"
group_username = "c0ban_global" # Group name can be found in group link (Example group link : https://t.me/c0ban_global, group name = 'c0ban_global')

#Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
#api_id = config['Telegram']['api_id']
#api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

#phone = config['Telegram']['phone']
#username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))
        

from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)
user_input_channel = group_username #input("enter entity(telegram URL or entity id):")

if user_input_channel.isdigit():
    entity = PeerChannel(int(user_input_channel))
else:
    entity = user_input_channel

my_channel = client.get_entity(entity)        
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)
offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0


async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = "c0ban_global"#input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    channel_connect = await client.get_entity(entity)
    channel_full_info = client(GetFullChannelRequest(channel=channel_connect))
    print(channel_full_info.full_chat.participants_count)
    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    # with open('channel_messages.json', 'w') as outfile:
    #     json.dump(all_messages, outfile, cls=DateTimeEncoder)

with client:
    client.loop.run_until_complete(main(phone))



