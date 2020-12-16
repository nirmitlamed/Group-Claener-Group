from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from Group_Cleaner.helper import keyboards as kyb, json_load, json_dump

msg_file = 'Group_Cleaner/msg.json'  # path of text-file for msg's
users_list = 'Group_Cleaner/users.json'  # path for file for users DB

# lambda func for get lang of user
get_lang = lambda client, message: client.get_users([message.from_user.id])[0].language_code \
    if client.get_users([message.from_user.id])[0].language_code in ['he', 'en'] else 'en'

# lambda func for mention user
formating = lambda message: f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})'


@Client.on_message(filters.private & filters.command(["start", "help"]))
# the Answer bot for commands '/start' or '/help'
def start_msg(client: Client, message: Message):
    lang = get_lang(client, message)
    message.reply(json_load(msg_file)[message.command[0]][lang].format(formating(message)),
                  disable_web_page_preview=True, reply_markup=kyb[message.command[0] + "_" + lang])

    # save user to list users DB
    all_users: list = json_load(users_list)
    if message.from_user.id not in all_users:
        all_users.append(message.from_user.id)
        json_dump(all_users, users_list)


@Client.on_callback_query()
# the Answer bot for callback quary's - change lang
async def edit_lang(_: Client, call: CallbackQuery):
    await call.message.edit_text(
        json_load(msg_file)[call.data[:-3]][call.data[-2:]].format(formating(call)),
        disable_web_page_preview=True,
        reply_markup=kyb[call.data])


@Client.on_message(filters.private & filters.command('clean'))
# the Answer bot for '/clean' command, on private
async def clean_private(_, message: Message):
    await message.reply(
        "שלחו פקודה זו בקבוצתכם כדי לנקות אותה ממגיבים.\nSend this command to your group to clear it of responders.")
