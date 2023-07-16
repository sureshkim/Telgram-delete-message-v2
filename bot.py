import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text('Bot started. I will automatically delete messages in channels where I am added, except for videos (MKV, MP4).')

def delete_message(update: Update, message_id: int) -> None:
    """Delete a specific message in the chat."""
    try:
        update.message.bot.delete_message(update.message.chat_id, message_id)
    except Exception as e:
        print(f'Error deleting message: {str(e)}')

def handle_text_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming text messages."""
    message = update.message
    # Process and handle text messages here
    # Delete the message after processing (Only if it's from a channel)
    if message.chat.type == 'channel':
        delete_message(update, message.message_id)

def handle_media_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming media messages (photos, videos, etc.)."""
    message = update.message
    # Process and handle media messages here
    # Delete the message after processing (Only if it's from a channel)
    if message.chat.type == 'channel':
        delete_message(update, message.message_id)

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages (except commands)."""
    if update.message.text:
        handle_text_message(update, context)
    elif update.message.media_group_id or update.message.photo or update.message.video or update.message.document:
        handle_media_message(update, context)

def main() -> None:
    """Main function to run the bot."""
    token = os.environ.get('BOT_TOKEN')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Register message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.media_group | Filters.photo | Filters.video | Filters.document, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
                   
