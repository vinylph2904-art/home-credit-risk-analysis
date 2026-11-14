# Kết quả thực nghiệm mô hình

Phiên bản dashboard hiện hành: CatBoost 182 biến, raw score,
ngưỡng `0.14539365168823878` (14,5394%).

| Nội dung | Kết quả |
|---|---|
| Chọn biến trên train và trong từng CV fold | [Feature selection](feature_selection_20261028/) |
| So sánh 21 cấu hình × 3 fold = 63 lượt CV sau Filter | [CV sau Filter](feature_selection_redo_20261029/results.md) |
| Calibration, ngưỡng validation và test lịch sử | [Đánh giá model cuối](selected_model_evaluation_20261030/results.md) |
| Quyết định phiên bản/ngưỡng | [Quyết định](selected_model_evaluation_20261030/project_model_decision.md) |
| Importance, sai số, gains/decile và ví dụ dự báo | [Diễn giải](selected_model_evaluation_20261030/interpretation/results.md) |
| Tích hợp model vào ứng dụng | [Tích hợp dashboard](selected_model_evaluation_20261030/dashboard_integration.md) |

Notebook 05 chọn biến; 06 so sánh mô hình; 07 fit trên train, kiểm tra calibration,
chọn ngưỡng trên validation và đánh giá test lịch sử; 08 diễn giải và minh họa inference.
Model cuối dùng 182 biến; từng CV fold dùng 181 biến được chọn riêng trong fold.

## Thực nghiệm trước đó

Các file `04_*`, `boosting_comparison/`, `catboost_finalization/`,
`feature_study_20261026/` và `operational_assessment_20261026/` giữ kết quả
của các giai đoạn trước. Phiên bản 199 biến và LR trong các báo cáo đó
khác phiên bản dashboard hiện hành; không dùng metrics của chúng thay model cuối.
Thời gian fit là thời gian thực nghiệm gốc, không phải thời gian tải checkpoint.

## Giới hạn

Test đã được xem trong quá trình phát triển, không phải kiểm định độc lập mới.
AP là Average Precision; Precision/Recall phụ thuộc ngưỡng.
Phạt `5FN + FP` là giả định phân tích, chưa quy đổi thành tiền.
Importance và SHAP không chứng minh quan hệ nhân quả.
Chưa có outcome sau vận hành hoặc kiểm định ngoài thời gian.
