import os
import telebot
import openai
from flask import Flask, request

# 🔐 Environment variables (add these in Koyeb dashboard)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))  # your Telegram ID
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))  # your group ID

# Initialize
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# ---------------------------
# Flask Webhook Endpoint
# ---------------------------
@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# ---------------------------
# Start Command
# ---------------------------
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == OWNER_ID:
        bot.reply_to(message, "👋 AI Doubt Solver Active! Send a NEET/JEE question in Gujarati or English.")
    else:
        bot.reply_to(message, "⚠️ Access Denied! This bot is private.")


# ---------------------------
# Doubt Solver
# ---------------------------
@bot.message_handler(content_types=["text", "photo"])
def handle_doubt(message):
    # Only allow Owner or Group messages
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon — image doubt solving)")
        return

    question = message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Gujarati NEET/JEE tutor. Answer conceptually and clearly."},
                {"role": "user", "content": question},
            ],
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, f"🧠 જવાબ:\n{answer}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")


# ---------------------------
# Run Flask App
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)