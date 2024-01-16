from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = 'Hier is der Token aus' #er wird nicht gezeigt damit nichts am Bot verändert werden kann
BOT_USERNAME: Final = '@nice_noice_nicy_bot'



# meine commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hey, was geht')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Schreibe was rein, dann bekommst du eine Antwort')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Das ist ein Custom Befehl!')

# meine antwort
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey, wie geht es dir?'
    if 'Wie geht es dir' in processed: 
        return "Gut, danke der Nachfrage "
    if 'du Bot' in processed:
        return "Ich weiß!"
    
    return 'ich verstehe dich nicht'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text  

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    # Nachricht
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Fehler
    app.add_error_handler(error)
    # aktiviert polling
    print('startet')
    app.run_polling(poll_interval=3)  
