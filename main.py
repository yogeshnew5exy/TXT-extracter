import asyncio
import json
import logging
import os
import re
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler
from subprocess import getstatusoutput

import requests
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyromod import listen

import online.helpers.vid as helper
from online.Config import *
from online.helpers.button import keyboard
from online.helpers.sudoers import *
from online.helpers.text import *

# ==========Logging==========#
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging = logging.getLogger()

# =========== Client ===========#
bot = Client(
    "bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
)

print(listen.__file__)


# ========== Converter =============#
@bot.on_message(filters.command(["taiyaric"]))
async def gaiyrab(bot: Client, message: Message):
    message.from_user.id if message.from_user is not None else None
    if not one(message.from_user.id):
        return await message.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await message.reply_text(
            "This is help to convert json file to text of taiyari karlo app ",
            disable_web_page_preview=True,
        )
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    to_write = ""
    try:
        with open(x, "r") as file:
            data = json.load(file)
            for entry in data:
                target_change = entry[1][0].get("targetChange")
                if target_change and target_change.get("targetChangeType") == "ADD":
                    continue
                document_change = (
                    entry[1][0]
                    .get("documentChange", {})
                    .get("document", {})
                    .get("fields", {})
                )
                quality = None
                recordings = (
                    document_change.get("recordings", {})
                    .get("arrayValue", {})
                    .get("values", [])
                )
                for recording in recordings:
                    recording_fields = recording.get("mapValue", {}).get("fields", {})
                    quality = recording_fields.get("quality", {}).get("stringValue")
                    if quality == "480p":
                        path = recording_fields.get("path", {}).get("stringValue")
                        title = document_change.get("title", {}).get("stringValue")
                        to_write += f"{title}:{path}\n"
                if document_change.get("type", {}).get("stringValue") == "pdf":
                    title_pdf = document_change.get("title", {}).get("stringValue")
                    ref_pdf = document_change.get("ref", {}).get("stringValue")
                    to_write += f"{title_pdf}:{ref_pdf}\n"
    except Exception as e:
        os.remove(x)
        return await message.reply_text(f"**Error** : {e}")
    with open(f"new.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"new.txt", "rb") as f:
        await asyncio.sleep(5)
        doc = await message.reply_document(document=f, caption="Here is your txt file.")


# =========== Core Commands ======#

shell_usage = f"**USAGE:** Executes terminal commands directly via bot.\n\n<pre>/shell pip install requests</pre>"


@bot.on_message(filters.command(["shell"]))
async def shell(client, message: Message):
    """
    Executes terminal commands via bot.
    """
    if not two(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(shell_usage, quote=True)

    user_input = message.text.split(None, 1)[1].split(" ")

    try:
        shell = subprocess.Popen(
            user_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = shell.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    except Exception as error:
        logging.info(f"{error}")
        return await message.reply_text(f"**Error**:\n\n{error}", quote=True)

    if len(result) > 2000:
        file = BytesIO(result.encode())
        file.name = "output.txt"
        await message.reply_text("Output is too large (Sending it as File)", quote=True)
        await client.send_document(message.chat.id, file, caption=file.name)
    else:
        await message.reply_text(f"**Output:**:\n\n{result}", quote=True)


paid_text = """
» Hello i am online class bot which help you to **Extract** and **Download** video of Physics Wallah / Apni Kaksha / Khan Gs ..... Any Type of Online Class Which You Want.
• **How to Access this bot**

Step 1: Click Below on Developer.
Step 2: Go to Telegram Username
Step 3: Send your Telegram ID From @missrose_bot
"""


# ============== Start Commands ==========#
@bot.on_message(filters.command(["start"]))
async def account_lstarn(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_photo(
            photo="https://telegra.ph/file/e6d2807b0d3074742fe41.jpg",
            caption=paid_text,
            reply_markup=keyboard,
        )
    await m.reply_text(start_text)


# ========== Global Concel Command ============
cancel = False


@bot.on_message(filters.command(["cancel"]))
async def cancel(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nThis Command is only For Owner",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "Canceling All process Plz wait\n🚦🚦 Last Process Stopped 🚦🚦"
    )
    global cancel
    cancel = False
    await editable.edit("cancelled all")
    return


# ============== Power Commands =================
@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nYou Don't Have Right To Access This Contact Owner",
        )
    await m.reply_text("➭ 𝗕𝗼𝘁 𝗜𝘀 𝗕𝗲𝗶𝗻𝗴 𝗥𝗲𝘀𝘁𝗮𝗿𝘁𝗶𝗻𝗴. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗞𝗲𝗲𝗽 𝗣𝗮𝘁𝗶𝗲𝗻𝗰𝗲", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


# ============ Download Commands ==============#
@bot.on_message(filters.command(["pyro"]))
async def download_pw(bot: Client, m: Message):
    global cancel
    m.from_user.id if m.from_user is not None else None
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await m.reply_text(pyro_text, disable_web_page_preview=True)
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    links = []
    try:
        with open(x, "r") as f:
            content = f.read()
            new_content = content.split("\n")
            for i in new_content:
                links.append(re.split(":(?=http)", i))
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"**Error** : {e}")
        os.remove(x)
        return
    await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    initial_number = await bot.listen(editable.chat.id)

    try:
        arg = int(initial_number.text)
    except:
        arg = 0

    await m.reply_text(
        f"Total links: **{len(links)}**\n\nSend Me Final Number\n\nBy Default Final is {len(links)}"
    )
    final_number = await bot.listen(editable.chat.id)

    try:
        arg1 = int(final_number.text)
    except:
        arg1 = len(links)
    await m.reply_text("**Enter batch name**")
    input0 = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text(
        "**For Thumb Url**\n\n• Custom url : Use @vtelegraphbot and send me links\n• If Your file Contain Url : `yes`\n• Send no if you don't want : `no`"
    )
    input6 = await bot.listen(editable.chat.id)
    lol_thumb = input6.text

    if arg == "0":
        count = 1
    else:
        count = int(arg)
    cancel = True
    for i in range(arg, arg1):
        try:
            while cancel == False:
                return await m.reply_text("Cancelled Process")
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )
            try:
                if lol_thumb == "yes":
                    old_thumb = links[i][2]
                    getstatusoutput(f"wget '{old_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                elif lol_thumb.startswith("http://") or lol_thumb.startswith(
                    "https://"
                ):
                    old_thumb = lol_thumb
                    getstatusoutput(f"wget '{lol_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                else:
                    thumb = "no"
                    old_thumb = "No Thumbnail"
            except Exception as e:
                return await m.reply_text(e)
            Total_Links = arg1 - int(arg)
            Show_old = f"**Total Links** : {Total_Links}\n\n**Name :-** `{name1}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
            prog_old = await m.reply_text(Show_old)
            if raw_text2 == "144":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "256x144" in out:
                    ytf = f"{out['256x144']}"
                elif "320x180" in out:
                    ytf = out["320x180"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "320x180" in out:
                    ytf = out["320x180"]
                elif "426x240" in out:
                    ytf = out["426x240"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "426x240" in out:
                    ytf = out["426x240"]
                elif "426x234" in out:
                    ytf = out["426x234"]
                elif "480x270" in out:
                    ytf = out["480x270"]
                elif "480x272" in out:
                    ytf = out["480x272"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "640x360" in out:
                    ytf = out["640x360"]
                elif "638x360" in out:
                    ytf = out["638x360"]
                elif "636x360" in out:
                    ytf = out["636x360"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "638x358" in out:
                    ytf = out["638x358"]
                elif "852x316" in out:
                    ytf = out["852x316"]
                elif "850x480" in out:
                    ytf = out["850x480"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["852x470"]
                elif "1280x720" in out:
                    ytf = out["1280x720"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["854x470"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "850x480" in out:
                    ytf = ["850x480"]
                elif "960x540" in out:
                    ytf = out["960x540"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]
            elif raw_text2 == "720":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "1280x720" in out:
                    ytf = out["1280x720"]
                elif "1280x704" in out:
                    ytf = out["1280x704"]
                elif "1280x474" in out:
                    ytf = out["1280x474"]
                elif "1920x712" in out:
                    ytf = out["1920x712"]
                elif "1920x1056" in out:
                    ytf = out["1920x1056"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == "144":
                    ytf = "http-240p"
                elif raw_text2 == "240":
                    ytf = "http-240p"
                elif raw_text2 == "360":
                    ytf = "http-360p"
                elif raw_text2 == "480":
                    ytf = "http-540p"
                elif raw_text2 == "720":
                    ytf = "http-720p"
                else:
                    ytf = "http-360p"
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]

            try:
                if "unknown" in out:
                    pass
                else:
                    list(out.keys())[list(out.values()).index(ytf)]

                name = f"{name1}"
            except Exception as e:
                return await m.reply(f"Error in ytf : {e}")
            await prog_old.delete(True)
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "youtu" in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif url.startswith("https://apni-kaksha.vercel.app"):
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == "0" or "unknown" in out:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ".pdf" or "download" in str(url):
                cmd = "pdf"
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'

            try:
                Show = f"**Downloading:-**\n\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
                prog = await m.reply_text(Show)
                cc = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                cc1 = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                if cmd == "pdf" or ".pdf" in str(url) or ".pdf" in name:
                    print("PDF")
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        await m.reply_document(
                            ka,
                            caption=f"{cc1}",
                        )
                        count += 1
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    filename = await helper.download_video(url, cmd, name)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`"
                )
                continue
        except Exception as e:
            return await m.reply_text(f"Overall Error : {e}")
    await m.reply_text("Done")


@bot.on_message(filters.command(["patna"]))
async def khan_dowbol(bot: Client, m: Message):
    global cancel
    m.from_user.id if m.from_user is not None else None
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await m.reply_text(pyro_text, disable_web_page_preview=True)
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    links = []
    try:
 
