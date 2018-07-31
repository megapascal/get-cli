from telethon import TelegramClient
import time
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon import errors
from colorama import Fore


class Configurations:
    def __init__(self, api_id: int(), api_hash: str(), session: str()):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session = session


# fill in api credentials that you can get from https://my.telegram.core
conf = Configurations(api_id="API_ID", api_hash='API_HASH', session='your_session')
# enter your session name don't edit it too much! one session per one account

client = TelegramClient(session=conf.session, api_id=conf.api_id, api_hash=conf.api_hash, app_version='0.0.1')
client.start()


# chat_id can be username/invite link
async def get_all_members(chat_id):
    title = await client.get_entity(chat_id)
    print(Fore.CYAN + "Parsing", Fore.MAGENTA + str(title.title), Fore.BLUE + str(title.id), sep=(Fore.BLACK+'|'))
    try:
        members_array = await client.get_participants(chat_id, aggressive=True)
        bomj_increment, ids_increment, usernames_increment = int(), int(), int()
        all_members_count = await client.get_participants(chat_id, limit=0)
        with open(f'{title.id}_{time.time()}.txt', 'w') as file:
            stats = f'(GET: {len(members_array)}/FROM: {all_members_count.total})'
            file.write('Alive users ids readable array:\n[\n')
            for self in members_array:
                if not self.bot:
                    if not self.deleted:
                        file.write(f"{self.id}, ")
                        ids_increment += 1
                    else:
                        bomj_increment += 1
                elif self.bot:
                    bomj_increment += 1
            file.write('\n]\nUsernames array: [\n')
            for self in members_array:
                if not self.bot:
                    if self.username:
                        file.write(f'\"@{self.username}\", ')
                        usernames_increment += 1

            file.write(f"\n]\n\nTrash(bots/deleted_accounts): {bomj_increment}\n"
                       f"IDs: {ids_increment}\nUsernames: {usernames_increment}\nStats: {stats}\n"
                       f"by </MPA\>")
            file.close()
        return stats + '\nFile successfully saved!'
    except Exception as out_error:
        return str(out_error)


async def join_channel(in_hash):
    try:
        await client(ImportChatInviteRequest(in_hash))
        return 't'
    except errors.InviteHashInvalidError as out_error:
        print(Fore.RED + str(out_error), Fore.GREEN + 'Clue: use valid links type id/Status: *\STOPPED\*', sep='->')
        return 'end'
    except errors.UserAlreadyParticipantError as out_error:
        print(Fore.RED + str(out_error), Fore.GREEN + 'Clue: just type channel id or private link\'s hash/'
                                                      'Status: *\CONTINUING\*', sep='->')
        return 'cont'


async def credit():
    credit_text = f"""\nCreator: Martin_Winks(t.me/martin_winks)\nLicensed under MIT licence\n"""
    print(Fore.LIGHTBLUE_EX + credit_text)
