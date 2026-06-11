import os
import streamlit as st
from github import Github

st.title("مستخرج ومشارك الأغاني")

# 1. جلب التوكن من إعدادات سريمتليت الآمنة
# تأكد أنك قمت بكتابة التوكن في الـ Secrets باسم github_token
try:
    ACCESS_TOKEN = st.secrets["github_token"]
except Exception:
    st.error("خطأ: لم يتم العثور على رمز الوصول (Token) في إعدادات Secrets.")
    st.stop()

REPO_NAME = "tiktok-scraper"       # اسم المستودع الخاص بك
FILE_PATH = "song.mp3"             # اسم ملف الأغنية الناتجة
COMMIT_MESSAGE = "Upload audio file via Streamlit"

# زر لتشغيل عملية الرفع
if st.button("رفع الأغنية ومشاركتها"):
    
    if not os.path.exists(FILE_PATH):
        st.error(f"الملف {FILE_PATH} غير موجود حالياً، تأكد من توليده أولاً.")
    else:
        with st.spinner("جاري الرفع إلى GitHub..."):
            try:
                # تنظيف التوكن من أي مسافات زائدة
                g = Github(ACCESS_TOKEN.strip())
                user = g.get_user()
                repo = user.get_repo(REPO_NAME)
                
                # قراءة الملف بصيغة بايتس ثنائية
                with open(FILE_PATH, "rb") as file:
                    content = file.read()
                
                # رفع الملف أو تحديثه إذا كان موجوداً مسبقاً
                try:
                    contents = repo.get_contents(FILE_PATH)
                    repo.update_file(contents.path, COMMIT_MESSAGE, content, contents.sha)
                except Exception:
                    repo.create_file(FILE_PATH, COMMIT_MESSAGE, content)
                
                # رابط المشاركة المباشر للأغنية
                share_url = f"https://github.com{user.login}/{REPO_NAME}/blob/main/{FILE_PATH}"
                
                st.success("تم الرفع بنجاح!")
                st.write(f"رابط مشاركة الأغنية:")
                st.code(share_url)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الرفع: {e}")
