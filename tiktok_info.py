import streamlit as st
import requests
import re

# إعدادات الصفحة
st.set_page_config(page_title="مستخرج بيانات تيك توك الرسمي", page_icon="📊", layout="centered")

st.title("📊 مستخرج معلومات حسابات TikTok")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب معلومات الحساب وصورته الشخصية فوراً بدون حظر.")
st.markdown("---")

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip().lower()
        
        with st.spinner("🔄 جاري تخطي أنظمة الحماية وجلب البيانات الآمنة..."):
            try:
                # طريقة متطورة: استخدام منصة قراءة بيانات مفتوحة ومحمية من الحظر
                api_url = f"https://tokcount.com/api/user/info/{username}"
                
                # استخدام نظام Headers متطور جداً لتقليد متصفح حقيقي بالكامل
                headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "ar-XM,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Origin": "https://tokcount.com",
                    "Referer": "https://tokcount.com/"
                }
                
                response = requests.get(api_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # التحقق من وجود بيانات الحساب داخل استجابة السيرفر الجديد
                    if data and "error" not in data and ("followers" in data or "data" in data):
                        st.success("✅ تم جلب البيانات بنجاح تام!")
                        st.markdown("---")
                        
                        # قراءة البيانات حسب هيكلة السيرفر الجديد الذكي
                        user_data = data.get("data", data)
                        
                        followers = user_data.get("followers", user_data.get("followerCount", 0))
                        following = user_data.get("following", user_data.get("followingCount", 0))
                        hearts = user_data.get("likes", user_data.get("heartCount", 0))
                        video_count = user_data.get("videos", user_data.get("videoCount", 0))
                        nickname = user_data.get("nickname", user_data.get("username", username))
                        avatar = user_data.get("avatar", "https://www.tiktok.com/favicon.ico")

                        # عرض البيانات للزوار
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
                        st.error("❌ الحساب غير موجود أو قد يكون خاصاً ومحمياً من قِبل صاحبه.")
                
                # حل احتياطي فوري إذا رجع السيرفر بـ 403 أو فشل
                else:
                    # نستخدم رابط بديل مجاني وسريع جداً مخصص للإحصائيات الحية
                    fallback_url = f"https://api.ttcounts.com/user/info/{username}"
                    fallback_resp = requests.get(fallback_url, headers=headers, timeout=10)
                    
                    if fallback_resp.status_code == 200:
                        fb_data = fallback_resp.json()
                        if fb_data and "user" in fb_data:
                            st.success("✅ تم جلب البيانات عبر الخادم الاحتياطي!")
                            u = fb_data["user"]
                            st.info(f"📢 **عدد المتابعين:** {u.get('followers', 0):,}")
                            st.info(f"❤️ **إجمالي الإعجابات:** {u.get('likes', 0):,}")
                            st.info(f"🎬 **عدد الفيديوهات:** {u.get('videos', 0):,}")
                        else:
                            st.error("❌ عذراً، الحساب لم يستجب. يرجى التأكد من الاسم.")
                    else:
                        st.error(f"⚠️ واجه الموقع نظام حماية تيك توك الصارم (كود الحظر: {response.status_code}). جرب كتابة اسم حساب آخر.")
                        
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة البيانات الفنية: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>مركز فحص الحسابات الذكي © 2026</div>", unsafe_allow_html=True)