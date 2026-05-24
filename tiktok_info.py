import streamlit as st
import requests
import re
import time
import random

# إعدادات الواجهة
st.set_page_config(
    page_title="مراقب لايف تيك توك المحمي",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 مستخرج ومراقب روابط TikTok Live (نسخة محمية)")
st.markdown("أدخل اسم الحساب بالأسفل، وسيقوم السيرفر بمراقبته بأمان عالي وجلب رابط البث فوراً.")
st.markdown("---")

# قائمة هويات متصفحات مختلفة (لعمل تدوير وحماية من الحظر)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
]

username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

# تفعيل وضع المراقبة المستمرة المحمية
check_live = st.checkbox("🔄 تفعيل المراقبة التلقائية المستمرة (نظام الحماية الذكي)")

if st.button("🔍 فحص حالة البث الآن", use_container_width=True) or check_live:
    if username:
        username = username.replace("@", "").strip().lower()
        live_url = f"https://www.tiktok.com/@{username}/live"
        
        status_box = st.empty()
        result_box = st.empty()
        
        # عدد محاولات الفحص في الدورة الواحدة
        loop_count = 6 if check_live else 1
        
        for i in range(loop_count):
            # 🛡️ الحماية 1: اختيار هوية متصفح عشوائية تماماً في كل محاولة فحص
            current_ua = random.choice(USER_AGENTS)
            
            headers = {
                "User-Agent": current_ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }
            
            status_box.info(f"🔄 جاري الفحص الآمن... (محاولة {i+1} من {loop_count})")
            
            try:
                # استخدام Session مستقل لضمان تنظيف الكوكيز وعدم كشف السيرفر
                with requests.Session() as session:
                    response = session.get(live_url, headers=headers, allow_redirects=True, timeout=12)
                    final_url = response.url
                    html_content = response.text
                
                # خوارزمية صيد البث النشط
                is_live_active = "room_id" in final_url or '"liveStatus\\":2' in html_content or '"liveStatus":2' in html_content or "LIVE" in html_content
                
                if is_live_active:
                    status_box.success("🎯 [حساب نشط] تم لقط البث المباشر بنجاح آمن!")
                    
                    with result_box.container():
                        st.markdown("### 🚨 الحساب يبث مباشر حالياً!")
                        st.code(final_url, language="text")
                        
                        st.markdown(
                            f'<a href="{final_url}" target="_blank" style="text-decoration:none;">'
                            f'<div style="text-align:center; padding:10px; background-color:#ff0050; color:white; border-radius:5px; font-weight:bold;">'
                            f'🚀 اضغط هنا لفتح البث مباشرة'
                            f'</div></a>', 
                            unsafe_allow_html=True
                        )
                    break  # التوقف فوراً عند النجاح لحماية السيرفر من العمل بلا داعٍ
                    
                else:
                    status_box.warning("💤 الحساب مغلق حالياً أو لا يبث. نظام الحماية يعمل بكفاءة.")
                    
            except Exception as e:
                status_box.error(f"⚠️ تنبيه حماية: واجه السيرفر صعوبة في الاتصال، سيتم التغيير تلقائياً. ({e})")
                
            # 🛡️ الحماية 2: وقت انتظار عشوائي تماماً بين المحاولات لكسر النمط الآلي
            if check_live and i < loop_count - 1:
                random_wait = random.randint(18, 35) # وقت عشوائي بين 18 إلى 35 ثانية
                status_box.markdown(f"⏳ تأمين السيرفر... إعادة الفحص خلال **{random_wait}** ثانية...")
                time.sleep(random_wait)
                
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>نظام مراقبة البث المحمي والمشفر © 2026</div>", unsafe_allow_html=True)