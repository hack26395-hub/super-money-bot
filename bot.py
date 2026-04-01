import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- نظام الحماية والبقاء مستيقظاً ---
app = Flask('')
@app.route('/')
def home():
    return "🛡️ SYSTEM SECURED & ONLINE V5.0"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

# قاعدة بيانات وهمية (تصفر عند إعادة تشغيل السيرفر)
# في الواقع يفضل استخدام JSON أو SQLite لحفظ البيانات بشكل دائم
user_data = {} 

def get_user_db(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "balance": 0.0000,
            "invites": 0,
            "step": "start",
            "id_game": None
        }
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = get_user_db(user.id)
    
    # التحقق من الإحالة (Referral)
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        if referrer_id != user.id and user.id not in user_data: # مستخدم جديد فعلاً
            ref_db = get_user_db(referrer_id)
            ref_db["balance"] += 0.2000
            ref_db["invites"] += 1

    welcome_text = (
        f"🛡️ **نظام الشحن السحابي المشفر V5**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"❇️ مـرحـباً بـك: {user.first_name}\n"
        f"💰 رصيدك الحالي: `{db['balance']:.4f}$`\n"
        f"👥 عدد الإحالات: `{db['invites']}`\n"
        f"🔒 الحالة: متصل (SSL Secure)\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        "📥 **المهمة المطلوبة لتوليد الرصيد:**\n"
        "اضغط على البطاقات أدناه. كل بطاقة تمنحك **0.0200$**.\n"
        "تجمع الرصيد ثم حوله إلى جواهر (الحد الأدنى 8$).\n\n"
        "⬇️ **بـطـاقـات الـتـفـعـيـل الـمـتـاحة**"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 بطاقة 01 (+0.02$)", url="https://ouo.io/Q8wFlh"), InlineKeyboardButton("💳 بطاقة 02 (+0.02$)", url="https://ouo.io/4bRZy7")],
        [InlineKeyboardButton("💳 بطاقة 03 (+0.02$)", url="https://ouo.io/8CbQnG"), InlineKeyboardButton("💳 بطاقة 04 (+0.02$)", url="https://ouo.io/ncwrz1")],
        [InlineKeyboardButton("💳 بطاقة 05 (+0.02$)", url="https://ouo.io/A9Y3lp"), InlineKeyboardButton("💳 بطاقة 06 (+0.02$)", url="https://ouo.io/F0U5qqI")],
        [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="refresh"), InlineKeyboardButton("💎 تحويل للجواهر", callback_data="withdraw")],
        [InlineKeyboardButton("👥 دعوة الأصدقاء (+0.20$)", callback_data="share")]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = get_user_db(user_id)
    await query.answer()

    if query.data == "refresh":
        # محاكاة زيادة الرصيد عند الضغط (وهمية لزيادة التفاعل)
        db["balance"] += 0.0200
        new_text = (
            f"💰 **تم تحديث محفظتك السحابية**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💵 الرصيد الجديد: `{db['balance']:.4f}$` \n"
            f"🚀 متبقي لك: `{max(0, 8 - db['balance']):.4f}$` للسحب."
        )
        await query.edit_message_text(new_text, reply_markup=query.message.reply_markup, parse_mode="Markdown")

    elif query.data == "withdraw":
        if db["balance"] < 8.0:
            await query.message.reply_text(
                f"❌ **فشل نظام التحويل!**\n\n"
                f"الحد الأدنى للتحويل إلى جواهر هو **8.0000$**.\n"
                f"رصيدك الحالي: `{db['balance']:.4f}$`.\n\n"
                f"💡 نصيحة: قم بدعوة أصدقائك لجمع 1$ عن كل 5 أشخاص!"
            )
        else:
            await query.message.reply_text("✅ **الرصيد مكتمل!**\nأرسل الآن كلمة (تم) لبدء ربط الآيدي.")

    elif query.data == "share":
        bot_info = await context.bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        await query.message.reply_text(
            f"👥 **نظام الإحالة المكثف**\n\n"
            f"ارسل هذا الرابط لأصدقائك.\n"
            f"ستحصل على **0.2000$** عن كل شخص يدخل!\n\n"
            f"🔗 رابطك:\n `{ref_link}`",
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    db = get_user_db(user_id)

    if text == "تم":
        if db["balance"] < 8.0:
            await update.message.reply_text("⚠️ رصيدك أقل من 8$، لا يمكنك التفعيل الآن.")
            return
        db["step"] = "awaiting_id"
        await update.message.reply_text(f"❇️ تم التحقق من الرصيد.. `{db['balance']:.4f}$` متوفرة.\n\nالآن، اكتب الـ **ID** الخاص بك ليتم شحن الجواهر مباشرة:")
    
    elif text.isdigit() and len(text) > 5:
        if db["step"] != "awaiting_id":
            await update.message.reply_text("⚠️ يرجى الوصول للحد الأدنى (8$) ثم كتابة (تم) أولاً.")
            return

        db["id_game"] = text
        msg = await update.message.reply_text("📡 جاري الاتصال بقاعدة بيانات اللعبة...")
        await asyncio.sleep(2)
        await msg.edit_text(f"🛰️ تم ربط الآيدي {text} بالسيرفر..\nجاري توليد الجواهر من الرصيد الحسابي...")
        await asyncio.sleep(2)
        
        await update.message.reply_text(
            f"✅ **عملية الشحن قيد المعالجة!**\n\n"
            f"الآيدي: `{text}`\n"
            f"المبلغ المحول: `{db['balance']:.2f}$` ما يعادل **50,000 جوهرة**.\n\n"
            f"📢 ستصلك الجواهر خلال ساعات. لا تغادر البوت لضمان نجاح العملية."
        , parse_mode="Markdown")

def main():
    keep_alive()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    from telegram.ext import CallbackQueryHandler
    
    print("✅ Bot V5.0 is Online...")
    application.run_polling()

if __name__ == "__main__":
    main()
                
