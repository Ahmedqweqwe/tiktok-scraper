import time
import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import requests

# واجهة مستخدم Streamlit
st.set_page_config(page_title="مستخرج بيانات تيك توك", page_icon="📊", layout="centered")
st.title("📊 مستخرج بيانات حسابات تيك توك")
st.write("أدخل اسم المستخدم بالأسفل لجلب معلومات الحساب وصورته الشخصية.")

def get_tiktok_info(username):
    username = username.replace("@", "")
    url = f"https://www.tiktok.com/@{username}"
    
    # إعدادات المتصفح للسيرفر (مهمة جداً لمنع الأخطاء أونلاين)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    with st.spinner(f"🔄 جاري فحص حساب @{username}... قد يستغرق ذلك بضع ثوانٍ"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        try:
            driver.get(url)
            time.sleep(5) 
            
            # استخراج الأرقام
            following = driver.find_element(By.XPATH, '//strong[@data-e2e="following-count"]').text
            followers = driver.find_element(By.XPATH, '//strong[@data-e2e="followers-count"]').text
            likes = driver.find_element(By.XPATH, '//strong[@data-e2e="likes-count"]').text
            
            # استخراج عدد الفيديوهات
            videos = driver.find_elements(By.XPATH, '//div[@data-e2e="user-post-item"]')
            video_count = len(videos)
            
            # استخراج رابط صورة الحساب
            img_element = driver.find_element(By.XPATH, '//img[contains(@class, "Avatar")]')
            img_url = img_element.get_attribute("src")
            
            # عرض البيانات على الموقع بشكل منظم
            st.success("✅ تم جلب البيانات بنجاح!")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if img_url:
                    st.image(img_url, caption=f"@{username}", width=150)
            with col2:
                st.write(f"**👥 يتابع:** {following}")
                st.write(f"**📢 المتابعون:** {followers}")
                st.write(f"**❤️ إجمالي الإعجابات:** {likes}")
                st.write(f"**🎬 الفيديوهات الظاهرة:** {video_count}")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء جلب البيانات. تأكد من صحة اسم الحساب أو حاول مجدداً لاحقاً.")
            st.info("ملاحظة: تيك توك قد يفرض حماية أحياناً تمنع السيرفرات من قراءة البيانات.")
            
        finally:
            driver.quit()

# استقبال المدخلات عبر واجهة الموقع
account_to_check = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("جلب معلومات الحساب"):
    if account_to_check:
        get_tiktok_info(account_to_check)
    else:
        st.warning("رجاءً أدخل اسم حساب أولاً!")
