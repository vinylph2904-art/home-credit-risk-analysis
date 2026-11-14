# Minh họa SHAP cục bộ — 08/11/2026

Đây là phân tích suy luận bổ sung cho mục 4.5.1, không phải chạy lại huấn luyện hay thay thế kết quả notebook 08 đã lưu ngày 30/10.

- Artifact: catboost-selected-a8763faa0c2ef0786f72; CatBoost 1.2.10; 182 đặc trưng; use_sigmoid=false; ngưỡng 0.14539365168823878.
- Hai hồ sơ 100001 và 100005 là hai dòng đầu của sample_predictions.csv có sẵn, được chọn trước khi tính SHAP. Cả hai thuộc application_test, chưa có TARGET. Không gọi chúng là FP/FN hoặc dùng để xác nhận độ chính xác.
- Mô hình, ngưỡng và database không thay đổi. Không đánh giá độ ổn định SHAP hoặc tính công bằng trong bước này.

## Tệp kết quả

- verification.json: danh tính/mã băm nguồn, môi trường, quy tắc chọn hồ sơ, bốn nhóm kiểm tra và top 5 đóng góp.
- case_summary.csv: điểm, ngưỡng, cảnh báo, giá trị nền, tổng SHAP, raw margin, sai số tái tạo.
- shap_values_all_features.csv: đủ 182 đóng góp cho mỗi hồ sơ.
- selected_inputs.parquet: đầu vào chọn theo feature_order; giữ độ chính xác dữ liệu để tái hiện.

## Cách kiểm tra lại

Từ thư mục dự án, chạy `py -3.14 scripts/verify_shap_case_study.py`.

Script kiểm tra tổng SHAP cộng giá trị nền khớp raw margin với atol=1e-10; sigmoid(raw margin) và điểm trong sample_predictions.csv khớp predict_proba với atol=1e-12; top 10 trong hàm web khớp SHAP CatBoost với atol=1e-10. Kết quả hiện tại passed.

SHAP thuộc thang raw margin, không phải điểm phần trăm xác suất. Hàm sigmoid chuyển raw margin của bộ phân loại sang xác suất gốc không đồng nhất với sigmoid calibration đã so sánh trên train OOF. Các đóng góp được diễn giải theo hồ sơ, không suy ra quan hệ nhân quả.
