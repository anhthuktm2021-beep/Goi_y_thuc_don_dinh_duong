import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
# Cài đặt giao diện trang web
st.set_page_config(page_title="Diet Recommender", layout="wide")
st.title("🥗 Ứng dụng Gợi ý Thực đơn Cá nhân hóa")

# 1. ĐỌC DỮ LIỆU
@st.cache_data # Lệnh này giúp web load dữ liệu 1 lần thôi cho nhanh
def load_data():
    # Thay link này bằng link raw GitHub file CSV của bạng
    url = 'https://raw.githubusercontent.com/anhthuktm2021-beep/Goi_y_thuc_don_dinh_duong/refs/heads/main/cleaned_nutrition.csv'
    return pd.read_csv(url)

df = load_data()

# 2. KHU VỰC NHẬP LIỆU (Bên thanh Sidebar)
st.sidebar.header("Thông số của bạng")
gender = st.sidebar.selectbox("Giới tính", ["Nam", "Nữ"])
weight = st.sidebar.number_input("Cân nặng (kg)", min_value=30.0, max_value=200.0, value=50.0)
height = st.sidebar.number_input("Chiều cao (cm)", min_value=100.0, max_value=250.0, value=160.0)
age = st.sidebar.number_input("Tuổi", min_value=10, max_value=100, value=20)

active_level = st.sidebar.selectbox("Mức độ vận động", 
    ["1. Ít vận động", "2. Vận động nhẹ", "3. Vận động vừa", "4. Vận động nặng"])
muc_tieu = st.sidebar.selectbox("Mục tiêu hình thể", 
    ["1. Giảm cân (-500 kcal)", "2. Giữ cân", "3. Tăng cân (+500 kcal)"])

# 3. NÚT BẤM CHẠY THUẬT TOÁN
if st.sidebar.button("Tính toán & Lên thực đơn"):
    # TÍNH TDEE
    s = 5 if gender == "Nam" else -161
    bmr = 10 * weight + 6.25 * height - 5 * age + s
    
    r_dict = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725}
    r = r_dict[active_level[0]] 
    tdee_goc = bmr * r
    
    if muc_tieu.startswith("1"):
        tdee_target = tdee_goc - 500
    elif muc_tieu.startswith("3"):
        tdee_target = tdee_goc + 500
    else:
        tdee_target = tdee_goc

    # TÍNH MACROS
    p_target = (tdee_target * 0.3) / 4
    c_target = (tdee_target * 0.4) / 4
    f_target = (tdee_target * 0.3) / 9

    # HIỂN THỊ KẾT QUẢ TÍNH TOÁN
    st.subheader(f"🔥 Mục tiêu Calo của bạng: {tdee_target:.0f} kcal/ngày")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Tỷ lệ Đạm - Đường - Béo")
        # Vẽ biểu đồ tròn
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([p_target*4, c_target*4, f_target*9], labels=['Protein', 'Carbs', 'Fat'], 
               autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'])
        st.pyplot(fig)

    with col2:
        st.write("### 🍽️ Thực đơn gợi ý cho bạn: ")
        
        # Chia mục tiêu cho từng bữa
        sang_t = tdee_target * 0.25
        trua_t = tdee_target * 0.40
        chieu_t = tdee_target * 0.35

        # Hàm bốc món nhanh cho Web (Bốc 2 món mỗi bữa)
        def bốc_món(target_cal):
            ket_qua = pd.DataFrame()
            tong_calo = 0
            so_lan_thu = 0 # Biến đếm để tránh vòng lặp chạy vô hạn
            
            # Cố gắng nhặt món cho đến khi tổng calo đạt ít nhất 90% mục tiêu
            while tong_calo < target_cal * 0.9 and so_lan_thu < 50:
                so_lan_thu += 1
                
                # Bốc ngẫu nhiên 1 món từ menu
                mon_ngau_nhien = df.sample(1)
                calo_mon = mon_ngau_nhien['Calories'].values[0]
                
                # Kiểm tra: Nếu nạp món này vào mà tổng calo KHÔNG bị lố quá 110% mục tiêu thì mới lấy
                if tong_calo + calo_mon <= target_cal * 1.1:
                    ket_qua = pd.concat([ket_qua, mon_ngau_nhien])
                    tong_calo += calo_mon
                    
            # Trường hợp xui xẻo (rất hiếm) vòng lặp kết thúc mà khay vẫn trống
            if ket_qua.empty:
                ket_qua = df.sample(1)
                tong_calo = ket_qua['Calories'].values[0]
                
            return ket_qua, tong_calo

        m_sang, c_sang = bốc_món(sang_t)
        m_trua, c_trua = bốc_món(trua_t)
        m_chieu, c_chieu = bốc_món(chieu_t)

        # Hiển thị từng bữa
        st.info(f"🌅 **Bữa Sáng (~{sang_t:.0f} kcal):**")
        for _, row in m_sang.iterrows():
            st.write(f"- {row['Food_Name']} ({row['Grams']}g): {row['Calories']} kcal")
        
        st.success(f"☀️ **Bữa Trưa (~{trua_t:.0f} kcal):**")
        for _, row in m_trua.iterrows():
            st.write(f"- {row['Food_Name']} ({row['Grams']}g): {row['Calories']} kcal")

        st.warning(f"🌙 **Bữa Chiều (~{chieu_t:.0f} kcal):**")
        for _, row in m_chieu.iterrows():
            st.write(f"- {row['Food_Name']} ({row['Grams']}g): {row['Calories']} kcal")

        st.divider()
        st.metric("Tổng năng lượng thực tế", f"{c_sang + c_sang + c_chieu:.0f} kcal", f"{tdee_target:.0f} mục tiêu")
        