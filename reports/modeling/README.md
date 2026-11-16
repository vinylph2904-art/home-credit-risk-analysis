# Kết quả thực nghiệm mô hình

Phiên bản ứng dụng được xác định bởi `artifacts/inference_metadata.json` ở gốc
dự án: `catboost-selected-a8763faa0c2ef0786f72`, 182 đặc trưng, xác suất lớp 1 gốc
(`use_sigmoid=false`), ngưỡng `0.14539365168823878`.

## Kết quả của luồng notebook 05–08 hiện tại

| Bước | Nơi đọc |
|---|---|
| Fit bộ lọc trên train và riêng trong từng CV fold, notebook 05 | [Feature selection](feature_selection_20261028/results.md) |
| 21 cấu hình × 3 fold = 63 lượt CV sau Filter, notebook 06 | [CV sau Filter](feature_selection_redo_20261029/results.md) |
| So sánh raw/sigmoid, ngưỡng validation và test lịch sử, notebook 07 | [Đánh giá model cuối](selected_model_evaluation_20261030/results.md) |
| Phiên bản và ngưỡng được chốt cho dự án | [Quyết định](selected_model_evaluation_20261030/project_model_decision.md) |
| Importance, sai số, top-k, gains/decile và suy luận mẫu, notebook 08 | [Diễn giải](selected_model_evaluation_20261030/interpretation/results.md) |
| Kiểm tra SHAP hai hồ sơ không nhãn bằng script bổ sung | [SHAP cục bộ](selected_model_evaluation_20261030/interpretation/shap_case_study_20261108/README.md) |
| Tích hợp bản đã chốt vào Flask/MySQL | [Tích hợp dashboard](selected_model_evaluation_20261030/dashboard_integration.md) |

Model cuối được fit trên 184.506 hồ sơ train với 182 biến; mỗi CV fold giữ
181 biến được chọn riêng. AP trung bình CV của CatBoost depth 6 là 0,267634.
Raw OOF Brier 0,06662082 thấp hơn sigmoid 0,06770763 nên giữ raw.

Các chỉ số lưu trong `selected_model_evaluation_20261030/evaluation_metrics.csv`:

| Tập | AP | ROC-AUC | Precision | Recall |
|---|---:|---:|---:|---:|
| Validation | 0,264876 | 0,775364 | 25,21% | 46,57% |
| Test nội bộ lịch sử | 0,280743 | 0,781073 | 26,05% | 46,53% |

Precision/recall ở cùng ngưỡng 0,14539365168823878. Trang `/model` hiển thị
validation, không phải test. Những tệp `*.parquet` chứa dự báo không nằm trong
bản clone GitHub; cần gói dữ liệu bàn giao khi chạy lại đánh giá hoặc mở trang mô hình.

## Các đợt nghiên cứu trước còn giữ

| Thư mục / nhóm tệp | Phạm vi |
|---|---|
| `04_*`, `selected_candidate.json`, `calibration_decision.json` tại đây | Đợt LR/DT/RF trước khi tách notebook; các tên file giữ mốc cũ |
| [boosting_comparison](boosting_comparison/README.md) | So sánh A/B trước Filter, có XGBoost và CatBoost; 24 lượt fit bổ sung |
| `catboost_finalization/` | CatBoost bộ B 199 biến, ngưỡng khoảng 14,8410% của đợt trước |
| `feature_study_20261026/`, `operational_assessment_20261026/` | Nghiên cứu đặc trưng và quy tắc rà soát của giai đoạn trước |

Các câu về model dashboard trong báo cáo lịch sử mô tả thời điểm đợt đó.
Đối chiếu model hiện tại theo metadata hoạt động và nhóm kết quả cuối ở trên;
không lấy AP/ngưỡng của bản 199 biến hoặc LR thay cho bản 182 biến.
`fit_s` là thời gian fit gốc, không phải thời gian tải checkpoint.

## Giới hạn diễn giải

Validation đã dùng để chọn ngưỡng; test từng được xem trong phát triển, không
phải kiểm định độc lập mới. AP là Average Precision, khác PR-AUC hình thang.
`5FN + FP` là điểm phạt giả định, chưa phải tổn thất bằng tiền. Brier không đo
riêng calibration; importance và SHAP không chứng minh nhân quả. Chưa có
đánh giá ngoài thời gian hoặc kết quả nghiệp vụ sau vận hành.
