import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import requests

def get_tiktok_info(username):
    # تنظيف اسم المستخدم لو تم إدخال @
    username = username.replace("@", "")
url = f"https://tiktok.com@{username}"
    
    # إعدادات المتصفح ليعمل بشكل مخفي واحترافي
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # يمكنك تفعيل هذا السطر لإخفاء المتصفح أثناء العمل
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    print(f"🔄 جاري فتح متصفح كروم وفحص حساب @{username}...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5) # الانتظار للتأكد من تحميل الصفحة بالكامل
        
        # 1. استخراج الأرقام (متابعة، متابعين، تسجيلات الإعجاب)
        following = driver.find_element(By.XPATH, '//strong[@data-e2e="following-count"]').text
        followers = driver.find_element(By.XPATH, '//strong[@data-e2e="followers-count"]').text
        likes = driver.find_element(By.XPATH, '//strong[@data-e2e="likes-count"]').text
        
        # 2. استخراج عدد الفيديوهات المنشورة
        videos = driver.find_elements(By.XPATH, '//div[@data-e2e="user-post-item"]')
        video_count = len(videos)
        
        # 3. استخراج رابط صورة الحساب الشخصية
        img_element = driver.find_element(By.XPATH, '//img[contains(@class, "Avatar")]')
        img_url = img_element.get_attribute("src")
        
        # طباعة البيانات في شاشة الكمبيوتر
        print("\n" + "="*40)
        print(f"📊 معلومات الحساب لـ @{username}:")
        print("="*40)
        print(f"👥 يتابع: {following}")
        print(f"📢 المتابعون: {followers}")
        print(f"❤️ إجمالي الإعجابات: {likes}")
        print(f"🎬 عدد الفيديوهات الظاهرة في الصفحة: {video_count}")
        print(f"🖼️ رابط الصورة الشخصية: {img_url}")
        print("="*40)
        
        # 4. تحميل الصورة الشخصية وحفظها على جهازك تلقائياً
        if img_url:
            img_data = requests.get(img_url).content
            img_name = f"{username}_profile.jpg"
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            print(f"✅ تم حفظ صورة الحساب في مجلد السكربت باسم: {img_name}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء جلب البيانات: {e}")
        print("💡 تلميح: قد يكون الحساب خاصاً (Private) أو تيك توك يطلب اختبار أمان كابتشا.")
        
    finally:
        driver.quit()

# تشغيل السكربت (ضع اسم أي حساب تريده هنا لتجربته)
if __name__ == "__main__":
    account_to_check = input("أدخل اسم حساب التيك توك (بدون @): ")
    get_tiktok_info(account_to_check)