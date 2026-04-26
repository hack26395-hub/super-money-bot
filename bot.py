import os
import time
import uuid
import telebot
import logging
from pdf2docx import Converter
from docx import Document
from docx.shared import RGBColor, Pt
from googletrans import Translator

# --- الإعدادات (ضع توكنك هنا) ---
TOKEN = "8433118363:AAH0iqeZVo3xz-KP_KQ7LxHSdhRZnOmb2LQ"
bot = telebot.TeleBot(TOKEN)
google_translator = Translator()

# إعداد السجلات لمراقبة الأخطاء في Render
logging.basicConfig(level=logging.INFO)

def safe_translate(text):
    """دالة ترجمة مستقرة تتجنب الانقطاع"""
    if not text.strip() or len(text.strip()) < 2:
        return ""
    try:
        res = google_translator.translate(text, src='en', dest='ar')
        return res.text
    except Exception as e:
        logging.error(f"Translation Error: {e}")
        return ""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل ملف PDF أو DOCX للترجمة الفورية.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    start_time = time.time()
    file_name = message.document.file_name
    ext = os.path.splitext(file_name)[1].lower()

    if ext not in ['.pdf', '.docx']:
        return

    status_msg = bot.reply_to(message, "⏳ جاري المعالجة...")
    
    # توليد أسماء فريدة لمنع التداخل في Render
    uid = uuid.uuid4().hex
    input_path = f"in_{uid}{ext}"
    output_docx = f"Translated_{file_name.split('.')[0]}.docx"

    try:
        # تحميل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open(input_path, 'wb') as f:
            f.write(downloaded)

        # إذا كان الملف PDF نحوله لـ Word أولاً للحفاظ على الصور والتنسيق
        if ext == '.pdf':
            docx_tmp = f"tmp_{uid}.docx"
            cv = Converter(input_path)
            cv.convert(docx_tmp, start=0, end=None)
            cv.close()
            working_file = docx_tmp
        else:
            working_file = input_path

        # فتح المستند والترجمة (سطر تحت سطر)
        doc = Document(working_file)
        for para in doc.paragraphs:
            original = para.text.strip()
            if len(original) > 2:
                translated = safe_translate(original)
                if translated:
                    # إضافة الترجمة بتنسيق احترافي تحت النص الأصلي
                    run = para.add_run(f"\n{translated}")
                    run.font.color.rgb = RGBColor(31, 73, 125) # أزرق
                    run.font.italic = True
                    run.font.size = Pt(10)

        doc.save(output_docx)
        elapsed = round(time.time() - start_time, 2)

        # إرسال الملف النهائي
        with open(output_docx, 'rb') as f:
            bot.send_document(
                message.chat.id, f, 
                caption=f"Done!\nTime: {elapsed}s"
            )

    except Exception as e:
        logging.error(f"General Error: {e}")
        bot.reply_to(message, "Error processing file.")
    
    finally:
        # تنظيف السيرفر فوراً لمنع امتلاء الذاكرة في Render
        for f in [input_path, output_docx, f"tmp_{uid}.docx" if ext == '.pdf' else ""]:
            if f and os.path.exists(f):
                try: os.remove(f)
                except: pass
        try: bot.delete_message(message.chat.id, status_msg.message_id)
        except: pass

# أهم جزء لـ Render: نظام الحماية من التوقف وإعادة التشغيل التلقائي
if __name__ == "__main__":
    while True:
        try:
            logging.info("Bot is starting...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logging.error(f"Bot crashed: {e}")
            time.sleep(5) # انتظر 5 ثواني ثم أعد التشغيل تلقائياً
    
