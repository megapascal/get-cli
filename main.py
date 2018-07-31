import asyncio
from colorama import Fore
from config import get_all_members
from config import client
from config import join_channel
import config


async def cleaner():
    await config.credit()
    text_cleaner = input(Fore.RESET+'Enter channel id/username/join_link: ').replace(' ', '')
    if text_cleaner.startswith('https://') or text_cleaner.startswith('t.me'):
        join_hash = text_cleaner.split('/')[-1]
        print(Fore.LIGHTMAGENTA_EX + join_hash, Fore.RESET + '- your invite link hash')
        succ = await join_channel(join_hash)
        if succ == 't':
            channel = await client.get_entity(text_cleaner)
            print(Fore.RESET+"Detected private channel/joined")
            return channel
        elif succ == 'end':
            asyncio.get_event_loop().close()
        elif succ == 'cont':
            channel = await client.get_entity(text_cleaner)
            print(Fore.RESET + "Detected private channel/joined")
            return channel
    else:
        join_hash = text_cleaner
        return join_hash


async def main_func():
    if client:
        try:
            answer = await get_all_members(await cleaner())
            print(Fore.LIGHTGREEN_EX+'fetching(please wait...)')
            if answer:
                print(Fore.GREEN + answer)
            elif not answer:
                print(Fore.RED + 'Error occurred!')
        except Exception as out_error:
            print(Fore.RED + str(out_error))
    elif not client:
        print('Error occurred! Please be sure you have session file/api credentials filled')
asyncio.get_event_loop().run_until_complete(main_func())