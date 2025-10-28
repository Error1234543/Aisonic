import os
import telebot
from flask import Flask
from threading import Thread
from openai import OpenAI

# --- Load Environment Variables ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))

# --- Initialize Bot & OpenAI ---
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Flask app for Koyeb health check ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ AI Doubt Solver Bot is running!"

# --- Telegram Bot Handlers ---
@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "👋 AI Doubt Solver Active! Send your NEET/JEE question in Gujarati or English.")
    else:
        bot.reply_to(message, "⚠️ Access Denied! Only the owner or group can use this bot.")

@bot.message_handler(content_types=["text", "photo"])
def handle_message(message):
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon)")
        return

    try:
        question = message.text
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Gujarati NEET/JEE tutor."},
                {"role": "user", "content": question},
            ]
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, f"🧠 જવાબ:\n{answer}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

# --- Run Flask + Telegram Polling Together ---
def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()