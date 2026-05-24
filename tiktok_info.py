import time
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

def get_tiktok_info(username):
    # تنظيف اسم المستخدم
    username = username.replace("@", "").strip()
    url = f"https://www.tiktok.com/@{username}"
    
    # إعدادات المتصفح الخاصة بالسيرفرات (مهمة جداً لـ Streamlit Cloud)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # تشغيل مخفي تماماً بدون شاشة
    chrome_options.add_argument("--no-sandbox") # تجاوز حماية الـ Sandbox في لينكس
    chrome_options.add_argument("--disable-dev-shm-usage") # لتفادي امتلاء ذاكرة السيرفر المؤقتة
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    print(f"🔄 جاري تهيئة متصفح السيرفر وفحص حساب @{username}...")
    
    # تشغيل المتصفح بناءً على المسار المتوفر في سيرفر لينكس
    try:
        # محاولة التشغيل عبر النظام الافتراضي للسيرفر أولاً
        driver = webdriver.Chrome(options=chrome_options)
    except:
        # حل احتياطي في حال تطلب مسار الخدمة المباشر
        try:
            from selenium.webdriver.chrome.service import Service
            service = Service(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"❌ فشل تشغيل المتصفح على السيرفر: {e}")
            return

    try:
        driver.get(url)
        time.sleep(7) # زيادة وقت الانتظار للسيرفر لضمان تحميل الصفحة كاملاً
        
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
        
        # طباعة البيانات في شاشة الكمبيوتر / السيرفر
        print("\n" + "="*40)
        print(f"📊 معلومات الحساب لـ @{username}:")
        print("="*40)
        print(f"👥 يتابع: {following}")
        print(f"📢 المتابعون: {followers}")
        print(f"❤️ إجمالي الإعجابات: {likes}")
        print(f"🎬 عدد الفيديوهات الظاهرة في الصفحة: {video_count}")
        print(f"🖼️ رابط الصورة الشخصية: {img_url}")
        print("="*40)
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء قراءة البيانات: {e}")
        print("💡 تلميح: قد يكون الحساب خاصاً أو واجه الموقع كابتشا الحماية.")
        
    finally:
        driver.quit()

# تشغيل السكربت
if __name__ == "__main__":
    account_to_check = input("أدخل اسم حساب التيك توك (بدون @): ")
    get_tiktok_info(account_to_check)