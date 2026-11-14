# Dữ liệu nghiên cứu

| Thư mục | Vai trò |
|---|---|
| `parquet/` | Tám bảng nguồn Home Credit |
| `raw_mysql/` | Kết quả đọc và đối soát MySQL đã lưu |
| `metadata/` | Từ điển biến, nguồn và manifest |
| `splits/` | Phân tập train/validation/test và CV fold cố định |
| `eda/` | Lịch sử tổng hợp đầu vào EDA |
| `features/` | Bộ đặc trưng A/B và chỉ mục |
| `model_input/` | Bản đối soát đầu vào mô hình qua MySQL |
| `database/` | Snapshot MySQL để chạy độc lập trên máy khác |

Giữ nguyên dữ liệu nguồn, ID, phân tập và nhãn. Các notebook đọc MySQL theo
luồng đã mô tả, không dùng bản Parquet đối soát để giả là kết quả truy vấn mới.
Xem [hướng dẫn khôi phục database](database/README.md).
