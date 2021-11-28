#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script


@trojanz.on_message(filters.private & (filters.document | filters.video))
async def confirm_dwnld(client, message):

    if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text(text=f"sorry ! this is a bot for private use.", quote=True)
        return

    media = message
    filetype = media.document or media.video

    if filetype.mime_type.startswith("video/"):
        await message.reply_text(
            "**What you want me to do??**",
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="DOWNLOAD and PROCESS", callback_data="download_file")],
                [InlineKeyboardButton(text="CANCEL", callback_data="close")]
            ])
        )
    else:
        await message.reply_text(
            "Invalid Media",
            quote=True
        )
@trojanz.on_message(filters.private & filters.incoming & filters.text & (filters.regex('^(ht|f)tp*')))
async def link_dwnld(client, message):

    if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text(text=f"sorry ! this is a bot for private use.", quote=True)
        return
    if not message.media:
        #link = message.text
        await message.reply_text(
            "**What you want me to do??**",
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="DOWNLOAD From Link", callback_data="download_url")],
                [InlineKeyboardButton(text="CANCEL", callback_data="close")]
            ])
        )
