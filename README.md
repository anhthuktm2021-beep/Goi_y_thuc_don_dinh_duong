# Dự án Gợi ý Thực đơn Dinh dưỡng Cá nhân hóa

## Giới thiệu
Dự án sử dụng Python để phân tích dữ liệu dinh dưỡng và đưa ra thực đơn phù hợp dựa trên chỉ số cơ thể.

## 🚀 Tiến độ dự án (Project Status)

- [x] **Giai đoạn 1: Thu thập & Làm sạch dữ liệu (Data Processing)**
  - Xử lý bộ dữ liệu thô, chuẩn hóa tên cột (English sync) và làm sạch các giá trị lỗi, định dạng kiểu dữ liệu bằng thư viện `pandas`.

- [x] **Giai đoạn 2: Xây dựng Bộ máy Tính toán (Health Metrics Calculator)**
  - Ứng dụng công thức Mifflin-St Jeor tính toán chính xác chỉ số BMR và TDEE.
  - Xây dựng logic phân bổ nhóm chất Macros (Đạm 30% - Tinh bột 40% - Béo 30%).
  - **Tính năng mở rộng:** Tự động điều chỉnh lượng Calo mục tiêu dựa trên nhu cầu người dùng (Giảm mỡ thâm hụt, Giữ cân, Tăng cơ thặng dư).

- [x] **Giai đoạn 3: Thuật toán Gợi ý Thực đơn (Recommendation Engine)**
  - Xây dựng **Data Pipeline** cơ bản: Kết nối luồng dữ liệu tự động giữa các module thông qua file `.json` và Google Drive API.
  - Triển khai thuật toán tìm kiếm và chọn lọc món ăn ngẫu nhiên có điều kiện (Randomized Heuristic).
  - Tự động phân bổ thực đơn cho 3 bữa (Sáng 25% - Trưa 40% - Chiều 35%) đảm bảo sai số Calo và Macros luôn dưới mức 15%.

- [ ] **Giai đoạn 4: Đóng gói & Trực quan hóa (Finalization & Visualization)**
  - (Đang tiến hành...)
## Công nghệ sử dụng
- Ngôn ngữ: Python
- Thư viện: Pandas, Numpy
- Công cụ: Google Colab
