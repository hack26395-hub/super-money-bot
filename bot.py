import os
import time
import telebot
import google.generativeai as genai
from docx import Document
from docx.shared import RGBColor, Pt
from pdf2docx import Converter

# --- بيانات الوصول الخاصة بك ---
TELEGRAM_TOKEN = "8433118363:AAH0iqeZVo3xz-KP_KQ7LxHSdhRZnOmb2LQ"
GEMINI_API_KEY = "AIzaSyCChd6IL-8hi9ttKOIwH-vVF57MzK8X26s"

# إعداد محرك الذكاء الاصطناعي (نسخة المطور قيس)
genai.configure(api_key=GEMINI_API_KEY)

# تعليمات النظام لتعريف البوت كخبير علمي وشخصية تابعة لقيس
SYSTEM_PROMPT = (
    "أنت 'ذكاء قيس' (Qais AI)، نظام متطور جداً تم تطويرك بواسطة المبرمج قيس. "
    "تمتلك خبرة هائلة في العلوم (الفيزياء، الكيمياء، الأحياء، الرياضيات، والتقنية). "
    "عندما يطرح عليك المستخدم سؤالاً علمياً، أجب بدقة ومنطق، واستخدم الأمثلة إذا لزم الأمر. "
    "دائماً اذكر بفخر أنك من تطوير قيس إذا سئلت عن هويتك. "
    "تتحدث العربية بأسلوب راقٍ ومفهوم."
)

ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def perform_smart_translation(text_content):
    if not text_content or len(text_content.strip()) < 2:
        return None
    try:
        prompt = f"Translate to professional Arabic (keep original meaning). Output only translation:\n\n{text_content}"
        response = ai_model.generate_content(prompt)
        return response.text.strip() if response.text else None
    except:
        return None

# --- معالجة الرسائل النصية (الدردشة والأسئلة العلمية) ---
@bot.message_handler(func=lambda message: True, content_types=['text'])
def qais_ai_chat(message):
    if message.text.startswith('/'): return 
    
    # رسالة انتظار بسيطة للأسئلة العلمية الطويلة
    wait_msg = bot.reply_to(message, "💡 Please wait, Qais AI is thinking...")
    
    try:
        # إرسال السؤال للذكاء الاصطناعي
        response = ai_model.generate_content(message.text)
        
        # مسح رسالة الانتظار وإرسال الإجابة العلمية
        bot.delete_message(message.chat.id, wait_msg.message_id)
        bot.reply_to(message, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.edit_message_text(f"❌ عفواً، واجهت مشكلة: {str(e)}", message.chat.id, wait_msg.message_id)

# --- معالجة الملفات (PDF و DOCX) ---
@bot.message_handler(content_types=['document'])
def handle_incoming_files(message):
    file_name = message.document.file_name
    progress_msg = bot.reply_to(message, "⏳ Please wait... Qais AI is processing your file.")
    
    timestamp = int(time.time())
    original_file = f"orig_{timestamp}_{file_name}"
    docx_file = f"temp_{timestamp}.docx"
    final_output = f"Translated_By_Qais_{file_name.split('.')[0]}.docx"

    try:
        # تحميل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open(original_file, 'wb') as f:
            f.write(downloaded)

        # تحويل PDF إلى DOCX تلقائياً
        if file_name.lower().endswith('.pdf'):
            cv = Converter(original_file)
            cv.convert(docx_file, start=0, end=None)
            cv.close()
            target_docx = docx_file
        else:
            target_docx = original_file

        # معالجة المستند وترجمته
        doc = Document(target_docx)
        for para in doc.paragraphs:
            if len(para.text.strip()) > 3:
                translated = perform_smart_translation(para.text)
                if translated:
                    run = para.add_run(f"\n{translated}")
                    run.font.color.rgb = RGBColor(0, 51, 153) # أزرق غامق فخم
                    run.font.bold = True
                    run.font.size = Pt(11)

        doc.save(final_output)

        with open(final_output, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Done! Processed by Qais AI.")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")
    
    finally:
        # تنظيف السيرفر
        for f in [original_file, docx_file, final_output]:
            if os.path.exists(f): os.remove(f)
        try: bot.delete_message(message.chat.id, progress_msg.message_id)
        except: pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أنا 'ذكاء قيس' الاصطناعي.\n\n"
                         "أنا خبير في العلوم ومحترف في ترجمة الملفات.\n"
                         "يمكنك سؤالي أي سؤال علمي، أو إرسال ملف (PDF/DOCX) لترجمته.")

print("Qais AI Multi-Function Bot is Ready!")
bot.polling(none_stop=True)
    
