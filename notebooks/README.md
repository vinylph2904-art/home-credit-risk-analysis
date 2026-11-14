# Luồng notebook

| Notebook | Nội dung |
|---|---|
| [01_data_understanding](01_data_understanding.ipynb) | Nguồn dữ liệu, grain, khóa, TARGET và phân tập |
| [02_data_quality](02_data_quality.ipynb) | Trùng lặp, missing, sentinel, ngoại lai, kiểm tra logic; xuất đầu vào EDA |
| [03_eda](03_eda.ipynb) | Quan hệ giữa các nhóm đặc điểm/lịch sử và TARGET trên train |
| [04_data_preparation_feature_engineering](04_data_preparation_feature_engineering.ipynb) | Cleaning, aggregate, A/B, từ điển và schema |
| [05_feature_selection](05_feature_selection.ipynb) | Filter trong từng fold; xuất schema 182 biến trên toàn train |
| [06_model_training](06_model_training.ipynb) | 63 lượt CV sau Filter, dùng 181 biến/fold; so sánh sáu họ mô hình |
| [07_model_evaluation](07_model_evaluation.ipynb) | Fit model 182 biến, calibration, ngưỡng validation và đánh giá test lịch sử |
| [08_model_interpretation](08_model_interpretation.ipynb) | Importance, ví dụ sai sót, gains/decile và minh họa chấm điểm |

Chạy mỗi file bằng kernel mới từ thư mục project hoặc `notebooks/`. Notebook 02 tạo đầu vào lịch sử cho 03; 04 tạo A/B và schema; 05 chọn biến. Notebook 06 đã hoàn tất train CV sau Filter, dùng 181 biến riêng cho mỗi fold. Notebook 07 đã fit bản cuối với 182 biến, đánh giá calibration và chốt ngưỡng trên validation. Notebook 08 đã cập nhật giải thích mô hình và ví dụ chấm điểm theo artifact 182 biến. Dashboard đã dùng cùng bản 182 biến từ ngày 31/10/2026.


Các kết quả test đã được quan sát trước đây được ghi rõ là test lịch sử.
