import os
import telebot
import threading
import time
from flask import Flask
import openai

# === Environment Variables ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Owner & Access Control ===
OWNER_ID = 8226637107          # 👈 Replace with your Telegram ID
ALLOWED_GROUP_ID = -1003126293720 # 👈 Replace with your group ID
AUTHORIZED_USERS = set([8226637107])  # Initially only owner allowed

# === Flask app for Koyeb health check ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ NEET/JEE Gujarati AI Bot Running Securely!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# === Telegram Bot ===
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY


# =================== ACCESS SYSTEM ===================
@bot.message_handler(commands=['auth'])
def auth_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Only owner can authorize users.")
        return

    try:
        parts = message.text.split()
        if len(parts) == 2:
            new_user_id = int(parts[1])
            AUTHORIZED_USERS.add(new_user_id)
            bot.reply_to(message, f"✅ Authorized user: {new_user_id}")
        else:
            bot.reply_to(message, "Usage: /auth <user_id>")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Group check
    if chat_id != ALLOWED_GROUP_ID and user_id != OWNER_ID:
        bot.reply_to(message, "❌ This bot only works in the official NEET/JEE group.")
        return

    # Auth check
    if user_id not in AUTHORIZED_USERS and user_id != OWNER_ID:
        bot.reply_to(message, "🔒 You are not authorized to use this bot.")
        return

    bot.reply_to(
        message,
        "👋 Namaste! હું NEET/JEE માટે તમારો AI Doubt Solver છું.\n"
        "તમારો કોઈપણ પ્રશ્ન મોકલો (Gujarati અથવા English માં) અને હું સમજાવીશ. 📚"
    )


@bot.message_handler(func=lambda msg: True)
def solve_doubt(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Group & Auth checks
    if chat_id != ALLOWED_GROUP_ID and user_id != OWNER_ID:
        return
    if user_id not in AUTHORIZED_USERS and user_id != OWNER_ID:
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a NEET/JEE Gujarati tutor who explains science topics simply and clearly."
                },
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message["content"]
        bot.reply_to(message, f"🧠 {answer}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")


# =================== THREADS ===================
def run_telebot():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Bot crashed: {e}")
            time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telebot()
