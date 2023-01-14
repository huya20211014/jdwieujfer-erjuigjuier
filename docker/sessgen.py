from telethon import TelegramClient
import os
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo
# import getpass
from telethon.errors import SessionPasswordNeededError

api_id = 3955576
api_hash = '16fa452f9283489c4a1045bb2b4eb4a8'

# api_id = 10421053
# api_hash = 'b9f0634e4811bf6b55366d2816947a24'

# # 15523530810
# api_id = 11577932
# api_hash = '7bce17be5b3cdd20eebb375964900b19'

config_path = 'app.exe'
import shutil
import time
import asyncio


def sleep_dis(sleep_time):
    for i in range(sleep_time, -1, -1):
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)

# async def gensess():
async def test():
    for i in range(69):
        print('whynotlovexxxxxx{}.session'.format(i))
        client = TelegramClient('whynotlovexxxxxx{}.session'.format(i), api_id, api_hash, proxy=proxy_)
        async with client:
            pass


#     telegram_channel = await authclient.get_entity("Telegram")

async def main():
    for i in range(2):
        print('whynotlovexxxxxx{}.session'.format(i))
        client = TelegramClient('whynotlovexxxxxx{}.session'.format(i), api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)

            me = await client.sign_in(phone_number, input('Enter code: '))
        else:
            print('whynotlovexxxxxx{}.session 已经登录'.format(i))



if __name__ == '__main__':
    phone_number = '+8613088719278'
    # phone_number = '+8613065531681'
    # phone_number = '+8615523530810'
    
    loop = asyncio.get_event_loop()
    tasks = [main()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

