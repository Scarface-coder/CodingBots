from pyrogram import filters
from pyrogram.types import Message

from CodingBots import app
from CodingBots.misc import SUDOERS
from CodingBots.utils.database import add_sudo, remove_sudo
from CodingBots.utils.decorators.language import language
from CodingBots.utils.extraction import extract_user
from CodingBots.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID


@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    text = _["sudo_5"]
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    text += f"1➤ {user}\n"
    count = 0
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user}\n"
            except:
                continue
    if not text:
        await message.reply_text(_["sudo_7"])
    else:
        await message.reply_text(text, reply_markup=close_markup(_))


@app.on_message(filters.command("clearsudo") & filters.user(OWNER_ID))
@language
async def clear_sudo_except_owner(client, message: Message, _):
    if not SUDOERS:
        return await message.reply_text("❌ Koi bhi sudo user nahi hai.")

    remaining = []
    failed = 0
    for user_id in list(SUDOERS):
        if user_id == OWNER_ID:
            remaining.append(user_id)
            continue
        removed = await remove_sudo(user_id)
        if removed:
            SUDOERS.remove(user_id)
        else:
            failed += 1

    await message.reply_text(
        f"✅ Sirf OWNER sudo me rakha gaya.\n"
        f"🗑️ Baaki sab remove kar diye gaye.\n"
        f"❌ Remove fail hue: {failed}" if failed else "✅ Cleaned successfully."
                    )
