from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from bots.core.phone.analyzer import analyze_phone_number
from bots.core.phone.formatter import format_phone_result


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de Análise Telefônica\n\n"
        "Envie um número de telefone para análise.\n"
        "Exemplo:\n"
        "11999999999"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    result = analyze_phone_number(text)
    response = format_phone_result(result)

    await update.message.reply_text(response)


def main():
    TOKEN = "8279564257:AAFhxmF5T70HwLrfTftFuJ0VG6xApN6Yu4s"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot Telegram rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
