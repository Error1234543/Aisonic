import os
import telebot
from openai import OpenAI
from flask import Flask, request

# 🔐 Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))

# 🧠 Setup
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# 🌐 Webhook route
@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# 🚀 Start command
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == OWNER_ID:
        bot.reply_to(message, "👋 AI Doubt Solver Bot Active!")
    else:
        bot.reply_to(message, "⚠️ Access Denied!")


# 📘 Handle messages
@bot.message_handler(content_types=["text", "photo"])
def handle_doubt(message):
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon...)")
        return

    question = message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Gujarati NEET/JEE tutor who explains clearly in Gujarati."},
                {"role": "user", "content": question},
            ],
        )

        answer = response.choices[0].message.content
        bot.reply_to(message, f"🧠 જવાબ:\n{answer}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")


# ✅ Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)