import os
import subprocess
import sys
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = '7803904870:AAERhP2w4jPibvB_NuHyjBQRu_a1IKNXMwQ'
user_dirs = {}

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_dirs:
        user_dirs[user_id] = os.path.expanduser("~")
    
    current_dir = user_dirs[user_id]
    command = update.message.text.strip()

    if command.startswith("cd "):
        path = command[3:].strip()
        new_dir = os.path.abspath(os.path.join(current_dir, path))
        if os.path.isdir(new_dir):
            user_dirs[user_id] = new_dir
            await update.message.reply_text(f"root@stxtamfan:~{new_dir}#")
        else:
            await update.message.reply_text(f"No such directory: {new_dir}")
        return

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=600
        )
        output = result.stdout.strip() + "\n" + result.stderr.strip()
        output = output.strip()
        if not output:
            output = "root@stxtamfan:~#"
    except Exception as e:
        output = f"Error: {str(e)}"

    for i in range(0, len(output), 4000):
        await update.message.reply_text(output[i:i+4000])


# Handler: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot by @kecee_pyrite sudah aktif. Kirim perintah shell \n\nFolder binary ada di /config \n\nSilahkan ketik cd /config \n\nLalu ketik ./stx")

# Handler: /restartbot
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot restarted...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Fungsi utama
def main():
    token = BOT_TOKEN
    if len(sys.argv) > 1:
        token = sys.argv[1]

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restartbot", restart))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_command))
    
    print("Bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()