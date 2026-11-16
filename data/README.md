# Dữ liệu nghiên cứu và dữ liệu bàn giao

Các thư mục dưới đây đang có trong bộ dự án cục bộ:

| Thư mục | Nội dung và bước sử dụng |
|---|---|
| `parquet/` | Tám bảng nguồn Home Credit ở định dạng Parquet |
| `raw_mysql/` | Bản đọc/đối soát tám bảng MySQL đã lưu; không thay thế truy vấn mới |
| `metadata/` | Từ điển nguồn, từ điển đặc trưng, manifest và thông tin nguồn gốc |
| `splits/` | Phân tập cố định, gồm `application_split.parquet` và `split_manifest.json` |
| `eda/` | Tổng hợp bureau/POS do notebook 02 tạo để notebook 03 đọc |
| `features/` | Bộ A/B theo train, validation, test, application_test; lịch sử tổng hợp và `feature_index.parquet` do notebook 04 tạo |
| `model_input/mysql/` | Bản đối soát đầu vào đọc qua MySQL ở bước mô hình |
| `database/` | Snapshot MySQL và hướng dẫn khôi phục trên máy khác |

## Bản cục bộ và bản clone GitHub

`.gitignore` loại toàn bộ `*.parquet`, `*.sql.gz`, SQL đã giải nén và
`database/demo_accounts.json` khỏi Git. Vì vậy clone repository chỉ nhận mã nguồn,
CSV/JSON metadata và hướng dẫn; không nhận đủ dữ liệu để chạy web/notebook ngay.

- Để mở dashboard: lấy `database.sql.gz` từ bộ dữ liệu bàn giao riêng, đặt vào
  `data/database/` và [khôi phục MySQL](database/README.md). Model joblib và
  metadata được lưu trong repository; các dự báo Parquet phục vụ trang mô hình
  cũng cần được bổ sung vào đúng thư mục `reports/modeling/` từ bộ bàn giao.
- Để chạy lại nghiên cứu: bổ sung các tệp Parquet và đầu ra phụ thuộc theo
  [luồng notebook](../notebooks/README.md). Có Parquet nguồn chưa đồng nghĩa
  database đã có các bảng `raw_*`; notebook 01 bắt đầu bằng đọc MySQL.
- Thông tin tài khoản demo được cung cấp riêng trong bộ bàn giao. Không dùng
  tài khoản đăng nhập dashboard thay cho tài khoản kết nối MySQL.

Giữ nguyên dữ liệu nguồn, ID, phân tập và nhãn. `TARGET` chỉ có trong
`application_train`; `application_test` không có nhãn và không dùng để tính hiệu năng.
Notebook 06 nhập bộ B 199 đặc trưng vào MySQL. Bộ lọc giữ 181 biến trong mỗi
CV fold và 182 biến khi fit trên toàn train; dữ liệu MySQL không vì vậy chỉ còn 182 cột.
