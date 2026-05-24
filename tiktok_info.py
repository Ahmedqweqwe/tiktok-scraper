import streamlit as st
import requests
import json

# إعدادات الصفحة
st.set_page_config(page_title="مستخرج بيانات تيك توك", page_icon="📊", layout="centered")

st.title("📊 مستخرج معلومات حسابات TikTok")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب معلومات الحساب وصورته الشخصية فوراً.")
st.markdown("---")

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip()
        
        # استخدام نظام فحص سريع ومفتوح لجلب بيانات الحساب
        api_url = f"https://www.tiktok.com/api/user/detail/?uniqueId={username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        with st.spinner("🔄 جاري الاتصال بتيك توك وجلب البيانات..."):
            try:
                # محاولة جلب البيانات عبر طلب مباشر
                response = requests.get(api_url, headers=headers, timeout=10)
                
                # إذا تطلب الأمر وسيلة بديلة بسبب حماية تيك توك، نستخدم مكاناً بديلاً مفتوحاً
                if response.status_code != 200 or "userInfo" not in response.text:
                    # رابط بديل مجاني ومستقر لجلب نفس البيانات دون حظر
                    backup_url = f"https://countik.com/api/userinfo?username={username}"
                    response = requests.get(backup_url, headers=headers, timeout=10)
                    data = response.json()
                else:
                    res_json = response.json()
                    data = res_json.get("userInfo", {})

                # التحقق من نجاح جلب البيانات
                if data and ("followerCount" in str(data) or "stats" in data):
                    st.success("✅ تم جلب بيانات الحساب بنجاح!")
                    st.markdown("---")
                    
                    # ترتيب استخراج البيانات حسب نوع الـ API المستجيب
                    stats = data.get("stats", data)
                    user_info = data.get("user", data)
                    
                    # استخراج الأرقام
                    followers = stats.get("followerCount", stats.get("followers", 0))
                    following = stats.get("followingCount", stats.get("following", 0))
                    hearts = stats.get("heartCount", stats.get("hearts", stats.get("likes", 0)))
                    video_count = stats.get("videoCount", stats.get("videos", 0))
                    
                    # استخراج الصورة والاسم
                    nickname = user_info.get("nickname", username)
                    avatar = user_info.get("avatarLarger", user_info.get("avatar", "https://www.tiktok.com/favicon.ico"))

                    # عرض البيانات للمستخدم بشكل احترافي بجانب بعضها
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(avatar, caption=f"صورة {nickname}", width=150)
                        
                    with col2:
                        st.markdown(f"### 👤 الإسم: **{nickname}**")
                        st.markdown(f"🔗 الرابط: [اضغط لزيارة الحساب](https://www.tiktok.com/@{username})")
                        
                        st.info(f"📢 **عدد المتابعين:** {followers:,}")
                        st.info(f"👥 **يتابع:** {following:,}")
                        st.info(f"❤️ **إجمالي الإعجابات:** {hearts:,}")
                        st.info(f"🎬 **عدد الفيديوهات المنشورة:** {video_count:,}")
                        
                else:
                    st.error("❌ لم نتمكن من العثور على الحساب. تأكد من كتابة الاسم بشكل صحيح، أو قد يكون الحساب خاصاً.")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>مركز فحص الحسابات الذكي © 2026</div>", unsafe_allow_html=True)