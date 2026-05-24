import streamlit as st
import requests

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
        
        with st.spinner("🔄 جاري الاتصال الآمن وتخطي الحماية وجلب البيانات..."):
            try:
                # استخدام API مفتوح ومستقر مخصص لجلب البيانات وتفادي حظر (line 1 column 1)
                api_url = f"https://countik.com/api/userinfo?username={username}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "application/json"
                }
                
                response = requests.get(api_url, headers=headers, timeout=15)
                
                # التحقق أولاً أن السيرفر رد باستجابة صحيحة وليس صفحة خطأ
                if response.status_code == 200:
                    data = response.json()
                    
                    # التحقق من أن الحساب موجود ويحتوي على بيانات
                    if data and "status" not in str(data) and "followers" in data:
                        st.success("✅ تم جلب بيانات الحساب بنجاح!")
                        st.markdown("---")
                        
                        # استخراج البيانات بدقة
                        followers = data.get("followers", 0)
                        following = data.get("following", 0)
                        hearts = data.get("likes", 0)
                        video_count = data.get("videos", 0)
                        nickname = data.get("nickname", username)
                        avatar = data.get("avatar", "https://www.tiktok.com/favicon.ico")

                        # عرض البيانات للمستخدم بشكل احترافي منسق
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
                        st.error("❌ لم نتمكن من العثور على هذا الحساب. تأكد من كتابة الاسم بشكل صحيح (قد يكون الحساب تم تغييره أو حذفه).")
                else:
                    st.error(f"⚠️ السيرفر مشغول حالياً، يرجى المحاولة مرة أخرى بعد ثوانٍ. (كود الخطأ: {response.status_code})")
                    
            except requests.exceptions.JSONDecodeError:
                st.error("❌ واجه السيرفر نظام حماية مؤقت من تيك توك. يرجى الانتظار دقيقة والمحاولة مجدداً.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>مركز فحص الحسابات الذكي © 2026</div>", unsafe_allow_html=True)