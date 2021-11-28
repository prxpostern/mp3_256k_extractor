#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from helpers.tools import execute, clean_up
from helpers.upload import upload_audio, upload_subtitle

async def extract_audio(client, message, data):
    await message.edit_text("Extracting Stream from file...")

    dwld_loc = data['location']
    out_loc = data['location'] + ".mp3"

    out, err, rcode, pid = await execute(f"ffmpeg -i \"{dwld_loc}\" -map 0:{data['map']} -af \"pan=stereo|c0=c0|c1=c0\" -ar 48000 -ab 256k -f mp3 \"{out_loc}\" -y")
    if rcode != 0:
        await message.edit_text(f"**(mp3 256k) - Error Occured.\n\n{err}**")
        print(err)
        await clean_up(dwld_loc, out_loc)
        return
    

    await clean_up(dwld_loc)
    tt = data['title']
    status = await upload_audio(client, message, out_loc, tt)
    if status:
        time.sleep(3)
        await upload_audio(client, message, out_loc, tt)

async def extract_subtitle(client, message, data):
    await message.edit_text("Extracting Stream from file")

    dwld_loc = data['location']
    out_loc = data['location'] + ".srt"   

    out, err, rcode, pid = await execute(f"ffmpeg -i '{dwld_loc}' -map 0:{data['map']} '{out_loc}' -y")
    if rcode != 0:
        await message.edit_text(f"**Error Occured.\n\n{err}**")
        print(err)
        await clean_up(dwld_loc, out_loc)
        return

    await clean_up(dwld_loc)  
    await upload_subtitle(client, message, out_loc)
