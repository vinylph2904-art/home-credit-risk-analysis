# Schema và truy vấn MySQL

Để chạy ứng dụng trên máy khác, [khôi phục snapshot đầy đủ](../data/database/README.md).
Các file ở đây là DDL/truy vấn của mã nguồn, không chứa toàn bộ dữ liệu nghiên cứu
và không thay thế dump `data/database/database.sql.gz`.

| File | Nội dung |
|---|---|
| `00_raw_schema.sql` | Tám bảng nguồn `raw_*` và bảng theo dõi nạp dữ liệu |
| `01_create_schema.sql` | Phân tập, bộ đặc trưng B và metadata dữ liệu |
| `02_read_queries.sql` | Truy vấn đối soát/đọc dữ liệu |
| `03_web_schema.sql` | Hồ sơ quản lý, phiên bản model, sự kiện chấm và ghi chú |
| `04_dashboard_indexes.sql` | Index phục vụ tra cứu lịch sử trên dashboard |
| `05_users.sql` | Bảng tài khoản và nhật ký; mã `web/users.py` bổ sung liên kết phân công nếu thiếu |

## Kết nối

`connectors/Connector.py` đọc cấu hình theo thứ tự ưu tiên:

| Thuộc tính | Thứ tự |
|---|---|
| Host / port / database / user | Tham số constructor → `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DATABASE` / `MYSQL_USER` → `configs/mysql_connection.json` |
| Password | Tham số constructor → `MYSQL_PASSWORD` → trường `password` của `configs/mysql_connection.local.json` |

File local chỉ được dùng để lấy mật khẩu. Mặc định JSON là `localhost:3306`,
database `home_credit_ml`, user `root`. Nếu khôi phục vào `home_credit_submission`,
cần đặt `MYSQL_DATABASE` hoặc sửa cấu hình để trỏ đúng schema. File
`configs/mysql_connection.local.example.json` là mẫu; file local thật không được theo dõi trong Git.

## Luồng dữ liệu hiện có

```text
MySQL raw_* → notebook 01–03: hiểu dữ liệu / chất lượng / EDA
           → notebook 04: tổng hợp lịch sử, xuất Parquet A/B
           → notebook 05: chọn biến
           → notebook 06: nhập B vào application_features và kiểm tra split
                          đọc lại train từ MySQL để chạy CV
           → notebook 07: đánh giá / fit cuối / ngưỡng
           → notebook 08: diễn giải từ đầu ra đã lưu
```

`application_split` giữ ID, vai trò tập và fold. `application_features` chứa bộ B
199 đặc trưng; bộ A lấy 127 cột, còn schema CatBoost cuối lấy 182 cột.
`TARGET` được đọc từ `raw_application_train`, không thuộc bảng đặc trưng.
Ba CV fold chỉ nằm trong train; mở dashboard không chia lại dữ liệu.

Giữ NULL, kiểu dữ liệu, ID và thứ tự nguồn. `_source_row` là khóa vật lý theo
thứ tự nguồn, không phải đặc trưng dự báo. Nhiều dòng thanh toán của một kỳ
không mặc nhiên là bản ghi trùng cần xóa. Các bản `data/raw_mysql/` và
`data/model_input/mysql/` là đầu ra đối soát, không giả thay cho truy vấn mới.

DDL chỉ tạo cấu trúc; notebook 01 bắt đầu bằng đọc bảng nguồn đã có dữ liệu.
Các script hiện có trong `scripts/` giải nén/kiểm tra snapshot, không phải bộ
nạp tự động tám bảng Parquet từ đầu. Dump bàn giao đã có bảng, index và dữ liệu;
không cần chạy lại các bước khởi tạo schema để dùng bản đã khôi phục.
