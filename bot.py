import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("8269128629:AAFITu17bRqLdejAJ6SHeO2o0CQClu-Zoqg")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}]
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot Started...")
app.run_polling()
