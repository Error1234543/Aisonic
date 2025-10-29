import os
import telebot
import google.generativeai as genai
from flask import Flask, request

# 🔐 Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))

# 🔧 Setup
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 🔑 Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "🤖 Gemini AI NEET/JEE Doubt Solver Ready! Send your question in Gujarati or English.")
    else:
        bot.reply_to(message, "⚠️ Access Denied! Only authorized users or group can use this bot.")

@bot.message_handler(content_types=["text", "photo"])
def handle_message(message):
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon with OCR feature)")
        return

    try:
        question = message.text
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"You are a Gujarati NEET/JEE tutor. Answer this clearly and accurately:\n\n{question}"
        )
        answer = response.text
        bot.reply_to(message, f"🧠 જવાબ:\n{answer}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)