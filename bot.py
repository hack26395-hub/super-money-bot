import os
import time
import uuid
import telebot
from pdf2docx import Converter
from docx import Document
from docx.shared import RGBColor, Pt
from googletrans import Translator

# --- الإعدادات ---
TOKEN = "8433118363:AAH0iqeZVo3xz-KP_KQ7LxHSdhRZnOmb2LQ"
bot = telebot.TeleBot(TOKEN)
google_translator = Translator()

def safe_translate(text):
    """ترجمة آمنة وسريعة عبر محرك جوجل"""
    if not text.strip() or len(text.strip()) < 2:
        return ""
    try:
        res = google_translator.translate(text, src='en', dest='ar')
        return res.text
    except:
        # محاولة ثانية في حال حدوث خطأ في الشبكة
        try:
            time.sleep(0.5)
            res = google_translator.translate(text, src='en', dest='ar')
            return res.text
        except:
            return ""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل ملف PDF أو DOCX للترجمة.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    start_time = time.time()
    file_name = message.document.file_name
    ext = os.path.splitext(file_name)[1].lower()

    if ext not in ['.pdf', '.docx']:
        return

    status = bot.reply_to(message, "Please wait...")
    
    uid = uuid.uuid4().hex
    in_file = f"in_{uid}{ext}"
    tmp_docx = f"tmp_{uid}.docx"
    out_file = f"Translated_{file_name}"

    try:
        # 1. تحميل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open(in_file, 'wb') as f:
            f.write(downloaded)

        # 2. التحويل (إذا كان PDF) مع الحفاظ على الكائنات والصور
        if ext == '.pdf':
            cv = Converter(in_file)
            cv.convert(tmp_docx, start=0, end=None)
            cv.close()
            target = tmp_docx
        else:
            target = in_file

        # 3. معالجة سطر بسطر (ترجمة تحت السطر مباشرة)
        doc = Document(target)
        for para in doc.paragraphs:
            original_text = para.text.strip()
            if len(original_text) > 2:
                translated = safe_translate(original_text)
                if translated:
                    # إضافة سطر جديد داخل نفس الفقرة ثم وضع الترجمة
                    run = para.add_run(f"\n{translated}")
                    run.font.color.rgb = RGBColor(31, 73, 125)
                    run.font.italic = True
                    run.font.size = Pt(10)

        # 4. حفظ وإرسال مع توقيت العملية
        doc.save(out_file)
        elapsed = round(time.time() - start_time, 2)

        with open(out_file, 'rb') as f:
            bot.send_document(
                message.chat.id, f, 
                caption=f"Done!\nTime: {elapsed}s"
            )

    except Exception:
        bot.reply_to(message, "Error.")
    
    finally:
        # تنظيف السيرفر
        for f in [in_file, tmp_docx, out_file]:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass
        try: bot.delete_message(message.chat.id, status.message_id)
        except: pass

# نظام الحماية من التوقف
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=25)
        except:
            time.sleep(5)
        
