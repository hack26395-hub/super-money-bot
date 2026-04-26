import os
import uuid
import time
import telebot
import google.generativeai as genai
from pdf2docx import Converter
from docx import Document
from docx.shared import RGBColor
import traceback

# ========== التوكنات (التزم بها كما هي) ==========
TELEGRAM_TOKEN = "8433118363:AAH0iqeZVo3xz-KP_KQ7LxHSdhRZnOmb2LQ"
GEMINI_API_KEY = "AIzaSyCChd6IL-8hi9ttKOIwH-vVF57MzK8X26s"

# ========== إعداد البوت وذكاء قيس ==========
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# تعليمات النظام (البرومبت) ليكون سريع ومترجم عبقري
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="أنت 'ذكاء قيس'. وظيفتك الترجمة الاحترافية بلمسة علمية. ردودك سريعة ودقيقة."
)

def gemini_translate(text):
    """استخدام الجيمني للترجمة بدلاً من المكتبات البطيئة"""
    if not text.strip(): return ""
    try:
        # نطلب منه الترجمة فقط لسرعة الرد
        response = model.generate_content(f"Translate this to Arabic ONLY: {text}")
        return response.text.strip()
    except:
        return " (فشلت الترجمة) "

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "🚀 أهلاً بك! أنا ذكاء قيس المطور.\n"
        "أرسل لي أي ملف (PDF/DOCX) وسأترجمه لك بسرعة البرق مع الحفاظ على الصور.\n"
        "أنا الآن أستخدم محرك Gemini 1.5 Flash السريع!"
    )
    bot.reply_to(message, welcome)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    start_time = time.time() # بدأنا حساب الوقت هنا
    file_name = message.document.file_name
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext not in ['.pdf', '.docx']:
        bot.reply_to(message, "❌ أرسل ملف PDF أو DOCX فقط يا بطل.")
        return

    progress = bot.reply_to(message, "⏳ ذكاء قيس بدأ العمل... يرجى الانتظار.")
    
    unique_id = uuid.uuid4().hex
    input_path = f"in_{unique_id}{ext}"
    docx_path = f"conv_{unique_id}.docx"
    output_path = f"Qais_AI_{file_name}"

    try:
        # تحميل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open(input_path, 'wb') as f:
            f.write(downloaded)

        # 1. تحويل الـ PDF إذا لزم الأمر
        if ext == '.pdf':
            cv = Converter(input_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            target_file = docx_path
        else:
            target_file = input_path

        # 2. الترجمة الاحترافية السريعة
        doc = Document(target_file)
        for para in doc.paragraphs:
            if len(para.text.strip()) > 2:
                translated = gemini_translate(para.text)
                run = para.add_run(f"\n{translated}")
                run.font.color.rgb = RGBColor(31, 73, 125)
                run.font.italic = True
                run.font.bold = True

        doc.save(output_path)
        
        # حساب الوقت المستغرق
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        # إرسال الملف مع المؤقت
        with open(output_path, 'rb') as f:
            bot.send_document(
                message.chat.id, f, 
                caption=f"✅ تمت الترجمة بنجاح!\n⏱ الوقت المستغرق: {duration} ثانية.\n👤 المطور: قيس"
            )

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")
    
    finally:
        # تنظيف الملفات
        for f in [input_path, docx_path, output_path]:
            if os.path.exists(f): os.remove(f)
        bot.delete_message(message.chat.id, progress.message_id)

@bot.message_handler(func=lambda m: True)
def chat(message):
    """الرد على الأسئلة العلمية"""
    try:
        res = model.generate_content(message.text)
        bot.reply_to(message, res.text)
    except:
        bot.reply_to(message, "أنا ذكاء قيس، اسألني أي شيء علمي!")

bot.polling(none_stop=True)
            
