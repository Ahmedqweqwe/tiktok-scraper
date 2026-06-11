import os
import streamlit as st
from github import Github

# --- إعداد تلقائي للملفات السرية محلياً (للتسهيل عليك) ---
# هذا الجزء سيوجهك لكتابة التوكن إذا نسيت إعداده
SECRETS_DIR = ".streamlit"
SECRETS_FILE = os.path.join(SECRETS_DIR, "secrets.toml")

if not os.path.exists(SECRETS_FILE):
    st.warning("⚠️ لم يتم العثور على ملف الإعدادات السرية (Secrets).")
    token_input = st.text_input("أدخل رمز الوصول (GitHub Token) الخاص بك هنا لإعداده تلقائياً:", type="password")
    if token_input:
        if not os.path.exists(SECRETS_DIR):
            os.makedirs(SECRETS_DIR)
        with open(SECRETS_FILE, "w", encoding="utf-8") as f:
            f.write(f'github_token = "{token_input.strip()}"\n')
        st.success("✅ تم حفظ التوكن بنجاح! يرجى إعادة تحديث الصفحة (Refresh) لتفعيل الإعدادات.")
        st.stop()
    else:
        st.info("قم بكتابة التوكن في المربع أعلاه، أو اتبّع الخطوات اليدوية لإنشاء ملف secrets.toml")
        st.stop()

# --- بداية التطبيق الأساسي ---
st.title("🎵 مستخرج ومشارك الأغاني")
st.subheader("رفع الملفات الصوتية مباشرة إلى GitHub")

# 1. جلب التوكن من إعدادات ستريمليت الآمنة
try:
    ACCESS_TOKEN = st.secrets["github_token"]
except Exception:
    st.error("خطأ: لم يتم العثور على رمز الوصول (Token) في إعدادات Secrets.")
    st.stop()

# --- إعدادات المستودع ---
# 💡 نصيحة: يمكنك تركها "YOUR_GITHUB_USERNAME" وسيقوم الكود بجلب اسم حسابك تلقائياً!
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"  
REPO_NAME = "tiktok-scraper"         # اسم المستودع الخاص بك على جيتهاب
FILE_PATH = "song.mp3"               # اسم ملف الأغنية المتواجد في مجلد المشروع
COMMIT_MESSAGE = "Upload audio file via Streamlit"

# واجهة المستخدم لرفع الملف
st.markdown("---")
st.write(f"الملف المستهدف للرفع: `{FILE_PATH}`")

# زر لتشغيل عملية الرفع
if st.button("🚀 رفع الأغنية ومشاركتها"):
    
    # التأكد من وجود ملف الـ MP3 أولاً في المجلد
    if not os.path.exists(FILE_PATH):
        st.error(f"❌ الخطأ: الملف `{FILE_PATH}` غير موجود حالياً في مجلد المشروع. تأكد من استخراجه أو توليده أولاً باسم صحيح.")
    else:
        with st.spinner("⏳ جاري الاتصال بـ GitHub ورفع الملف..."):
            try:
                # تنظيف التوكن والاتصال بـ GitHub
                g = Github(ACCESS_TOKEN.strip())
                
                # جلب اسم المستخدم ديناميكياً إذا لم يتم تعديله في الأعلى
                if GITHUB_USERNAME == "YOUR_GITHUB_USERNAME":
                    user_login = g.get_user().login
                else:
                    user_login = GITHUB_USERNAME
                
                # الوصول للمستودع
                repo = g.get_repo(f"{user_login}/{REPO_NAME}")
                
                # قراءة الملف بصيغة بايتس ثنائية (Binary)
                with open(FILE_PATH, "rb") as file:
                    content = file.read()
                
                # رفع الملف أو تحديثه إذا كان موجوداً مسبقاً
                try:
                    contents = repo.get_contents(FILE_PATH)
                    repo.update_file(contents.path, COMMIT_MESSAGE, content, contents.sha)
                    st.info("🔄 تم تحديث الملف الحالي بنسخة جديدة.")
                except Exception:
                    repo.create_file(FILE_PATH, COMMIT_MESSAGE, content)
                    st.info("🆕 تم إنشاء ملف جديد في المستودع.")
                
                # إنشاء روابط المشاركة
                share_url = f"https://github.com/{user_login}/{REPO_NAME}/blob/main/{FILE_PATH}"
                raw_url = f"https://raw.githubusercontent.com/{user_login}/{REPO_NAME}/main/{FILE_PATH}"
                
                st.success("🎉 تم الرفع بنجاح!")
                
                # عرض الروابط للمستخدم
                st.markdown("### 🔗 روابط الملف:")
                st.write("رابط المعاينة على GitHub:")
                st.code(share_url)
                
                st.write("رابط التحميل المباشر (يمكن تشغيله في المشغلات الصوتية):")
                st.code(raw_url)
                
                # تشغيل الصوت للتأكد داخل التطبيق
                st.audio(FILE_PATH)
                
            except Exception as e:
                st.error(f"🛑 حدث خطأ غير متوقع أثناء الرفع: {e}")
                st.info("تأكد من أن اسم المستودع (Repository) صحيح وأن التوكن يمتلك صلاحيات الـ Repo.")