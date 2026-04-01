import os
import sqlite3
import asyncio
from flask import Flask, redirect
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- إعدادات قاعدة البيانات ---
DB_NAME = "users_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, balance REAL, invites INTEGER, clicks INTEGER)''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT balance, invites, clicks FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row: return {"balance": row[0], "invites": row[1], "clicks": row[2]}
    return {"balance": 0.0, "invites": 0, "clicks": 0}

def update_user(user_id, balance=None, invites=None, clicks=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    user = get_user(user_id)
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

# دالة لإرسال رسالة للمستخدم من داخل السيرفر
def send_vpn_warning(user_id):
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
def home(): return "✅ System V8.1 Online"

@app.route('/click/<int:user_id>')
def register_click(user_id):
    user = get_user(user_id)
    new_clicks = user["clicks"] + 1
    new_balance = user["balance"] + 0.0200
    
    update_user(user_id, balance=new_balance, clicks=new_clicks)
    
    # إذا خلص الـ 4 روابط، نبعت له الرسالة فوراً على التلجرام
    if new_clicks >= 4:
        Thread(target=send_vpn_warning, args=(user_id,)).start()
        update_user(user_id, clicks=0) # تصفير العداد للمرة الجاية بعد الـ VPN
        
    return redirect(FINAL_AD_LINK)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- أوامر التلجرام ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = get_user(user.id)
    magic_url = f"{SERVER_URL}/click/{user.id}"
    
    welcome_text = (
        f"🛡️ **محفظة الشحن الدائمة**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 الرصيد الحالي: `{db['balance']:.4f}$` \n"
        f"👥 الإحالات: `{db['invites']}`\n\n"
        f"✅ رصيدك محفوظ في قاعدة البيانات."
    )
    kb = [[InlineKeyboardButton(f"💳 بطاقة تفعيل {i:02d}", url=magic_url) for i in range(1, 3)],
          [InlineKeyboardButton(f"💳 بطاقة تفعيل {i:02d}", url=magic_url) for i in range(3, 5)],
          [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="ref")]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    db = get_user(query.from_user.id)
    await query.answer()
    if query.data == "ref":
        await query.edit_message_text(f"💰 **الرصيد المحدث:** `{db['balance']:.4f}$`", 
                                     reply_markup=query.message.reply_markup, parse_mode="Markdown")

def main():
    init_db()
    Thread(target=run_flask).start()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CallbackQueryHandler(handle_callback))
    print("🚀 BOT V8.1 LIVE ON RENDER")
    tg_app.run_polling()

if __name__ == "__main__": main()
    
