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
    return "🛡️ SYSTEM SECURED & ONLINE V4.0"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# قاعدة بيانات مؤقتة لتفادي القلتشات
user_steps = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_steps[user.id] = "started" # تسجيل بداية المستخدم
    
    welcome_text = (
        f"🛡️ **نظام الشحن السحابي المشفر V4**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"❇️ مرحباً بك عـمـيـلـنـا: {user.first_name}\n"
        f"🔒 الحالة: اتصال آمن (SSL 256-bit)\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        "📥 **المهمة المطلوبة لتفعيل الرصيد:**\n"
        "يجب فك تشفير الـ 21 بطاقة أمنية لجمع الأكواد.\n\n"
        "⚠️ **تنبيهات هامة:**\n"
        "• يمنع استخدام حسابات وهمية (سيتم حظرك).\n"
        "• تأكد من تحميل جميع الملفات لإثبات نشاطك.\n"
        "• شغل VPN (فرنسا/أمريكا) لتسريع المعالجة.\n\n"
        "⬇️ **بـطـاقـات الـتـفـعـيـل الـمـتـاحة**"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 بطاقة 01", url="https://ouo.io/Q8wFlh"), InlineKeyboardButton("💳 بطاقة 02", url="https://ouo.io/4bRZy7")],
        [InlineKeyboardButton("💳 بطاقة 03", url="https://ouo.io/8CbQnG"), InlineKeyboardButton("💳 بطاقة 04", url="https://ouo.io/ncwrz1")],
        [InlineKeyboardButton("💳 بطاقة 05", url="https://ouo.io/A9Y3lp"), InlineKeyboardButton("💳 بطاقة 06", url="https://ouo.io/F0U5qqI")],
        [InlineKeyboardButton("💳 بطاقة 07", url="https://ouo.io/XW6G92"), InlineKeyboardButton("💳 بطاقة 08", url="https://ouo.io/bgy7tS")],
        [InlineKeyboardButton("💳 بطاقة 09", url="https://ouo.io/Aa195y"), InlineKeyboardButton("💳 بطاقة 10", url="https://ouo.io/Vedw2O")],
        [InlineKeyboardButton("💳 بطاقة 11", url="https://ouo.io/NJtakV"), InlineKeyboardButton("💳 بطاقة 12", url="https://ouo.io/gaHDvH")],
        [InlineKeyboardButton("💳 بطاقة 13", url="https://ouo.io/ejEdRS"), InlineKeyboardButton("💳 بطاقة 14", url="https://ouo.io/J4xY1a")],
        [InlineKeyboardButton("💳 بطاقة 15", url="https://ouo.io/I6NR5A0"), InlineKeyboardButton("💳 بطاقة 16", url="https://ouo.io/bLWa7C")],
        [InlineKeyboardButton("💳 بطاقة 17", url="https://ouo.io/nnOkeH"), InlineKeyboardButton("💳 بطاقة 18", url="https://ouo.io/je3Nhy")],
        [InlineKeyboardButton("💳 بطاقة 19", url="https://ouo.io/EVZbqI"), InlineKeyboardButton("💳 بطاقة 20", url="https://ouo.io/vcim0gM")],
        [InlineKeyboardButton("🔥 هـديـة الـمـلـيـون جـوهـرة 🔥", url="https://ouo.io/vcim0gM")]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_steps[user_id] = "photo_sent"
    await update.message.reply_text("✅ **تم فحص الصورة بنجاح!**\nالنظام تأكد من تحميل الملفات. أرسل كلمة (تم) الآن لربط حسابك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    step = user_steps.get(user_id, "start")

    if text == "تم":
        user_steps[user_id] = "awaiting_id"
        await update.message.reply_text(f"❇️ أهلاً يا {user_name}.. تم التحقق من هويتك.\n\nالآن، قم بكتابة الـ **ID** الخاص بك بدقة ليتم ربطه بسيرفر الشحن:")
    
    elif text.isdigit() and len(text) > 5:
        if step != "awaiting_id":
            await update.message.reply_text("⚠️ يرجى الضغط على كلمة (تم) أولاً قبل إرسال الآيدي.")
            return

        user_steps[user_id] = "id_sent"
        msg = await update.message.reply_text("📡 جاري محاكاة الاتصال بخوادم اللعبة...")
        await asyncio.sleep(1.5)
        await msg.edit_text("🛰️ تم اختراق جدار الحماية.. جاري حقن الجواهر...")
        await asyncio.sleep(1.5)
        
        bot_info = await context.bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        
        await update.message.reply_text(
            f"✅ **تم العثور على الحساب!**\n\n"
            f"📥 **الخطوة النهائية (التحقق البشري):**\n"
            f"بسبب أنظمة الحماية الجديدة، يجب دعوة **10 أشخاص** عبر رابطك لضمان عدم حظر حسابك.\n\n"
            f"🔗 رابطك الخاص:\n `{ref_link}`\n\n"
            f"أرسل الرابط لأصدقائك، ثم اكتب هنا (**تم الشحن**)."
        , parse_mode="Markdown")
    
    elif text == "تم الشحن":
        if step != "id_sent":
            await update.message.reply_text("⚠️ لم تكتمل خطواتك بعد! أرسل الآيدي أولاً.")
            return
            
        await update.message.reply_text(
            f"💎 **تمت العملية بنجاح يا {user_name}!**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "طلبك الآن في مرحلة التحويل اليدوي. ستصلك الجواهر خلال 24-48 ساعة.\n\n"
            "📢 سنرسل لك إشعاراً فور انتهاء العملية.\n"
            "🚫 **تذكير:** مغادرة البوت تعني إلغاء الطلب فوراً."
        )

def main():
    keep_alive()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is Secured and Running...")
    application.run_polling()

if __name__ == "__main__":
    main()
