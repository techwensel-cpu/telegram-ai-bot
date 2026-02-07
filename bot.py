import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --------------------------
# Load .env variables
# --------------------------
load_dotenv()  # .env file load karega

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Safety check
if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("BOT_TOKEN or OPENAI_API_KEY is not set!")

# --------------------------
# OpenAI Client
# --------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------
# Telegram message reply function
# --------------------------
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

# --------------------------
# Telegram bot application
# --------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot Started...")  # Render logs me dikhega
app.run_polling()
