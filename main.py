#!/usr/bin/env python3
import os
import openai
import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")

CHAT = 1

def ask(question):
  return openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[{"role": "user", "content": question}]).choices[0].message.content
  # return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}]).choices[0].message.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Chat started")
    await update.message.reply_text("Ask a question")
    return CHAT

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # user = update.message.from_user
    logger.info("Q: %s", update.message.text)
    reply = ask(update.message.text)
    await update.message.reply_text(reply)
    return CHAT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()


