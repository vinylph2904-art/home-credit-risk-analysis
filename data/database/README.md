# Khôi phục database MySQL

`database.sql.gz` là snapshot ngày 02/11/2026 từ MySQL 8.0.32. Bản này đã có
cấu trúc, index, tám bảng nguồn, đặc trưng, phân tập, model và dữ liệu demo.
[manifest.json](manifest.json) lưu SHA-256, kích thước và số dòng đối chiếu.

| Tệp | Kích thước theo manifest |
|---|---|
| `database.sql.gz` | 1.500.643.844 byte, khoảng 1,50 GB |
| SQL sau giải nén | 3.694.742.776 byte, khoảng 3,69 GB |

Cần thêm dung lượng cho database và index sau nhập. Snapshot có khoảng 58 triệu
dòng lịch sử; các bảng ứng dụng ban đầu gồm 200 hồ sơ, 604 sự kiện chấm điểm và
3 tài khoản. Đây là số liệu snapshot, không phải số lượng cố định của database đang dùng.

## Chuẩn bị tệp và môi trường

File nén và `demo_accounts.json` nằm trong bộ bàn giao cục bộ, không có trong
bản clone GitHub. Lấy bản tương ứng từ gói dữ liệu riêng và đặt vào
`data/database/`. Cài Python/thư viện theo [README chính](../../README.md).
Các lệnh dưới đây chạy từ gốc `project/` bằng môi trường `.venv`.

## Khôi phục

1. Kiểm tra checksum và giải nén:

   ```powershell
   .venv\Scripts\python.exe scripts/prepare_database.py
   ```

   Công cụ tạo `data/database/database.sql`; nếu SQL đã có thì chỉ tái dùng khi
   checksum khớp, không ghi đè. Dùng `--check-only` nếu chỉ cần xác minh file nén.
   Script này không tự kết nối hoặc nhập dữ liệu vào MySQL.

2. Trong MySQL Workbench, tạo schema mới `home_credit_submission`, charset utf8mb4.
   Chọn **Server → Data Import → Import from Self-Contained File**, trỏ tới
   `data/database/database.sql`, chọn schema đích và **Dump Structure and Data → Start Import**.

3. Cấu hình Connector bằng biến môi trường hoặc JSON theo README chính.
   Mặc định JSON trỏ tới `home_credit_ml`; nếu khôi phục theo tên schema ở trên,
   đặt trong cùng terminal chạy lệnh:

   ```powershell
   $env:MYSQL_DATABASE = 'home_credit_submission'
   ```

   Đặt host, port, user phù hợp; mật khẩu lấy từ `MYSQL_PASSWORD` hoặc
   `configs/mysql_connection.local.json`. File local chỉ cung cấp mật khẩu.

4. Ngay sau nhập, đối chiếu số dòng snapshot:

   ```powershell
   .venv\Scripts\python.exe scripts/verify_database.py
   ```

   Lệnh đọc số dòng từng bảng và so với manifest, không phải kiểm tra toàn bộ
   giá trị hay checksum của database. Sau khi đăng nhập, chấm lại, thêm hồ sơ
   hoặc ghi chú, bảng tác nghiệp có thể lệch snapshot; không nhập đè database
   đang dùng chỉ để đưa các số đếm trở về bản bàn giao.

5. Khởi động:

   ```powershell
   .venv\Scripts\python.exe web/app.py
   ```

   Mở `http://127.0.0.1:5000`; đăng nhập bằng tài khoản trong gói bàn giao.

Dump đã có bảng, model và điểm demo, không cần `--init-db`, `--init-users`,
chạy lại notebook hoặc kích hoạt model để mở web. Các tệp dự báo đánh giá mà
trang `/model` đọc nằm ngoài SQL, cần giữ cùng bộ dự án đầy đủ.
[reset_demo_passwords.sql](reset_demo_passwords.sql) chỉ dùng khi chủ động muốn
đặt lại mật khẩu demo trên database đã nhập; không nằm trong luồng khôi phục thông thường.
