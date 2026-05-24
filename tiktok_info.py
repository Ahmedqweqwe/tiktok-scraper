import streamlit as st
import requests
import re
import time

# إعدادات الواجهة
st.set_page_config(
    page_title="مراقب لايف تيك توك التلقائي",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 مستخرج ومراقب روابط TikTok Live")
st.markdown("أدخل اسم الحساب بالأسفل، وسيقوم السيرفر بمراقبته وجلب رابط البث المباشر فوراً.")
st.markdown("---")

username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

# تفعيل وضع المراقبة المستمرة
check_live = st.checkbox("🔄 تفعيل المراقبة التلقائية المستمرة")

if st.button("🔍 فحص حالة البث الآن", use_container_width=True) or check_live:
    if username:
        username = username.replace("@", "").strip().lower()
        live_url = f"https://www.tiktok.com/@{username}/live"
        
        # هيدرز لمحاكاة متصفح حقيقي من السيرفر
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        }
        
        status_box = st.empty()
        result_box = st.empty()
        
        # حلقة تكرارية لو اختار المستخدم مراقبة مستمرة
        loop_count = 5 if check_live else 1
        
        for i in range(loop_count):
            status_box.info(f"🔄 جاري فحص الحساب الآن... (محاولة {i+1} من {loop_count})")
            
            try:
                # طلب الصفحة لمعرفة هل يوجد بث نشط
                response = requests.get(live_url, headers=headers, allow_redirects=True, timeout=10)
                final_url = response.url
                html_content = response.text
                
                # تيك توك يقوم بتحويل الرابط أو وضع وسم "ROOM_ID" أو "isLive":true عندما يكون البث نشطاً
                is_live_active = "room_id" in final_url or '"liveStatus":2' in html_content or "LIVE" in html_content
                
                if is_live_active:
                    status_box.success("🎯 [حساب نشط] تم اكتشاف البث المباشر الآن!")
                    
                    with result_box.container():
                        st.markdown("### 🚨 الحساب يبث مباشر حالياً!") # تم تصحيح السطر هنا
                        st.code(final_url, language="text")
                        
                        # زر نسخ ذكي يعمل داخل المتصفح للزائر مباشرة
                        st.markdown(
                            f'<a href="{final_url}" target="_blank" style="text-decoration:none;">'
                            f'<div style="text-align:center; padding:10px; background-color:#ff0050; color:white; border-radius:5px; font-weight:bold;">'
                            f'🚀 اضغط هنا لفتح البث مباشرة'
                            f'</div></a>', 
                            unsafe_allow_html=True
                        )
                    break # إيقاف الفحص بمجرد العثور على اللايف
                    
                else:
                    status_box.warning("💤 الحساب مغلق حالياً ولا يوجد أي بث مباشر مفتوح.")
                    
            except Exception as e:
                status_box.error(f"حدث خطأ أثناء الاتصال بالشبكة: {e}")
                
            if check_live and i < loop_count - 1:
                time.sleep(15) # الانتظار 15 ثانية قبل إعادة الفحص تلقائياً
                
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>نظام مراقبة البث الآمن المباشر © 2026</div>", unsafe_allow_html=True)