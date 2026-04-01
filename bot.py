import os
from flask import Flask, redirect, request
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- إعدادات السيرفر (Render) ---
app = Flask(__name__)
user_data = {}

# رابط الربح الخاص بك (Ouo.io)
FINAL_AD_LINK = "https://ouo.io/Q8wFlh"

# الصفحة الرئيسية (لمنع رسالة Not Found)
@app.route('/')
def home():
    return "✅ Server is Running! The bot is ready to count your money."

# رابط احتساب النقرات
@app.route('/click/<user_id>')
def register_click(user_id):
    try:
        u_id = int(user_id)
        if u_id not in user_data:
            user_data[u_id] = {"balance": 0.0, "invites": 0}
        
        # إضافة 0.02$ فوراً عند الضغط
        user_data[u_id]["balance"] += 0.0200
        print(f"💰 Done! User {u_id} earned 0.02$")
        
        # التحويل التلقائي للرابط الربحي
        return redirect(FINAL_AD_LINK)
    except:
        return "⚠️ Error: Invalid User ID."

def run():
    # رندر يستخدم بورت 10000 أو PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات التلجرام ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
SERVER_URL = "https://super-money-bot-2.onrender.com"

def get_user_db(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.0, "invites": 0}
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = get_user_db(user.id)
    
    # نظام الإحالة
    if context.args and context.args[0].isdigit():
        ref_id = int(context.args[0])
        if ref_id != user.id and user.id not in user_data:
            r_db = get_user_db(ref_id)
            r_db["balance"] += 0.20
            r_db["invites"] += 1

    # رابط الزر السحري (سيقوم رندر باحتساب الربح ثم التحويل)
    magic_url = f"{SERVER_URL}/click/{user.id}"

    welcome_text = (
        f"🛡️ **نظام الشحن التلقائي V7.3**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 رصيدك الحالي: `{db['balance']:.4f}$` \n"
        f"👥 عدد الإحالات: `{db['invites']}`\n\n"
        f"✅ **اضغط على أي بطاقة، وسيتم إضافة الربح تلقائياً فوراً!**"
    )
    
    kb = [
        [InlineKeyboardButton("💳 بطاقة تفعيل 01", url=magic_url), InlineKeyboardButton("💳 بطاقة تفعيل 02", url=magic_url)],
        [InlineKeyboardButton("💳 بطاقة تفعيل 03", url=magic_url), InlineKeyboardButton("💳 بطاقة تفعيل 04", url=magic_url)],
        [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="ref")],
        [InlineKeyboardButton("💎 سحب الجواهر (8$)", callback_data="draw")],
        [InlineKeyboardButton("👥 رابط الإحالة (+0.20$)", callback_data="share")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    db = get_user_db(query.from_user.id)
    await query.answer()

    if query.data == "ref":
        await query.edit_message_text(
            f"💰 **تحديث الرصيد:** `{db['balance']:.4f}$` \n\nاضغط على البطاقات لزيادة رصيدك!", 
            reply_markup=query.message.reply_markup, 
            parse_mode="Markdown"
        )
    elif query.data == "draw":
        if db["balance"] < 8.0:
            await query.message.reply_text(f"❌ رصيدك `{db['balance']:.4f}$` أقل من الحد الأدنى (8$).")
        else:
            await query.message.reply_text("✅ رصيدك جاهز! أرسل الآيدي الخاص بك.")
    elif query.data == "share":
        bot_info = await context.bot.get_me()
        await query.message.reply_text(f"🔗 رابط إحالتك:\n`https://t.me/{bot_info.username}?start={query.from_user.id}`")

def main():
    # تشغيل السيرفر في خلفية Thread
    Thread(target=run).start()
    
    # تشغيل البوت
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("🚀 BOT IS ONLINE AND SYNCED WITH RENDER")
    application.run_polling()

if __name__ == "__main__":
    main()
        
