import asyncio

from pyrogram import Client, filters  # class pyrogram
from pyrogram.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery  # class pyrogram
from pyrogram.errors.exceptions.bad_request_400 import UserIdInvalid  # telegram error

from Group_Cleaner.helper import json_load, json_dump

admin_check = lambda _, c, m: True if m.chat.get_member(m.from_user.id).status \
                                      in ["creator", "administrator"] else False  # func for check if user is admin

groups_list = 'Group_Cleaner/groups.json'


@Client.on_message(filters.group & filters.create(admin_check) &
                   filters.command(["clean", 'clean@GroupCleanerHebBot']))
# func for kick existing members
# using with telegram-commands: "/clean"
async def clean_group(_, message: Message, name=None):
    # check if bot is admin
    get_me = await message.chat.get_member("me")
    if get_me.status != "administrator":
        await message.reply("הרובוט דורש ניהול!\nThe robot requires management!")
        return

    count = 0  # Counted kickers
    async for member in message.chat.iter_members():
        id_member = member.user.id
        get_member = await message.chat.get_member(id_member)

        if get_member.status not in ["creator", "administrator"]:
            await message.chat.kick_member(id_member)  # kick member
            await message.chat.unban_member(id_member)  # remove member from black_list
            count += 1

    if count > 0:
        await message.reply(f'''מספר משתמשים שהוסרו:\nNumber of users removed:\n`{count}`''',
                            reply_markup=InlineKeyboardMarkup([[
                                InlineKeyboardButton("Delete / מחק", callback_data="delete")]]))

    else:
        await message.reply("לא נמצאו משתמשים להסרה!\nNo removable users found")


@Client.on_callback_query(filters.regex("delete"))
# func for delete msg with Click on button
def delete_msg_count(_: Client, call: CallbackQuery):
    call.message.delete()


@Client.on_message(filters.group & filters.new_chat_members)
# func for remove new_members
async def group(client: Client, message: Message):
    me = await client.get_me()

    for new_member in message.new_chat_members:
        if me.id == new_member.id:
            continue

        try:
            id_member = new_member.id
            kick = await message.chat.kick_member(id_member)  # kick member

            await asyncio.sleep(30)

            await message.chat.unban_member(id_member)  # remove member from black_list

            if type(kick) != bool:
                await kick.delete()  # delete the message "<bot> removed <user>"
        except UserIdInvalid:
            pass

    await message.delete()  # delete the message "<user> joined the group"

    # saved group to DB
    all_groups: list = json_load(groups_list)
    if message.chat.id not in all_groups:
        all_groups.append(message.chat.id)
        json_dump(all_groups, groups_list)


@Client.on_message(filters.group & filters.service, group=1)
# func for delete other service message
async def service_messages(_: Client, message: Message):
    await message.delete()
