import os
import telebot
from flask import Flask, request
import openai

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "8226637107"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1003126293720"))

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Gujarati NEET/JEE tutor."},
                {"role": "user", "content": question},
            ]
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, f"🧠 જવાબ:\n{answer}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)