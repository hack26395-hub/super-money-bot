import os
import sqlite3
import asyncio
from flask import Flask, redirect
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- إعدادات قاعدة البيانات (SQLite) لضمان بقاء الرصيد ---
DB_NAME = "users_v82.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, balance REAL, invites INTEGER, clicks INTEGER)''')
    conn.commit()
    conn.close()

def get_user_db(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT balance, invites, clicks FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row: return {"balance": row[0], "invites": row[1], "clicks": row[2]}
    return {"balance": 0.0, "invites": 0, "clicks": 0}

def update_user_db(user_id, balance=None, invites=None, clicks=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    user = get_user_db(user_id)
    new_bal = balance if balance is not None else user["balance"]
    new_inv = invites if invites is not None else user["invites"]
    new_clk = clicks if clicks is not None else user["clicks"]
    c.execute("INSERT OR REPLACE INTO users (user_id, balance, invites, clicks) VALUES (?, ?, ?, ?)",
              (user_id, new_bal, new_inv, new_clk))
    conn.commit()
    conn.close()

# --- إعدادات السيرفر والتلجرام ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
SERVER_URL = "https://super-money-bot-2.onrender.com"
FINAL_AD_LINK = "https://ouo.io/Q8wFlh"

app = Flask(__name__)
tg_app = Application.builder().token(TOKEN).build()

# دالة إرسال التنبيه الفوري للمستخدم
def send_instant_warning(user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    warning_text = (
        "⚠️ **تنبيه أمني عاجل من النظام!**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "لقد استنفدت جميع النقرات المتاحة لهويتك الحالية.\n\n"
        "🛡️ **الإجراء المطلوب:**\n"
        "يجب عليك تغيير الـ **VPN** الآن واختيار دولة (أمريكا أو ألمانيا) لضمان احتساب النقاط، "
        "وإلا سيتم تجميد رصيدك وحظر حسابك نهائياً! 🚫"
    )
    loop.run_until_complete(tg_app.bot.send_message(chat_id=user_id, text=warning_text, parse_mode="Markdown"))

@app.route('/')
def home(): return "✅ Bot v8.2 Permanent DB Online"

@app.route('/click/<int:user_id>')
def register_click(user_id):
    user = get_user_db(user_id)
    new_clk = user["clicks"] + 1
    new_bal = user["balance"] + 0.0200
    update_user_db(user_id, balance=new_bal, clicks=new_clk)
    
    if new_clk >= 4:
        Thread(target=send_instant_warning, args=(user_id,)).start()
        update_user_db(user_id, clicks=0) # تصفير العداد للمرة القادمة
        
    return redirect(FINAL_AD_LINK)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- واجهة البوت والأزرار ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # معالجة الإحالة عند الدخول أول مرة
    if context.args and context.args[0].isdigit():
        ref_id = int(context.args[0])
        if ref_id != user.id:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT user_id FROM users WHERE user_id=?", (user.id,))
            if not c.fetchone(): # المستخدم جديد فعلاً
                inviter = get_user_db(ref_id)
                update_user_db(ref_id, balance=inviter["balance"] + 0.20, invites=inviter["invites"] + 1)
            conn.close()

    db = get_user_db(user.id)
    magic_url = f"{SERVER_URL}/click/{user.id}"
    
    welcome_text = (
        f"🛡️ **محفظة الشحن الدائمة V8.2**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 الرصيد الحالي: `{db['balance']:.4f}$` \n"
        f"👥 الإحالات: `{db['invites']}`\n\n"
        f"✅ رصيدك محفوظ ولن يتغير عند التحديث."
    )
    
    kb = [
        [InlineKeyboardButton("💳 بطاقة تفعيل 01", url=magic_url), InlineKeyboardButton("💳 بطاقة تفعيل 02", url=magic_url)],
        [InlineKeyboardButton("💳 بطاقة تفعيل 03", url=magic_url), InlineKeyboardButton("💳 بطاقة تفعيل 04", url=magic_url)],
        [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="ref"), InlineKeyboardButton("💎 تحويل للجواهر", callback_data="draw")],
        [InlineKeyboardButton("👥 دعوة الأصدقاء (+0.20$)", callback_data="share")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = get_user_db(user_id)
    await query.answer()
    
    if query.data == "ref":
        await query.edit_message_text(
            f"💰 **تم تحديث الرصيد:** `{db['balance']:.4f}$` \n\nاضغط على البطاقات لزيادة أرباحك!",
            reply_markup=query.message.reply_markup, parse_mode="Markdown"
        )
    elif query.data == "draw":
        if db["balance"] < 8.0:
            await query.message.reply_text(f"❌ فشل النظام: رصيدك `{db['balance']:.4f}$` أقل من الحد الأدنى (8$).")
        else:
            await query.message.reply_text("✅ رصيدك جاهز! أرسل الآيدي الخاص بك.")
    elif query.data == "share":
        bot_info = await context.bot.get_me()
        await query.message.reply_text(f"🔗 **رابط إحالتك:**\n`https://t.me/{bot_info.username}?start={user_id}`")

def main():
    init_db()
    Thread(target=run_flask).start()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CallbackQueryHandler(handle_callback))
    print("🚀 BOT V8.2 IS LIVE WITH ALL FEATURES")
    tg_app.run_polling()

if __name__ == "__main__": main()
    
