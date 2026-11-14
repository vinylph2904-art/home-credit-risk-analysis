# MySQL

Để chạy bản nộp trên máy khác, khôi phục bản database có dữ liệu theo
[hướng dẫn](../data/database/README.md). Các file SQL trong thư mục này
phục vụ xem thiết kế hoặc xây dựng từ đầu; DDL không chứa dữ liệu nghiên cứu.

| File | Nội dung |
|---|---|
| `00_raw_schema.sql` | Tám bảng nguồn và tiến độ nạp dữ liệu |
| `01_create_schema.sql` | Đặc trưng, phân tập và metadata |
| `02_read_queries.sql` | Truy vấn đối soát và đọc dữ liệu |
| `03_web_schema.sql` | Hồ sơ quản lý, model, lịch sử chấm và ghi chú |
| `04_dashboard_indexes.sql` | Index tra cứu lịch sử dashboard |
| `05_users.sql` | Tài khoản, phân quyền và phân công |

`Connector` đọc host/port/database/user từ `configs/mysql_connection.json`,
ưu tiên biến môi trường `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`.
Mật khẩu lấy từ tham số, `MYSQL_PASSWORD` hoặc `configs/mysql_connection.local.json`.

## Luồng dữ liệu

Nguồn ban đầu → MySQL `raw_*` → notebook 01–03 hiểu dữ liệu/chất lượng/EDA
→ notebook 04 chuẩn bị đặc trưng → `application_features`
→ notebook 05–08 chọn biến, huấn luyện, đánh giá và diễn giải.

Giữ tên cột, kiểu dữ liệu, NULL, giá trị và thứ tự nguồn.
`_source_row` là thứ tự nguồn, không phải đặc trưng hay khóa nghiệp vụ.
Không tự xóa các kỳ trả nợ lặp trước khi đối chiếu cấp kỳ.
Workbench không nhập trực tiếp file Parquet bằng cách đổi đuôi sang CSV.

`application_split` lưu ID, role và fold; `application_features` chứa bộ B 199 biến.
Bộ A lấy 127 cột; Filter dùng 182 biến ở model cuối.
TARGET được SELECT từ `raw_application_train`, không nằm trong bảng đặc trưng.
Ba CV fold chỉ thuộc train; giữ phân tập đã lưu, không chia lại khi mở dashboard.

Các lớp `HomeCreditData`, `HomeCreditQuality`, `HomeCreditPreparation` và
`HomeCreditModelData` đọc MySQL qua Connector. Notebook 02 tạo các bảng EDA
trong `data/eda/`; notebook 04 tạo đặc trưng và đầu vào cho bước mô hình.
Cache `data/raw_mysql/` giữ kết quả đọc/đối soát trước đây; không thay thế
việc SELECT MySQL trong luồng nghiên cứu hiện hành.

Ứng dụng dùng `model_versions`, `demo_profiles`, `scoring_events`,
`review_notes`, `users` và `user_audit`. Bản dump đã có bảng, index và dữ liệu demo;
không chạy lại các lệnh tạo bảng hoặc reset dữ liệu sau khi nhập dump.
