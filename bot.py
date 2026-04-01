import os
from flask import Flask, redirect
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- إعدادات السيرفر (Render) ---
app = Flask('')
user_data = {}

# الرابط الذي يربحك المال (ضع رابط أوو آي أو الخاص بك هنا)
FINAL_AD_LINK = "https://ouo.io/Q8wFlh"

@app.route('/')
def home():
    return "✅ SERVER IS LIVE V7.2"

@app.route('/click/<int:user_id>')
def register_click(user_id):
    # إضافة الربح تلقائياً بمجرد فتح الرابط
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.0, "invites": 0}
    
    user_data[user_id]["balance"] += 0.0200
    print(f"💰 ضغطة جديدة! المستخدم {user_id} حصل على 0.02$")
    
    # تحويل المستخدم فوراً لرابط الإعلانات
    return redirect(FINAL_AD_LINK)

def run():
    # رندر يستخدم البوت 10000 تلقائياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات التلجرام ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
# رابط الرندر الخاص بك الذي أرسلته
SERVER_URL = "https://super-money-bot-2.onrender.com"

def get_user_db(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.0, "invites": 0}
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = get_user_db(user.id)
    
    # نظام الإحالة (Referral)
    if context.args and context.args[0].isdigit():
        ref_id = int(context.args[0])
        if ref_id != user.id and user.id not in user_data:
            r_db = get_user_db(ref_id)
            r_db["balance"] += 0.20
            r_db["invites"] += 1

    # رابط الضغط السحري (يمر عبر الرندر أولاً)
    click_url = f"{SERVER_URL}/click/{user.id}"

    welcome_text = (
        f"🛡️ **نظام الشحن السحابي الذكي V7.2**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 رصيدك الحالي: `{db['balance']:.4f}$` \n"
        f"👥 عدد الإحالات: `{db['invites']}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 **اضغط على أي بطاقة لشحن رصيدك بـ 0.02$ فوراً!**"
    )
    
    kb = [
        [InlineKeyboardButton("💳 بطاقة 01", url=click_url), InlineKeyboardButton("💳 بطاقة 02", url=click_url)],
        [InlineKeyboardButton("💳 بطاقة 03", url=click_url), InlineKeyboardButton("💳 بطاقة 04", url=click_url)],
        [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="ref")],
        [InlineKeyboardButton("💎 تحويل (8$)", callback_data="draw")],
        [InlineKeyboardButton("👥 رابط الإحالة (+0.20$)", callback_data="share")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = get_user_db(user_id)
    await query.answer()

    if query.data == "ref":
        await query.edit_message_text(
            f"💰 **تم التحديث!**\nرصيدك الآن هو: `{db['balance']:.4f}$`", 
            reply_markup=query.message.reply_markup, 
            parse_mode="Markdown"
        )
    elif query.data == "draw":
        if db["balance"] < 8.0:
            await query.message.reply_text(f"❌ رصيدك الحالي `{db['balance']:.4f}$` وهو أقل من الحد الأدنى للسحب (8$).")
        else:
            await query.message.reply_text("✅ مبروك! رصيدك جاهز. أرسل الآيدي الخاص بك الآن.")
    elif query.data == "share":
        bot_info = await context.bot.get_me()
        await query.message.reply_text(f"🔗 **رابط إحالتك الخاص:**\n`https://t.me/{bot_info.username}?start={user_id}`\n\n(ارسل الرابط لأصدقائك واحصل على 0.20$ عن كل شخص!)")

def main():
    # تشغيل سيرفر الفلاسك في خلفية مستقلة
    Thread(target=run).start()
    
    # تشغيل البوت
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("🚀 BOT IS RUNNING ON RENDER URL...")
    application.run_polling()

if __name__ == "__main__":
    main()
        
