# Minh họa SHAP cục bộ ngày 08 tháng 11 năm 2026

Phân tích suy luận bổ sung cho mục 4.5.1 của báo cáo, sử dụng artifact
`catboost-selected-a8763faa0c2ef0786f72`: CatBoost 1.2.10, 182 đặc trưng,
`use_sigmoid=false`, ngưỡng `0.14539365168823878`. Đây không phải đợt huấn luyện lại.

Hai hồ sơ 100001 và 100005 là hai dòng đầu trong `../sample_predictions.csv`
đã có, được chọn trước khi tính SHAP. Cả hai thuộc `application_test`, chưa có
TARGET; không gọi chúng là FP/FN hoặc dùng để xác nhận dự báo đúng/sai.

## Tệp kết quả đang lưu

- [verification.json](verification.json): model/hash, môi trường, quy tắc chọn hồ sơ và bốn nhóm kiểm tra; kết quả ghi nhận ngày 08/11/2026 là `passed`.
- [case_summary.csv](case_summary.csv): điểm, ngưỡng, cảnh báo, giá trị nền, tổng SHAP, margin và sai số tái tạo.
- [shap_values_all_features.csv](shap_values_all_features.csv): đủ 182 đóng góp của mỗi hồ sơ.
- `selected_inputs.parquet`: đầu vào theo feature_order; tệp Parquet được bàn giao riêng, không theo dõi trong Git.
- [shap_waterfall.png](shap_waterfall.png), [shap_waterfall.pdf](shap_waterfall.pdf) và [waterfall_verification.json](waterfall_verification.json): hình minh họa và đối chiếu hình đã lưu.

## Kiểm tra lại bằng script hiện có

Từ gốc `project/`, dùng môi trường đã cài `requirements.txt`:

```powershell
.venv\Scripts\python.exe scripts/verify_shap_case_study.py
```

Script cần `data/features/b/application_test.parquet`, model và metadata hiện hành,
cùng `sample_predictions.csv` đã lưu. Nó không cần kết nối MySQL, không fit model
và không thay ngưỡng, nhưng **ghi lại** `verification.json`, `case_summary.csv`,
`shap_values_all_features.csv` và `selected_inputs.parquet` trong thư mục này.
Script không tạo lại các hình waterfall.

Các phép kiểm tra: giá trị nền + toàn bộ SHAP khớp raw margin với atol=1e-10;
sigmoid(margin) và điểm mẫu khớp `predict_proba` với atol=1e-12; top 10 do hàm
web trả về khớp SHAP CatBoost với atol=1e-10. Kết quả mới phải đọc từ lần chạy mới,
không mặc nhiên lấy trạng thái `passed` của đợt đã lưu.

SHAP thuộc thang raw margin/logit, không phải điểm phần trăm xác suất.
Sigmoid chuyển margin sang xác suất gốc khác với sigmoid calibration đã so sánh
trên train OOF. Minh họa không xác lập nhân quả, độ ổn định SHAP hoặc tính công bằng.
