import os
import base64
from github import Github

# 1. إعداد البيانات الأساسية
ACCESS_TOKEN = "ضع_هنا_توكن_الحساب"
REPO_NAME = "اسم_المستودع"      
FILE_PATH = "song.mp3"         # تأكد من وجود ملف الأغنية بنفس المجلد أو اكتب مساره الصحيح
COMMIT_MESSAGE = "Upload song via Python Streamlit"

# 2. الاتصال بحساب GitHub
g = Github(ACCESS_TOKEN)
user = g.get_user()

# 3. جلب المستودع أو إنشاؤه
try:
    repo = user.get_repo(REPO_NAME)
except Exception:
    repo = user.create_repo(REPO_NAME, private=False)

# 4. قراءة محتوى الملف وتحويله إلى Base64 لتفادي أخطاء الترميز (UnicodeEncodeError)
with open(FILE_PATH, "rb") as file:
    content = file.read()

file_name = os.path.basename(FILE_PATH)

try:
    # رفع الملف مباشرة باستخدام PyGithub التي ستتعامل مع التشفير بشكل صحيح
    repo.create_file(file_name, COMMIT_MESSAGE, content)
    
    # 5. توليد رابط المشاركة المباشر
    share_url = f"https://github.com{user.login}/{REPO_NAME}/blob/main/{file_name}"
    print(f"تم الرفع بنجاح! رابط المشاركة هو:\n{share_url}")

except Exception as e:
    print(f"حدث خطأ أثناء الرفع: {e}")
