import streamlit as st
import requests
import re
import json
from datetime import datetime

# إعدادات الواجهة
st.set_page_config(
    page_title="مستخرِج بيانات تيك توك الذكي",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 مستخرج معلومات حسابات TikTok الشامل")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب تفاصيل الحساب، موقع الدولة، تاريخ الإنشاء، والإيميل.")
st.markdown("---")

# قاموس الدول الموسع لتغطية كافة الاحتمالات
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

# دالة فك تشفير تاريخ الإنشاء
def extract_creation_date(user_id):
    try:
        id_int = int(user_id)
        timestamp = id_int >> 32
        creation_date = datetime.fromtimestamp(timestamp)
        return creation_date.strftime('%Y-%m-%d %I:%M %p')
    except:
        return "غير قادر على حساب التاريخ"

# دالة قنص الإيميل من البايو
def extract_email_from_bio(bio_text):
    if not bio_text:
        return None
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, bio_text)
    return emails[0] if emails else None

# 🌍 دالة ذكية جديدة ومحسنة لتحديد الدولة الحقيقية للحساب
def detect_real_region(html_content, json_region):
    # 1. البحث عن لغة المحتوى المحددة في الـ HTML (مثلاً ar-SA أو en-US)
    lang_match = re.search(r'lang="([a-zA-Z]{2})-([a-zA-Z]{2})"', html_content)
    if lang_match:
        detected_reg = lang_match.group(2).upper()
        if detected_reg in COUNTRY_MAP:
            return COUNTRY_MAP[detected_reg]
            
    # 2. فحص كود المنطقة الداخلي لو كان صحيحاً
    if json_region and json_region.upper() in COUNTRY_MAP:
        return COUNTRY_MAP[json_region.upper()]
        
    # 3. فحص نصوص العملات أو اللغات المدمجة في الصفحة كمؤشر بديل
    if "currency\":\"SAR\"" in html_content or "المملكة العربية السعودية" in html_content:
        return COUNTRY_MAP["SA"]
    elif "currency\":\"EGP\"" in html_content or "مصر" in html_content:
        return COUNTRY_MAP["EG"]
    elif "currency\":\"AED\"" in html_content:
        return COUNTRY_MAP["AE"]
        
    return f"المنطقة الافتراضية للتطبيق أو دولة أخرى ({json_region if json_region else 'العالمية'})"

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip().lower()
        url = f"https://www.tiktok.com/@{username}"
        
        with st.spinner("🔄 جاري قراءة البيانات وتدقيق المنطقة الجغرافية بدقة..."):
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
                            st.success("✅ تم جلب وتدقيق البيانات بنجاح!")
                            st.markdown("---")
                            
                            stats = user_info.get("stats", {})
                            user_meta = user_info.get("user", {})
                            
                            # 🛠️ تشغيل الدالة الذكية الجديدة لتحديد الدولة لتفادي الأخطاء
                            raw_region = user_meta.get("region", "")
                            country_name = detect_real_region(html_content, raw_region)
                            
                            # استخراج باقي البيانات
                            user_id = user_meta.get("id", "")
                            creation_date = extract_creation_date(user_id) if user_id else "غير متوفر"
                            
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
                                st.success(f"📍 **الدولة والمنطقة المستهدفة للحساب:** {country_name}")
                                st.markdown(f"📝 **الوصف:** {bio if bio else 'لا يوجد بايو'}")
                                
                                if detected_email:
                                    st.info(f"📧 **البريد الإلكتروني المكتشف لتواصل العمل:** `{detected_email}`")
                                else:
                                    st.warning("📧 **البريد الإلكتروني:** لم يتم العثور على إيميل علني في الوصف.")
                                    
                                st.warning(f"📅 **تاريخ إنشاء الحساب (تقريبي):** {creation_date}")
                                st.markdown(f"🔗 الرابط: [اضغط لزيارة الحساب](https://www.tiktok.com/@{username})")
                                
                                # عرض الأرقام بشكل كروت مرئية ممتازة
                                c1, c2, c3, c4 = st.columns(4)
                                c1.metric("المتابعون", f"{followers:,}")
                                c2.metric("يتابع", f"{following:,}")
                                c3.metric("الإعجابات", f"{hearts:,}")
                                c4.metric("الفيديوهات", f"{video_count:,}")
                        else:
                            st.error("❌ فشل تحليل بيانات الحساب المعروضة.")
                    else:
                        st.error("❌ تيك توك فرض نظام حماية مؤقت. يرجى إعادة المحاولة بعد قليل.")
                else:
                    st.error(f"⚠️ تيك توك رفض الاستجابة (كود: {response.status_code})")
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة البيانات: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")