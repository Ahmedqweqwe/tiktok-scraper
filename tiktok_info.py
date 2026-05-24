import streamlit as st
import requests
import re
import json

# إعدادات الصفحة
st.set_page_config(page_title="مستخرج بيانات تيك توك الرسمي", page_icon="📊", layout="centered")

st.title("📊 مستخرج معلومات حسابات TikTok")
st.markdown("أدخل اسم المستخدم بالأسفل لجلب معلومات الحساب وصورته الشخصية فوراً.")
st.markdown("---")

# خانة إدخال اسم المستخدم
username = st.text_input("أدخل اسم حساب التيك توك (بدون @):", placeholder="مثال: khaby.lame")

if st.button("🔍 جلب البيانات الآن", use_container_width=True):
    if username:
        username = username.replace("@", "").strip().lower()
        url = f"https://www.tiktok.com/@{username}"
        
        with st.spinner("🔄 جاري قراءة بيانات الحساب مباشرة من تيك توك..."):
            try:
                # استخدام هيدرز قوي جداً يحاكي متصفح حقيقي متطور
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    html_content = response.text
                    
                    # البحث عن بيانات الحساب المدمجة داخل الصفحة عبر الـ Regex
                    data_pattern = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html_content)
                    
                    # محاولة نمط قديم احتياطي لو تيك توك غير الهيكل
                    if not data_pattern:
                        data_pattern = re.search(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', html_content)
                        
                    if data_pattern:
                        json_data = json.loads(data_pattern.group(1))
                        
                        # الدخول لعمق ملف البيانات لاستخراج الأرقام بدقة
                        try:
                            # الهيكلة الحديثة لبيانات تيك توك
                            default_scope = json_data.get("__DEFAULT_SCOPE__", {})
                            user_detail = default_scope.get("webapp.user-detail", {})
                            user_info = user_detail.get("userInfo", {})
                        except:
                            user_info = json_data.get("UserModule", {}).get("users", {}).get(username, {})
                            
                        if user_info:
                            st.success("✅ تم جلب البيانات بنجاح مباشر!")
                            st.markdown("---")
                            
                            # استخراج تفاصيل الحساب والأرقام
                            stats = user_info.get("stats", {})
                            user_meta = user_info.get("user", {})
                            
                            followers = stats.get("followerCount", 0)
                            following = stats.get("followingCount", 0)
                            hearts = stats.get("heartCount", 0)
                            video_count = stats.get("videoCount", 0)
                            
                            nickname = user_meta.get("nickname", username)
                            avatar = user_meta.get("avatarLarger", "https://www.tiktok.com/favicon.ico")
                            bio = user_meta.get("signature", "لا يوجد بايو")

                            # عرض البيانات للزوار بشكل احترافي
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.image(avatar, caption=f"صورة {nickname}", width=150)
                                
                            with col2:
                                st.markdown(f"### 👤 الإسم: **{nickname}**")
                                st.markdown(f"📝 **الوصف:** {bio}")
                                st.markdown(f"🔗 الرابط: [اضغط لزيارة الحساب](https://www.tiktok.com/@{username})")
                                
                                st.info(f"📢 **عدد المتابعين:** {followers:,}")
                                st.info(f"👥 **يتابع:** {following:,}")
                                st.info(f"❤️ **إجمالي الإعجابات:** {hearts:,}")
                                st.info(f"🎬 **عدد الفيديوهات المنشورة:** {video_count:,}")
                        else:
                            st.error("❌ فشل تحليل بيانات الحساب الداعمة. جرب لاحقاً.")
                    else:
                        # حل بديل ذكي جداً وسريع جداً لو فشل الـ JSON (استخراج الأرقام بالنص الصريح)
                        try:
                            followers_match = re.search(r'"followerCount":(\d+)', html_content)
                            hearts_match = re.search(r'"heartCount":(\d+)', html_content)
                            video_match = re.search(r'"videoCount":(\d+)', html_content)
                            
                            if followers_match:
                                st.success("✅ تم جلب البيانات عبر الفحص السريع!")
                                st.info(f"📢 **عدد المتابعين التقديري:** {int(followers_match.group(1)):,}")
                                if hearts_match:
                                    st.info(f"❤️ **إجمالي الإعجابات:** {int(hearts_match.group(1)):,}")
                                if video_match:
                                    st.info(f"🎬 **عدد الفيديوهات:** {int(video_match.group(1)):,}")
                            else:
                                st.error("❌ عذراً، تيك توك يطلب اختبار أمان (Captcha) حالياً لهذا الحساب. جرب بعد دقائق.")
                        except:
                            st.error("❌ الحساب غير موجود أو تم حظره.")
                else:
                    st.error(f"⚠️ تيك توك رفض الاستجابة للسيرفر حالياً (كود: {response.status_code}). جرب مجدداً.")
                        
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالشبكة: {e}")
    else:
        st.warning("⚠️ يرجى كتابة اسم المستخدم أولاً!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>مركز فحص الحسابات الذكي © 2026</div>", unsafe_allow_html=True)