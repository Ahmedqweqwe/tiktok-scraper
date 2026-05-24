import streamlit as st
import requests
import re
import json
from datetime import datetime

# 🧊 هنا تم وضع الإعدادات التي أرسلتها أنت لتجعل شكل الموقع عريضاً واحترافياً
st.set_page_config(
    page_title="مستخرِج بيانات تيك توك الذكي",
    page_icon="🧊",
    layout="wide", # جعل الصفحة عريضة واحترافية
    initial_sidebar_state="expanded"
)

st.title("📊 مستخرج معلومات حسابات TikTok الشامل")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب تفاصيل الحساب، موقع الدولة، تاريخ الإنشاء، والإيميل.")
st.markdown("---")

# قاموس لتحويل أكواد الدول العالمية
COUNTRY_MAP = {
    "SA": "المملكة العربية السعودية 🇸🇦",
    "EG": "جمهورية مصر العربية 🇪🇬",
    "AE": "الإمارات العربية المتحدة 🇦🇪",
    "KW": "الكويت 🇰🇼",
    "QA": "قطر 🇶🇦",
    "BH": "البحرين 🇧🇭",
    "OM": "سلطنة عمان 🇴🇲",
    "MA": "المغرب 🇲🇦",
    "DZ": "الجزائر 🇩🇿",
    "TN": "تونس 🇹🇳",
    "JO": "الأردن 🇯🇴",
    "LB": "لبنان 🇱🇧",
    "IQ": "العراق 🇮🇶",
    "US": "الولايات المتحدة الأمريكية 🇺🇸",
    "GB": "المملكة المتحدة (بريطانيا) 🇬🇧",
    "FR": "فرنسا 🇫🇷",
    "TR": "تركيا 🇹🇷"
}

# دالة فك تشفير الـ ID واستخراج تاريخ الإنشاء
def extract_creation_date(user_id):
    try:
        id_int = int(user_id)
        timestamp = id_int >> 32
        creation_date = datetime.fromtimestamp(timestamp)
        return creation_date.strftime('%Y-%m-%d %I:%M %p')
    except:
        return "غير قادر على حساب التاريخ"

# 📧 هذه هي الدالة الحقيقية والمسؤولة برمجياً عن قنص الإيميل من الحساب
def extract_email_from_bio(bio_text):
    if not bio_text:
        return None
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, bio_text)
    return emails[0] if emails else None

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip().lower()
        url = f"https://www.tiktok.com/@{username}"
        
        with st.spinner("🔄 جاري قراءة البيانات وتحديد الدولة وتاريخ الإنشاء..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    html_content = response.text
                    
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
                            st.success("✅ تم جلب البيانات وتحديد المنطقة بنجاح!")
                            st.markdown("---")
                            
                            stats = user_info.get("stats", {})
                            user_meta = user_info.get("user", {})
                            
                            # استخراج الدولة 
                            region_code = user_meta.get("region", "US")
                            country_name = COUNTRY_MAP.get(region_code, f"دولة أجنبية ({region_code})")
                            
                            # استخراج الـ ID وتاريخ الإنشاء
                            user_id = user_meta.get("id", "")
                            creation_date = extract_creation_date(user_id) if user_id else "غير متوفر"
                            
                            # استخراج الإيميل والبايو
                            bio = user_meta.get("signature", "")
                            detected_email = extract_email_from_bio(bio)
                            
                            followers = stats.get("followerCount", 0)
                            following = stats.get("followingCount", 0)
                            hearts = stats.get("heartCount", 0)
                            video_count = stats.get("videoCount", 0)
                            
                            nickname = user_meta.get("nickname", username)
                            avatar = user_meta.get("avatarLarger", "https://www.tiktok.com/favicon.ico")

                            # عرض البيانات للزوار بشكل عريض ومقسم
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                st.image(avatar, caption=f"صورة {nickname}", width=180)
                                
                            with col2:
                                st.markdown(f"### 👤 الإسم: **{nickname}**")
                                st.success(f"📍 **منطقة الحساب والدولة:** {country_name}")
                                st.markdown(f"📝 **الوصف:** {bio if bio else 'لا يوجد بايو'}")
                                
                                # 📧 هنا يظهر الإيميل للمستخدم كصندوق مستقل ونظيف
                                if detected_email:
                                    st.info(f"📧 **البريد الإلكتروني المكتشف للتواصل:** `{detected_email}`")
                                else:
                                    st.warning("📧 **البريد الإلكتروني:** لم يتم العثور على إيميل علني في الوصف.")
                                    
                                st.warning(f"📅 **تاريخ إنشاء الحساب:** {creation_date}")
                                st.markdown(f"🔗 الرابط: [اضغط لزيارة الحساب](https://www.tiktok.com/@{username})")
                                
                                # عرض الأرقام بشكل منسق
                                c1, c2, c3, c4 = st.columns(4)
                                c1.metric("المتابعون", f"{followers:,}")
                                c2.metric("يتابع", f"{following:,}")
                                c3.metric("الإعجابات", f"{hearts:,}")
                                c4.metric("الفيديوهات", f"{video_count:,}")
                        else:
                            st.error("❌ فشل تحليل بيانات الحساب.")
                    else:
                        st.error("❌ تيك توك يطلب اختبار أمان حالياً. يرجى المحاولة لاحقاً.")
                else:
                    st.error(f"⚠️ تيك توك رفض الاستجابة (كود: {response.status_code})")
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة البيانات: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")