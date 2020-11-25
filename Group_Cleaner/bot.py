from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from Group_Cleaner.group import group, clean_group, service_messages
from Group_Cleaner.private import private, clean_private, help

app = Client("clean")


app.add_handler(MessageHandler(
    group, filters.group & filters.new_chat_members
))

app.add_handler(MessageHandler(
    private, filters.private & filters.command("start")
))

app.add_handler(MessageHandler(
   service_messages, filters.group & filters.left_chat_member
))

app.add_handler(MessageHandler(
   clean_group, filters.group & filters.command("clean")
))

app.add_handler(MessageHandler(
    help, filters.private & filters.command("help")
))

app.add_handler(MessageHandler(
    clean_private, filters.private & filters.command("clean")
))
