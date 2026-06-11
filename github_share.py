import os
import streamlit as st
import requests

st.title("مستخرج ومشارك الأغاني")
st.subheader("رفع الملفات الصوتية مباشرة ومشاركتها")

FILE_PATH = "song.mp3"  # اسم ملف الأغنية الناتجة في مشروعك

if st.button("رفع الأغنية ومشاركتها فوراً"):
    if not os.path.exists(FILE_PATH):
        st.error(f"الملف {FILE_PATH} غير موجود حالياً، تأكد من توليده أولاً.")
    else:
        with st.spinner("جاري الرفع وتوليد رابط المشاركة..."):
            try:
                # الرفع إلى خادم مجاني ومباشر (مثال: file.io تنتهي صلاحيته بعد التحميل أو فترة)
                with open(FILE_PATH, "rb") as f:
                    response = requests.post("https://file.io", files={"file": f})
                
                if response.status_code == 200:
                    share_url = response.json().get("link")
                    st.success("تم الرفع بنجاح!")
                    st.write("رابط مشاركة الأغنية المباشر:")
                    st.code(share_url)
                else:
                    st.error("فشل الرفع، يرجى المحاولة مرة أخرى.")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء الرفع: {e}")
