# Dashboard Flask

Từ thư mục dự án, chạy `py -3.14 web/app.py`, rồi mở `http://127.0.0.1:5000`.
Đổi cổng bằng `--port 5001`. Cấu hình MySQL và khôi phục dữ liệu theo
[README chính](../README.md) và [hướng dẫn database](../data/database/README.md).

## Chức năng

- Tổng quan tài chính và phân tích danh mục trên tập train nghiên cứu.
- Tra cứu lịch sử tín dụng và kỳ thanh toán theo quyền truy cập.
- Chấm điểm hồ sơ, diễn giải đóng góp, mô phỏng thay đổi đầu vào.
- Quản lý phân công, trạng thái rà soát, ghi chú và lịch sử chấm điểm.
- Đăng nhập và phân quyền quản trị, trưởng bộ phận rủi ro, chuyên viên tín dụng.

Hồ sơ quản lý được chọn từ `application_test` đã có đặc trưng;
chưa có luồng tiếp nhận hồ sơ gốc hoàn toàn mới.
Ghi chú rà soát không phải nhãn kết quả thanh toán để đánh giá lại model.

## Tổ chức

`app.py` khởi tạo ứng dụng; các file `*_routes.py` xử lý nhóm URL.
`runtime.py` tải model và cấp kết nối theo request. Các module dữ liệu,
thống kê và biểu đồ chuẩn bị nội dung cho template. HTML nằm trong `templates/`,
CSS/JavaScript trong `static/`, font trong `assets/`.

Model dùng `artifacts/inference_metadata.json`: CatBoost 182 biến, raw score,
ngưỡng 14,5394%. Trang Mô hình đọc kết quả validation của cùng phiên bản.
SHAP giải thích raw margin, không diễn giải thành quan hệ nhân quả.
Tham khảo [artifact](../artifacts/README.md).

## Khởi tạo từ database nghiên cứu

Chỉ dùng khi chưa có các bảng ứng dụng; không cần cho database dump đã bàn giao:

```powershell
py -3.14 web/app.py --init-db --seed-demo 200
py -3.14 web/app.py --init-users
```

Đọc `users.py` để đặt biến môi trường mật khẩu tài khoản trước khi khởi tạo.
`scripts/activate_selected_model.py` đăng ký model hiện hành và bổ sung điểm
còn thiếu cho hồ sơ đã quản lý, giữ lại lịch sử.
Ứng dụng không tự cập nhật model khi chạy notebook.

Khởi động lại Flask sau khi sửa Python. Static asset có version theo nội dung;
cache truy vấn được lưu trong `tmp/dashboard_research_cache/`.
