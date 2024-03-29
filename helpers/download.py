#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import time
import json
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.progress import progress_func
from helpers.tools import execute, clean_up
from helpers.download_from_url import download_link

DATA = {}

async def download_file(client, message):
    media = message.reply_to_message
    if media.empty:
        await message.reply_text('Why did you delete that?? 😕', True)
        return

    filetype = media.document or media.video
    tt = "EmptyTITLEdetected"
    
    if media.caption:
        if len(media.caption) <= 32:
            tt = media.caption
    elif filetype.file_name :
        if '@madresehahlebait' in filetype.file_name :
            tt = "@madresehahlebait"
        
    msg = await client.send_message(
        chat_id=message.chat.id,
        text=f"**Downloading your file to server...**\n\n**Title:** `{tt}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Check Progress", callback_data="progress_msg")]
        ]),
        reply_to_message_id=media.id
    )
    
    c_time = time.time()
    download_location = await client.download_media(
        message=media,
        progress=progress_func,
        progress_args=(
            "**Downloading your file to server...**",
            msg,
            c_time
        )
    )

    await msg.edit_text("Processing your file....")

    output = await execute(f"ffprobe -hide_banner -show_streams -print_format json '{download_location}'")
    
    if not output:
        await clean_up(download_location)
        await msg.edit_text("Some Error Occured while Fetching Details...")
        return

    details = json.loads(output[0])
    buttons = []
    DATA[f"{message.chat.id}-{msg.id}"] = {}
    for stream in details["streams"]:
        mapping = stream["index"]
        stream_name = stream["codec_name"]
        stream_type = stream["codec_type"]
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try: 
            lang = stream["tags"]["language"]
        except:
            lang = mapping
        
        DATA[f"{message.chat.id}-{msg.id}"][int(mapping)] = {
            "map" : mapping,
            "name" : stream_name,
            "type" : stream_type,
            "lang" : lang,
            "location" : download_location,
            "title" : tt
        }
        buttons.append([
            InlineKeyboardButton(
                f"{stream_type.upper()} - {str(lang).upper()}", f"{stream_type}_{mapping}_{message.chat.id}-{msg.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("CANCEL",f"cancel_{mapping}_{message.chat.id}-{msg.id}")
    ])    

    await msg.edit_text(
        "**Select the Stream to be Extracted...**",
        reply_markup=InlineKeyboardMarkup(buttons)
        )

async def download_url_link(client, message):
    m = message.reply_to_message
    link = m.text
    
    if '|' in link:
        link, tt = link.split('|')
        link = link.strip()
        tt = tt.strip()
    else:
        link = link.strip()
        tt = None
    
    filename = os.path.basename(link)
    filename = filename.replace('%40','@')
    dl_path = os.path.join(f'./{filename}')
    
    msg = await client.send_message(
        chat_id=m.chat.id,
        text=f"**Downloading your file to server...**\n\n**Title:** `{tt}`",
        reply_to_message_id=m.id
    )
    
    start = time.time()
    try:
        download_location = await download_link(link, dl_path, msg, start, client)
    except Exception as e:
        print(e)
        await msg.edit(f"**Download Failed** :\n\n{e}")
        await clean_up(download_location)
        return
    
    output = await execute(f"ffprobe -hide_banner -show_streams -print_format json '{download_location}'")
    
    if not output:
        await clean_up(download_location)
        await msg.edit_text("Some Error Occured while Fetching Details...")
        return

    details = json.loads(output[0])
    buttons = []
    DATA[f"{m.chat.id}-{msg.id}"] = {}
    for stream in details["streams"]:
        mapping = stream["index"]
        stream_name = stream["codec_name"]
        stream_type = stream["codec_type"]
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try: 
            lang = stream["tags"]["language"]
        except:
            lang = mapping
        
        DATA[f"{m.chat.id}-{msg.id}"][int(mapping)] = {
            "map" : mapping,
            "name" : stream_name,
            "type" : stream_type,
            "lang" : lang,
            "location" : download_location,
            "title" : tt
        }
        buttons.append([
            InlineKeyboardButton(
                f"{stream_type.upper()} - {str(lang).upper()}", f"{stream_type}_{mapping}_{m.chat.id}-{msg.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("CANCEL",f"cancel_{mapping}_{m.chat.id}-{msg.id}")
    ])    

    await msg.edit_text(
        "**Select the Stream to be Extracted...**",
        reply_markup=InlineKeyboardMarkup(buttons)
        )
