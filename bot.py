import os
import sqlite3
import asyncio
from flask import Flask, redirect
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- إعدادات قاعدة البيانات (تطوير V9.0) ---
DB_NAME = "users_pro_v9.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, balance REAL, invites INTEGER, clicks INTEGER, level TEXT)''')
    conn.commit()
    conn.close()

def get_user_db(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT balance, invites, clicks, level FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row: return {"balance": row[0], "invites": row[1], "clicks": row[2], "level": row[3]}
    return {"balance": 0.0, "invites": 0, "clicks": 0, "level": "مبتدئ 🌱"}

def update_user_db(user_id, balance=None, invites=None, clicks=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    user = get_user_db(user_id)
    
    new_bal = balance if balance is not None else user["balance"]
    new_inv = invites if invites is not None else user["invites"]
    new_clk = clicks if clicks is not None else user["clicks"]
    
    # تحديد المستوى بناءً على الرصيد
    new_lvl = "مبتدئ 🌱"
    if new_bal > 5: new_lvl = "محترف ⚡"
    if new_bal > 15: new_lvl = "ملك الشحن 👑"
    
    c.execute("INSERT OR REPLACE INTO users (user_id, balance, invites, clicks, level) VALUES (?, ?, ?, ?, ?)",
              (user_id, new_bal, new_inv, new_clk, new_lvl))
    conn.commit()
    conn.close()

# --- إعدادات السيرفر والتلجرام ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
SERVER_URL = "https://super-money-bot-2.onrender.com"
FINAL_AD_LINK = "https://ouo.io/Q8wFlh"

app = Flask(__name__)
tg_app = Application.builder().token(TOKEN).build()

def send_instant_warning(user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    warning_text = (
        "🛑 **إيقاف مؤقت للنظام!**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "نظام الحماية اكتشف استهلاكاً عالياً للنقرات من منطقتك.\n\n"
        "⚠️ **لتجنب حظر حسابك:**\n"
        "1️⃣ أغلق البوت تماماً.\n"
        "2️⃣ قم بتشغيل الـ **VPN** (دولة ألمانيا 🇩🇪 أو أمريكا 🇺🇸).\n"
        "3️⃣ أعد المحاولة بعد دقيقة واحدة.\n\n"
        "*سيتم تجميد الأرباح في حال مخالفة التعليمات!*"
    )
    loop.run_until_complete(tg_app.bot.send_message(chat_id=user_id, text=warning_text, parse_mode="Markdown"))

@app.route('/')
def home(): return "💎 GemsMatrix PRO V9.0 IS ACTIVE"

@app.route('/click/<int:user_id>')
def register_click(user_id):
    user = get_user_db(user_id)
    new_clk = user["clicks"] + 1
    new_bal = user["balance"] + 0.0200
    update_user_db(user_id, balance=new_bal, clicks=new_clk)
    
    if new_clk >= 4:
        Thread(target=send_instant_warning, args=(user_id,)).start()
        update_user_db(user_id, clicks=0) 
        
    return redirect(FINAL_AD_LINK)

# --- واجهة البوت المطورة ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # نظام الإحالة المتطور
    if context.args and context.args[0].isdigit():
        ref_id = int(context.args[0])
        if ref_id != user.id:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT user_id FROM users WHERE user_id=?", (user.id,))
            if not c.fetchone(): 
                inviter = get_user_db(ref_id)
                update_user_db(ref_id, balance=inviter["balance"] + 0.20, invites=inviter["invites"] + 1)
            conn.close()

    db = get_user_db(user.id)
    magic_url = f"{SERVER_URL}/click/{user.id}"
    
    welcome_text = (
        f"💎 **مرحباً بك في GemsMatrix PRO**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 المستـخدم: `{user.first_name}`\n"
        f"🏆 المستـوى: *{db['level']}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 الرصـيد: `{db['balance']:.4f}$` \n"
        f"👥 الإحالات: `{db['invites']}` شخص\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *ملاحظة: الرصيد يحدث تلقائياً عند الضغط على التحديث.*"
    )
    
    kb = [
        [InlineKeyboardButton("💳 شحن بطاقة (A)", url=magic_url), InlineKeyboardButton("💳 شحن بطاقة (B)", url=magic_url)],
        [InlineKeyboardButton("💳 شحن بطاقة (C)", url=magic_url), InlineKeyboardButton("💳 شحن بطاقة (D)", url=magic_url)],
        [InlineKeyboardButton("📊 تحديث الحساب", callback_data="ref"), InlineKeyboardButton("🏦 سحب الأرباح", callback_data="draw")],
        [InlineKeyboardButton("🎁 مكافأة الإحالة (+0.20$)", callback_data="share")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = get_user_db(user_id)
    await query.answer()
    
    if query.data == "ref":
        await query.edit_message_text(
            f"🔄 **تم مزامنة البيانات بنجاح!**\n\n"
            f"💰 رصيدك الحالي: `{db['balance']:.4f}$` \n"
            f"🏅 مستواك الحالي: *{db['level']}*\n\n"
            f"استمر في الضغط لزيادة أرباحك اليومية!",
            reply_markup=query.message.reply_markup, parse_mode="Markdown"
        )
    elif query.data == "draw":
        if db["balance"] < 8.0:
            await query.message.reply_text(f"⚠️ **عذراً، الوصول مرفوض!**\n\nيجب أن يصل رصيدك إلى **8.00$** على الأقل.\nنقصك الحالي: `{8.0 - db['balance']:.2f}$`")
        else:
            await query.message.reply_text("🎊 **مبروك! وصلت للحد الأدنى.**\n\nيرجى كتابة رقم محفظتك أو ID اللعبة وسيتم التحويل خلال 24 ساعة.")
    elif query.data == "share":
        bot_info = await context.bot.get_me()
        share_msg = (
            f"🚀 **اربح الدولارات والجواهر مجاناً!**\n\n"
            f"سجل من خلال رابطي واحصل على هدية دخول:\n"
            f"https://t.me/{bot_info.username}?start={user_id}"
        )
        await query.message.reply_text(share_msg)

def main():
    init_db()
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CallbackQueryHandler(handle_callback))
    print("🚀 BOT V9.0 IS LIVE WITH PRO UI")
    tg_app.run_polling()

if __name__ == "__main__": main()
                    
