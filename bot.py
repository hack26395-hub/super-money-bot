import logging
import os
import asyncio
import random
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- نظام البقاء مستيقظاً (KEEP ALIVE) ---
# هذا الجزء هو "سر" بقاء البوت شغالاً على رندر 24/7 دون أن ينام.
app = Flask('')
@app.route('/')
def home():
    return "SERVER STATUS: ONLINE ✅ V3.0.5"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------------

# --- إعدادات البوت ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # الحصول على اسم المستخدم الذي أمامه الديناميكي
    current_user_name = update.effective_user.first_name
    
    welcome_text = (
        f"🛡 الـمـركـز الـرئـيـسـي لـلـشـحـن السحابي 🛡\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"❇️ مرحباً بك عـمـيـلـنـا: {current_user_name}\n"
        f"نظام الاستحقاق التلقائي (V3.0.5) مـفـعـل ✅\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        "📥 لـبـدء عـمـلـيـة الـشـحـن الـفـوري:\n"
        "يجب استخراج أكواد التفعيل من الـ 21 بطاقة بالأسفل.\n\n"
        "📜 الـتـعـلـيـمات الـتـقـنـيـة:\n"
        "🔹 افتح الروابط بالترتيب وحمل ملفات الكود.\n"
        "🔹 أرسل صورة (Screenshot) للملفات لإثبات المهمة.\n"
        "🔹 أرسل كلمة (تم) للبدء في ربط الآيدي بالسيرفر.\n\n"
        "⬇️ بـطـاقـات الـتـفـعـيـل الـمـشـفـرة ⬇️"
    )
    
    # الروابط المختصرة (الشغالة)
    keyboard = [
        [InlineKeyboardButton("🔹 بطاقة 01", url="https://shrinkme.click/Gems-2026-X7"), InlineKeyboardButton("🔹 بطاقة 02", url="https://shrinkme.click/Gems-2026-X8")],
        [InlineKeyboardButton("🔹 بطاقة 03", url="https://shrinkme.click/Gems-2026-X3"), InlineKeyboardButton("🔹 بطاقة 04", url="https://shrinkme.click/Gems-2026-X4")],
        [InlineKeyboardButton("🔹 بطاقة 05", url="https://shrinkme.click/Gems-2026-X5"), InlineKeyboardButton("🔹 بطاقة 06", url="https://shrinkme.click/Gems-2026-X6")],
        [InlineKeyboardButton("🔹 بطاقة 07", url="https://shrinkme.click/Gems-2026-X9"), InlineKeyboardButton("🔹 بطاقة 08", url="https://shrinkme.click/Gems-2026-X10")],
        [InlineKeyboardButton("🔹 بطاقة 09", url="https://shrinkme.click/Gems-2026-X11"), InlineKeyboardButton("🔹 بطاقة 10", url="https://shrinkme.click/Gems-2026-X12")],
        [InlineKeyboardButton("🔹 بطاقة 11", url="https://shrinkme.click/Gems-2026-X13"), InlineKeyboardButton("🔹 بطاقة 12", url="https://shrinkme.click/Gems-2026-X14")],
        [InlineKeyboardButton("🔹 بطاقة 13", url="https://shrinkme.click/Gems-2026-X15"), InlineKeyboardButton("🔹 بطاقة 14", url="https://shrinkme.click/Gems-2026-X16")],
        [InlineKeyboardButton("🔹 بطاقة 15", url="https://shrinkme.click/Gems-2026-X17"), InlineKeyboardButton("🔹 بطاقة 16", url="https://shrinkme.click/Gems-2026-X18")],
        [InlineKeyboardButton("🔹 بطاقة 17", url="https://shrinkme.click/Gems-2026-X19"), InlineKeyboardButton("🔹 بطاقة 18", url="https://shrinkme.click/Gems-2026-X20")],
        [InlineKeyboardButton("🔹 بطاقة 19", url="https://shrinkme.click/Gems-2026-X21"), InlineKeyboardButton("🔹 بطاقة 20", url="https://shrinkme.click/Gems-2026-X22")],
        [InlineKeyboardButton("👑 مـكـافـأة الـ 5000 جـوهـرة 🔥", url="https://shrinkme.click/Gems-2026-X22")]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # قراءة اسم الشخص الذي أرسل الصورة
    current_user_name = update.effective_user.first_name
    await update.message.reply_text(f"📸 تم استلام لقطة الشاشة يا {current_user_name}.. جاري التحليل الآلي...\n\n✅ الصور مطابقة! أرسل الآن كلمة (تم) لبدء ربط الآيدي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    # الحصول على اسم المستخدم الديناميكي
    current_user_name = update.effective_user.first_name

    if text == "تم":
        await update.message.reply_text(f"❇️ أهلاً يا {current_user_name}.. تم التأكد من تحميل الملفات.\n\nالآن، قم بكتابة الـ **ID** الخاص بك بدقة ليتم توجيه الجواهر إليه:")
    
    elif text.isdigit() and len(text) > 5:
        # نظام التحميل الوهمي (للمصداقية)
        status_msg = await update.message.reply_text("⏳ جاري البحث عن الحساب في قاعدة البيانات...")
        await asyncio.sleep(1.2)
        await status_msg.edit_text("📡 تم الاتصال بالسيرفر.. جاري مطابقة الـ ID...")
        await asyncio.sleep(1.2)
        await status_msg.edit_text(f"✅ تم العثور على الحساب بنجاح!\nالمستوى: مؤهل للشحن السريع 🚀")
        
        bot_info = await context.bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        
        await update.message.reply_text(
            f"📥 الـتـوثـيـق الـبـشـري مـطـلـوب:\n\n"
            f"نظام الشحن يتطلب منك دعوة **10 أشخاص** فقط عبر رابطك الخاص لضمان استقرار السيرفر وتجنب حظر الحساب.\n\n"
            f"🔗 رابط التفعيل الخاص بك:\n {ref_link}\n\n"
            f"أرسل الرابط لأصدقائك، ثم أرسل هنا كلمة (**تم الشحن**)."
        )
    
    elif text == "تم الشحن":
        await update.message.reply_text(
            f"💎 تـم وضـع طـلـبـك فـي قـائـمـة الانـتـظـار يا {current_user_name} 💎\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "نظراً لضغط الطلبات الحالي (أكثر من 45,000 مستخدم)، سيتم تحويل الجواهر إلى حسابك خلال 24-48 ساعة كحد أقصى.\n\n"
            "❌ ملاحظة: لا تقم بحذف البوت أو حظره قبل استلام الجواهر سيلغي الطلب فوراً."
        )

def main():
    # تشغيل نظام عدم النوم
    keep_alive()
    
    # تشغيل البوت
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن وميزة Keep-Alive مفعلة!")
    application.run_polling()

if __name__ == "__main__":
    main()
    
