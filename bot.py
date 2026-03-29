import logging
import os
import asyncio
import random
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- نظام البقاء مستيقظاً (KEEP ALIVE) ---
app = Flask('')
@app.route('/')
def home():
    return "SERVER STATUS: ONLINE ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    welcome_text = (
        f"🛡 الـمـركـز الـرئـيـسـي لـلـشـحـن 🛡\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"مرحباً بك عـمـيـلـنـا: {user_first_name}\n"
        f"نظام الاستحقاق التلقائي (V3.0.5) مـفـعـل ✅\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        "📥 لـبـدء عـمـلـيـة الـشـحـن الـفـوري:\n"
        "يجب استخراج أكواد التفعيل من الـ 21 بطاقة بالأسفل.\n\n"
        "📜 الـتـعـلـيـمات الـتـقـنـيـة:\n"
        "🔹 افتح الروابط بالترتيب وحمل ملفات الكود.\n"
        "🔹 أرسل صورة (Screenshot) للملفات لإثبات المهمة.\n"
        "🔹 أرسل (تم) للبدء في ربط الـ ID بالخادم.\n\n"
        "⬇️ بـطـاقـات الـتـفـعـيـل الـمـشـفـرة ⬇️"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 بـطـاقـة 01", url="https://shrinkme.click/Gems-2026-X7"), InlineKeyboardButton("💳 بـطـاقـة 02", url="https://shrinkme.click/Gems-2026-X8")],
        [InlineKeyboardButton("💳 بـطـاقـة 03", url="https://shrinkme.click/Gems-2026-X3"), InlineKeyboardButton("💳 بـطـاقـة 04", url="https://shrinkme.click/Gems-2026-X4")],
        [InlineKeyboardButton("💳 بـطـاقـة 05", url="https://shrinkme.click/Gems-2026-X5"), InlineKeyboardButton("💳 بـطـاقـة 06", url="https://shrinkme.click/Gems-2026-X6")],
        [InlineKeyboardButton("💳 بـطـاقـة 07", url="https://shrinkme.click/Gems-2026-X9"), InlineKeyboardButton("💳 بـطـاق+ة 08", url="https://shrinkme.click/Gems-2026-X10")],
        [InlineKeyboardButton("💳 بـطـاقـة 09", url="https://shrinkme.click/Gems-2026-X11"), InlineKeyboardButton("💳 بـطـاقـة 10", url="https://shrinkme.click/Gems-2026-X12")],
        [InlineKeyboardButton("💳 بـطـاقـة 11", url="https://shrinkme.click/Gems-2026-X13"), InlineKeyboardButton("💳 بـطـاقـة 12", url="https://shrinkme.click/Gems-2026-X14")],
        [InlineKeyboardButton("💳 بـطـاقـة 13", url="https://shrinkme.click/Gems-2026-X15"), InlineKeyboardButton("💳 بـطـاقـة 14", url="https://shrinkme.click/Gems-2026-X16")],
        [InlineKeyboardButton("💳 بـطـاقـة 15", url="https://shrinkme.click/Gems-2026-X17"), InlineKeyboardButton("💳 بـطـاقـة 16", url="https://shrinkme.click/Gems-2026-X18")],
        [InlineKeyboardButton("💳 بـطـاقـة 17", url="https://shrinkme.click/Gems-2026-X19"), InlineKeyboardButton("💳 بـطـاقـة 18", url="https://shrinkme.click/Gems-2026-X20")],
        [InlineKeyboardButton("💳 بـطـاقـة 19", url="https://shrinkme.click/Gems-2026-X21"), InlineKeyboardButton("💳 بـطـاقـة 20", url="https://shrinkme.click/Gems-2026-X22")],
        [InlineKeyboardButton("🔥 هـديـة الـمـلـيـون جـوهـرة 🔥", url="https://shrinkme.click/Gems-2026-X22")]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 تم استلام لقطة الشاشة.. جاري التحليل عبر الذكاء الاصطناعي...\n\n✅ الصور مطابقة! أرسل الآن كلمة (تم) لمتابعة الشحن.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if text == "تم":
        await update.message.reply_text(f"❇️ أهلاً {user_name}.. تم التأكد من تحميل البطاقات الـ 21.\n\nالآن، قم بكتابة الـ **ID** الخاص بك بدقة:")
    
    elif text.isdigit() and len(text) > 5:
        # نظام التحميل الوهمي لزيادة المصداقية
        status_msg = await update.message.reply_text("⏳ جاري البحث عن الحساب في قاعدة البيانات...")
        await asyncio.sleep(1.5)
        await status_msg.edit_text("📡 تم الاتصال بالسيرفر.. جاري فك تشفير البيانات...")
        await asyncio.sleep(1.5)
        await status_msg.edit_text(f"✅ تم العثور على الحساب بنجاح!\nالمستوى: مؤهل للشحن السريع 🚀")
        
        bot_info = await context.bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        
        await update.message.reply_text(
            f"📥 الـتـوثـيـق الـبـشـري مـطـلـوب:\n\n"
            f"نظام الشحن يتطلب منك دعوة **10 أشخاص** فقط عبر رابطك الخاص لضمان استقرار السيرفر وتجنب الحظر.\n\n"
            f"🔗 رابط التفعيل الخاص بك:\n {ref_link}\n\n"
            f"أرسل الرابط لأصدقائك ثم أرسل هنا كلمة (**تم الشحن**)."
        )
    
    elif text == "تم الشحن":
        await update.message.reply_text(
            "💎 تـم وضـع طـلـبـك فـي قـائـمـة الانـتـظـار 💎\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "سيتم تحويل الجواهر إلى حسابك خلال 24-48 ساعة كحد أقصى.\n\n"
            "🔔 سنرسل لك إشعاراً فور اكتمال التحويل.\n"
            "❌ ملاحظة: مغادرة البوت أو حظره قبل استلام الجواهر سيلغي الطلب فوراً."
        )

def main():
    keep_alive()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running perfectly with new updates!")
    application.run_polling()

if __name__ == "__main__":
    main()
