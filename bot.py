import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- ပြင်ဆင်ရန် အချက်အလက်များ ---
TOKEN = '8699176485:AAH01MvEzzN5seccvcUcKLrTmvpb-rvB4aI'
BOT_USERNAME = 'TDI_Myanmar_Bot' # သင့် Bot Username
OWNER_LINK = 'https://t.me/TDIGameShop4' # သင့် Link

# /start command - Menu ခလုတ်များပေါ်စေရန်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # အောက်ခြေ Menu ခလုတ်များ
    menu_keyboard = [
        [KeyboardButton("/check (Info စစ်ရန်)"), KeyboardButton("/ton (စျေးနှုန်းကြည့်ရန်)")],
        [KeyboardButton("/help (အကူအညီ)"), KeyboardButton("/adminlist (Admin များ)")]
    ]
    reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    
    # Add to group ခလုတ်ပြာ
    add_btn = [[InlineKeyboardButton("➕ Add to group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
    
    await update.message.reply_text(
        f"Hello {user.first_name}, welcome!\n\nဒီ bot က ဘာလုပ်နိုင်လဲဆိုတော့\n/help နှိပ်ကြည့် 💝",
        reply_markup=reply_markup
    )
    await update.message.reply_text("အောက်က Menu ကိုသုံးနိုင်ပါတယ်-", reply_markup=InlineKeyboardMarkup(add_btn))

# /help command - ပုံထဲကစာသားများ
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "❓ **Help Menu**\n\n"
        "● seller တွေအတွက်ကိုယ့် group မှာ scammer တွေကြောင့် content protection ဖွင့်ထားတဲ့အခါ id တွေ ကို copy ယူနိုင်အောင်လုပ်ပေးနိုင်ပါတယ်။\n\n"
        "● ton seller တွေအတွက် ton address ပို့ရင် copy ယူလို့ရပါတယ်\n\n"
        "🛠 **Commands:**\n"
        "• `/check` - User info ကြည့်ရန် (Reply ထောက်ပါ)\n"
        "• `/ton` - TON Price ကြည့်ရန်\n"
        "• `/adminlist` - Admin List ကြည့်ရန်\n"
        "• `/copy` - စာသားကူးရန် (Reply ထောက်ပါ)\n\n"
        "📊 **Calculator:** `1k+2k` သို့မဟုတ် `1.5m*2` စသဖြင့် ရိုက်တွက်နိုင်ပါတယ်။"
    )
    owner_btn = [[InlineKeyboardButton("🧤 Owner", url=OWNER_LINK)]]
    await update.message.reply_text(help_text, reply_markup=InlineKeyboardMarkup(owner_btn), parse_mode='Markdown')

# /ton command
async def ton_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💎 **TON Current Price**\n\nRate: $1.3"
    btn = [[InlineKeyboardButton("🐥 Copy Price", callback_data='copy')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(btn), parse_mode='Markdown')

# /adminlist command
async def admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return await update.message.reply_text("Group ထဲမှာပဲ သုံးလို့ရပါတယ်။")
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    text = "👮 **Admin List:**\n\n" + "\n".join([f"• {a.user.full_name}" for a in admins])
    await update.message.reply_text(text, parse_mode='Markdown')

# /copy command
async def copy_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original = update.message.reply_to_message.text or update.message.reply_to_message.caption
        await update.message.reply_text(f"📝 **Copied:**\n\n`{original}`", parse_mode='MarkdownV2')
    else:
        await update.message.reply_text("စာကို Reply ထောက်ပြီး /copy လို့ ရိုက်ပါ။")

# စာသားများ တွက်ချက်ခြင်းနှင့် Menu များဖတ်ခြင်း
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "/check" in text:
        user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
        await update.message.reply_text(f"👤 **Name:** {user.full_name}\n🆔 **ID:** `{user.id}`", parse_mode='Markdown')
    elif "/ton" in text: await ton_price(update, context)
    elif "/help" in text: await help_command(update, context)
    elif "/adminlist" in text: await admin_list(update, context)
    
    # Calculator
    elif any(op in text for op in ['+', '-', '*', '/']):
        calc = text.lower().replace('k', '*1000').replace('m', '*1000000')
        calc = re.sub(r'[^0-9+\-*/(). ]', '', calc)
        try:
            result = eval(calc)
            await update.message.reply_text(f"📊 ရလဒ်: {result:,}")
        except: pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ton", ton_price))
    app.add_handler(CommandHandler("adminlist", admin_list))
    app.add_handler(CommandHandler("copy", copy_func))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot စတင်နေပါပြီ...")
    app.run_polling()

