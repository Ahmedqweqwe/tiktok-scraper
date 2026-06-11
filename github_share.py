import os
from github import Github

# 1. إعداد البيانات الأساسية
ACCESS_TOKEN = "ضع_هنا_توكن_الحساب"
REPO_NAME = "اسم_المستودع"      # مثال: my-songs-repo
FILE_PATH = "song.mp3"         # مسار الملف في جهازك
COMMIT_MESSAGE = "Upload song via Python"

# 2. الاتصال بحساب GitHub
g = Github(ACCESS_TOKEN)
user = g.get_user()

# 3. جلب المستودع أو إنشاؤه إذا لم يكن موجوداً
try:
    repo = user.get_repo(REPO_NAME)
except Exception:
    repo = user.create_repo(REPO_NAME, private=False) # True إذا كنت تريده خاصاً

# 4. قراءة محتوى الملف ورفعه
with open(FILE_PATH, "rb") as file:
    content = file.read()

file_name = os.path.basename(FILE_PATH)

try:
    # رفع الملف
    repo.create_file(file_name, COMMIT_MESSAGE, content)
    
    # 5. توليد رابط المشاركة المباشر
    share_url = f"https://github.com{user.login}/{REPO_NAME}/blob/main/{file_name}"
    print(f"تم الرفع بنجاح! رابط المشاركة هو:\n{share_url}")

except Exception as e:
    print(f"حدث خطأ أثناء الرفع: {e}")
