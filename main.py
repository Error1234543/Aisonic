import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# 🔑 Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))

# 🤖 Initialize bot & Gemini
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# 🌐 Flask app
app = Flask(__name__)

@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "👋 Gemini AI Doubt Solver Active! Send your NEET/JEE question in Gujarati or English.")
    else:
        bot.reply_to(message, "⚠️ Access Denied! Only the owner or group can use this bot.")

@bot.message_handler(content_types=["text", "photo"])
def handle_message(message):
    # Access control
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    # Handle photo (future update)
    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon...)")
        return

    try:
        question = message.text
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(question)
        bot.reply_to(message, f"🧠 જવાબ:\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)