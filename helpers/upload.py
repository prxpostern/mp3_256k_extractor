#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import time
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helpers.download_from_url import get_size
from helpers.tools import clean_up
from helpers.progress import progress_func
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def upload_audio(client, message, file_loc, tt):

    msg = await message.edit_text(
        text="**Uploading extracted stream...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    if tt == "EmptyTITLEdetected":
        title = None
    else:
        title = tt
    
    artist = None
    duration = 0

    metadata = extractMetadata(createParser(file_loc))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    
    fn = os.path.basename(file_loc)
    fn = os.path.splitext(fn)[0]
    fn = os.path.splitext(fn)[0]
    fn = fn + ".mp3"
    
    if '@madresehahlebait' in fn :
        artist = "استاد حسن اللهیاری"

    size = os.path.getsize(file_loc)
    size = get_size(size)
    
    c_time = time.time()    
    try:
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_loc,
            file_name=str(fn),
            caption=f"**Filename:** `{fn}`\n**Title:** `{title}`\n**Artist(s):** `{artist}`\n**Size:** {size}",
            title=title,
            performer=artist,
            duration=duration,
            progress=progress_func,
            progress_args=(
                "**Uploading extracted stream...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text(f"**Some Error Occurred.\nTrying again in 3 seconds...**\n\n{e}**")   
        return True

    await msg.delete()
    await clean_up(file_loc)    
    return False

async def upload_subtitle(client, message, file_loc):

    msg = await message.edit_text(
        text="**Uploading extracted subtitle...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    c_time = time.time() 

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_loc,
            caption="**@posternaudext001bot**",
            progress=progress_func,
            progress_args=(
                "**Uploading extracted subtitle...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text("**Some Error Occurred. See Logs for More Info.**")   
        return

    await msg.delete()
    await clean_up(file_loc)
