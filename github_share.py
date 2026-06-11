import os
import streamlit as st
from github import Github

# إعدادات واجهة المستخدم
st.set_page_config(page_title="مستخرج ومشارك الأغاني", page_icon="🎵", layout="centered")

st.title("🎵 مستخرج ومشارك الأغاني")
st.write("قم برفع ملف صوتي من جهازك للحصول على رابط مباشر ومشاركته مع أصدقائك للاستماع أو التحميل!")

# --- التحقق من التوكن السري ---
try:
    ACCESS_TOKEN = st.secrets["github_token"]
except Exception:
    st.error("❌ خطأ: لم يتم العثور على رمز الوصول (github_token) في إعدادات Secrets الخاصة بـ Streamlit.")
    st.stop()

# --- إعدادات المستودع ---
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"  # اختياري: يمكنك وضع اسم حسابك، أو سيقوم الكود بجلبه تلقائياً
REPO_NAME = "tiktok-scraper"               # اسم المستودع المستهدف على جيتهاب
COMMIT_MESSAGE = "Upload new audio file via Streamlit"

st.markdown("---")

# 2. صندوق رفع الملف من الجهاز
uploaded_file = st.file_saver = st.file_uploader("اختر ملف الأغنية من جهازك (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # عرض مشغل صوتي للمعاينة قبل الرفع
    st.write("🎵 معاينة الملف قبل الرفع:")
    st.audio(uploaded_file)
    
    file_name = uploaded_file.name
    
    # زر تشغيل عملية الرفع والعمل الخلفي
    if st.button("🚀 ارفع الأغنية الآن وجهز رابط المشاركة"):
        with st.spinner("⏳ جاري رفع الأغنية إلى حسابك على GitHub وتوليد الروابط..."):
            try:
                # الاتصال بـ GitHub
                g = Github(ACCESS_TOKEN.strip())
                
                # جلب اسم المستخدم تلقائياً إن لم يكن محدداً
                if GITHUB_USERNAME == "YOUR_GITHUB_USERNAME" or GITHUB_USERNAME.strip() == "":
                    user_login = g.get_user().login
                else:
                    user_login = GITHUB_USERNAME
                
                repo = g.get_repo(f"{user_login}/{REPO_NAME}")
                
                # قراءة محتوى الملف المرفوع بصيغة البايتات
                file_content = uploaded_file.getvalue()
                
                # رفع الملف أو تحديثه إذا كان بنفس الاسم
                try:
                    contents = repo.get_contents(file_name)
                    repo.update_file(contents.path, COMMIT_MESSAGE, file_content, contents.sha)
                    st.info("🔄 تم تحديث الأغنية بنسخة جديدة في المستودع.")
                except Exception:
                    repo.create_file(file_name, COMMIT_MESSAGE, file_content)
                    st.info("🆕 تم إضافة الأغنية كملف جديد في المستودع.")
                
                # روابط المشاركة والتحميل
                share_url = f"https://github.com/{user_login}/{REPO_NAME}/blob/main/{file_name}"
                raw_download_url = f"https://raw.githubusercontent.com/{user_login}/{REPO_NAME}/main/{file_name}"
                
                st.success("🎉 تم الرفع بنجاح وأصبحت الأغنية جاهزة للمشاركة!")
                
                # --- واجهة الشخص الآخر (صندوق روابط المشاركة) ---
                st.markdown("### 🔗 أرسل هذه الروابط للشخص الآخر:")
                
                st.write("🔹 **رابط الاستماع والتحميل المباشر** (ينصح به - يفتح مشغل صوتي مباشر في متصفح الشخص الآخر ويحتوي على زر تحميل 📥):")
                st.code(raw_download_url)
                
                st.write("🔹 **رابط صفحة الملف على GitHub** (لمعاينة الملف داخل موقع جيتهاب نفسه):")
                st.code(share_url)
                
            except Exception as e:
                st.error(f"🛑 حدث خطأ أثناء عملية الرفع: {e}")
                st.info("تأكد من صحة إعدادات التوكن (Secrets) وأن المستودع عام (Public) ولديك صلاحيات الكتابة فيه.")