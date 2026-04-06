import os
import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Rose Bot အလုပ်လုပ်နေပါပြီ!")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for new_user in update.message.new_chat_members:
        if new_user.id == context.bot.id: continue
        mention = f"[{new_user.first_name}](tg://user?id={new_user.id})"
        await update.message.reply_text(f"ဟိုင်း {mention} ရေ... ကြိုဆိုပါတယ်!", parse_mode=constants.ParseMode.MARKDOWN)

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if user_status.status not in [constants.ChatMemberStatus.OWNER, constants.ChatMemberStatus.ADMINISTRATOR]:
        return await update.message.reply_text("Admin ပဲ သုံးလို့ရပါတယ်။")
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Ban ပြီးပါပြီ။")
    else:
        await update.message.reply_text("Ban ချင်သူကို Reply ပြန်ပြီး /ban ရိုက်ပါ။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('ban', ban))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()

