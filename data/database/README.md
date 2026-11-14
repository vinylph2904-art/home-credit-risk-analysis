# Khôi phục database

`database.sql.gz` là bản xuất MySQL ngày 02/11/2026, đã có cấu trúc, index,
dữ liệu nghiên cứu và tài khoản demo. `manifest.json` ghi checksum và số dòng
của snapshot; database đang sử dụng sau ngày đó có thể đã có thêm thao tác.
Nguồn dump dùng MySQL 8.0.32, khoảng 58 triệu dòng lịch sử.
Cần đủ dung lượng cho SQL giải nén (khoảng 3,7 GB) và database sau nhập.

## Các bước

1. Từ thư mục gốc dự án chạy `py -3.14 scripts/prepare_database.py`.
   Công cụ kiểm tra checksum và giải nén thành `data/database/database.sql`.
   Nếu file SQL đã có, công cụ chỉ tái dùng khi checksum khớp.
2. Trong MySQL Workbench, tạo schema mới `home_credit_submission`, charset utf8mb4.
3. Chọn Server → Data Import → Import from Self-Contained File,
   trỏ đến `data/database/database.sql`; chọn Default Target Schema vừa tạo.
4. Chọn Dump Structure and Data → Start Import. Chờ nhập hoàn tất.
5. Đặt `MYSQL_DATABASE=home_credit_submission` cùng host, port, user và
   `MYSQL_PASSWORD` của máy nhận.
6. Chạy `py -3.14 scripts/verify_database.py` để đối chiếu số dòng snapshot.
7. Chạy `py -3.14 web/app.py`, mở `http://127.0.0.1:5000`.

Dump đã có bảng và dữ liệu demo; không cần chạy `--init-db`, `--init-users`
hoặc chạy lại notebook trước khi mở web. Tài khoản demo ở `demo_accounts.json`.
`reset_demo_passwords.sql` chỉ dùng khi cần đặt lại mật khẩu demo trên database đã nhập.
