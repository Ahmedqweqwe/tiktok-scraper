import streamlit as st
import requests
import re
import json
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مستخرج بيانات تيك توك الرسمي", page_icon="📊", layout="centered")

st.title("📊 مستخرج معلومات حسابات TikTok الشامل")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب تفاصيل الحساب، صورته الشخصية، **وتاريخ إنشائه بدقة**.")
st.markdown("---")

# دالة رياضية لفك تشفير الـ ID واستخراج تاريخ الإنشاء منه (بصمة Snowflake الزمنية)
def extract_creation_date(user_id):
    try:
        # تحويل الـ ID إلى رقم صحيح
        id_int = int(user_id)
        # في نظام تيك توك، أول 32 بت من الرقم تمثل وقت الإنشاء بالثواني (Unix Timestamp)
        timestamp = id_int >> 32
        # تحويل الطابع الزمني إلى تاريخ ووقت مفهوم
        creation_date = datetime.fromtimestamp(timestamp)
        return creation_date.strftime('%Y-%m-%d %I:%M %p')
    except:
        return "غير قادر على حساب التاريخ"

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip().lower()
        url = f"https://www.tiktok.com/@{username}"
        
        with st.spinner("🔄 جاري قراءة بيانات الحساب وفك تشفير تاريخ الإنشاء..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    html_content = response.text
                    
                    # البحث عن البيانات المدمجة
                    data_pattern = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html_content)
                    if not data_pattern:
                        data_pattern = re.search(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', html_content)
                        
                    if data_pattern:
                        json_data = json.loads(data_pattern.group(1))
                        
                        try:
                            default_scope = json_data.get("__DEFAULT_SCOPE__", {})
                            user_detail = default_scope.get("webapp.user-detail", {})
                            user_info = user_detail.get("userInfo", {})
                        except:
                            user_info = json_data.get("UserModule", {}).get("users", {}).get(username, {})
                            
                        if user_info:
                            st.success("✅ تم جلب وتشفير البيانات بنجاح!")
                            st.markdown("---")
                            
                            stats = user_info.get("stats", {})
                            user_meta = user_info.get("user", {})
                            
                            # 1. استخراج الـ ID السري للحساب وحساب تاريخ الإنشاء
                            user_id = user_meta.get("id", "")
                            if user_id:
                                creation_date = extract_creation_date(user_id)
                            else:
                                creation_date = "غير متوفر"
                            
                            # 2. باقي البيانات الأخرة
                            followers = stats.get("followerCount", 0)
                            following = stats.get("followingCount", 0)
                            hearts = stats.get("heartCount", 0)
                            video_count = stats.get("videoCount", 0)
                            
                            nickname = user_meta.get("nickname", username)
                            avatar = user_meta.get("avatarLarger", "https://www.tiktok.com/favicon.ico")
                            bio = user_meta.get("signature", "لا يوجد بايو")

                            # عرض البيانات للزوار
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.image(avatar, caption=f"صورة {nickname}", width=150)
                                
                            with col2:
                                st.markdown(f"### 👤 الإسم: **{nickname}**")
                                st.markdown(f"📝 **الوصف:** {bio}")
                                
                                # عرض تاريخ الإنشاء بلون مميز لجذب الانتباه
                                st.warning(f"📅 **تاريخ إنشاء الحساب التقريبي:** {creation_date}")
                                
                                st.info(f"📢 **عدد المتابعين:** {followers:,}")
                                st.info(f"👥 **يتابع:** {following:,}")
                                st.info(f"❤️ **إجمالي الإعجابات:** {hearts:,}")
                                st.info(f"🎬 **عدد الفيديوهات المنشورة:** {video_count:,}")
                        else:
                            st.error("❌ فشل تحليل بيانات الحساب.")
                    else:
                        # حل احتياطي سريع للأرقام الأساسية لو فشل الـ JSON الكامل
                        followers_match = re.search(r'"followerCount":(\d+)', html_content)
                        id_match = re.search(r'"id":"(\d+)"', html_content) # محاولة صيد الـ ID من الصفحة مباشرة
                        
                        if followers_match:
                            st.success("✅ تم جلب البيانات عبر الفحص السريع!")
                            if id_match:
                                creation_date = extract_creation_date(id_match.group(1))
                                st.warning(f"📅 **تاريخ إنشاء الحساب التقريبي:** {creation_date}")
                            st.info(f"📢 **عدد المتابعين:** {int(followers_match.group(1)):,}")
                        else:
                            st.error("❌ تيك توك يطلب اختبار أمان حالياً. يرجى المحاولة لاحقاً.")
                else:
                    st.error(f"⚠️ تيك توك رفض الاستجابة (كود: {response.status_code})")
                        
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة البيانات: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>مركز فحص الحسابات الذكي بميزة الخوارزمية الزمنية © 2026</div>", unsafe_allow_html=True)