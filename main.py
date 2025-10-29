import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# 🔐 Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "7447651332"))
GROUP_ID = int(os.getenv("GROUP_ID", "-1002432150473"))

# 🤖 Telegram bot setup
bot = telebot.TeleBot(BOT_TOKEN)

# 🔑 Gemini API setup
genai.configure(api_key=GEMINI_API_KEY)

# 🌐 Flask app for webhook
app = Flask(__name__)

@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# 🏁 Start Command
@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "👋 Gemini AI Doubt Solver Active!\nSend your NEET/JEE question in Gujarati or English.")
    else:
        bot.reply_to(message, "⚠️ Access Denied! Only the owner or authorized group can use this bot.")


# 🧠 Handle text or photo messages
@bot.message_handler(content_types=["text", "photo"])
def handle_message(message):
    # Access check
    if message.chat.id != GROUP_ID and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Access denied.")
        return

    # Handle photo input (future feature)
    if message.content_type == "photo":
        bot.reply_to(message, "🖼️ Photo received! (Coming soon...)")
        return

    try:
        question = message.text
        bot.send_chat_action(message.chat.id, "typing")  # show typing indicator

        # ✅ Use Gemini 1.5 Flash (latest model)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(f"You are a Gujarati NEET/JEE tutor. Answer this:\n{question}")

        # Send the answer
        if response and response.text:
            bot.reply_to(message, f"🧠 જવાબ:\n{response.text}")
        else:
            bot.reply_to(message, "⚠️ Sorry, I couldn't generate a response.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")


# 🚀 Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)