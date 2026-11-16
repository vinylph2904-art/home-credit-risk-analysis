# Luồng tám notebook nghiên cứu

Chạy theo thứ tự 01–08, mỗi file bằng kernel mới. Thư mục làm việc là gốc
`project/` hoặc `project/notebooks/`; các cell đầu tự xác định gốc dự án.
Mở bằng công cụ hỗ trợ `.ipynb` và chọn Python của `.venv` đã cài
`requirements.txt`. Gói này có kernel `ipykernel`, chưa bao gồm giao diện JupyterLab/Notebook.

## Điều kiện đầu vào

- Cấu hình MySQL và khôi phục database theo [hướng dẫn](../data/database/README.md).
  Notebook 01 đọc các bảng `raw_*`, không tự nạp tám bảng Parquet nguồn vào MySQL.
- Giữ các tệp dữ liệu lớn từ bộ bàn giao: phân tập, Parquet đặc trưng và dự báo
  không có trong bản clone GitHub. Xem [dữ liệu](../data/README.md).
- Notebook có thể ghi lại bảng, hình, schema, dự báo hoặc checkpoint. Tải và đọc
  output có sẵn không đòi hỏi chạy lại; chạy lại cell huấn luyện khi thiếu checkpoint
  hợp lệ có thể phát sinh fit mới.

## Thứ tự và đầu ra

| Notebook | Công việc hiện tại | Đầu ra chính |
|---|---|---|
| [01_data_understanding](01_data_understanding.ipynb) | Đọc MySQL, grain, khóa, TARGET; tạo/kiểm tra phân tập 60/20/20 và CV | `data/splits/`, `reports/data_understanding/` |
| [02_data_quality](02_data_quality.ipynb) | Trùng, thiếu, sentinel, ngoại lai và logic; tổng hợp đầu vào EDA | `data/eda/`, `reports/data_quality/` |
| [03_eda](03_eda.ipynb) | Đọc train từ MySQL và đầu ra notebook 02; khảo sát liên hệ với TARGET | Bảng và biểu đồ trong output notebook |
| [04_data_preparation_feature_engineering](04_data_preparation_feature_engineering.ipynb) | Làm sạch, tổng hợp sáu nguồn lịch sử, tạo A/B và schema | `data/features/`, `data/metadata/feature_dictionary.csv`, `reports/data_preparation/` |
| [05_feature_selection](05_feature_selection.ipynb) | Fit bộ lọc trong từng fold và toàn train | `reports/modeling/feature_selection_20261028/` |
| [06_model_training](06_model_training.ipynb) | Nhập bộ B vào MySQL; đọc lại train; chạy 21 cấu hình × 3 fold sau Filter | `reports/modeling/feature_selection_redo_20261029/` |
| [07_model_evaluation](07_model_evaluation.ipynb) | So sánh calibration trên train, fit cuối, chọn ngưỡng validation, đối chiếu test lịch sử | `reports/modeling/selected_model_evaluation_20261030/` và thư mục artifact riêng |
| [08_model_interpretation](08_model_interpretation.ipynb) | PredictionValuesChange, FP/FN, top-k, gains/decile và suy luận mẫu | `selected_model_evaluation_20261030/interpretation/` trong `reports/modeling/` |

Notebook 02 tạo bureau/POS tổng hợp cho 03; 04 tạo đặc trưng cho 05–06.
Notebook 06 mới nhập đặc trưng vào `application_features` và phân tập vào
`application_split`. Notebook 07 đọc schema/checkpoint của 06; notebook 08
đọc quyết định, model và dự báo của 07. Các notebook 01–04 và 06–07 cần MySQL.

## Mô hình và checkpoint hiện tại

Bộ A có 127 đặc trưng, B có 199. Bộ lọc được fit riêng trong fold và giữ
181 biến/fold; model cuối fit trên toàn train có 182 biến. Số này không phải
số chiều sau one-hot của các nhánh LR/DT/RF.

Checkpoint CV của 06 nằm trong
`reports/modeling/feature_selection_redo_20261029/cache/`; checkpoint calibration
của 07 nằm trong `reports/modeling/selected_model_evaluation_20261030/cache/`.
Việc dùng lại phụ thuộc ID, nhãn, schema và cấu hình khớp, không chỉ tên file.

Dashboard đọc `artifacts/inference_metadata.json`, hiện trỏ tới CatBoost 182 biến
đã tích hợp ngày 31/10/2026. Notebook 07 xuất model và metadata riêng, không tự
đổi model web; việc đăng ký/kích hoạt được mô tả ở [artifact](../artifacts/README.md).

Các chỉ số validation tại ngưỡng đã dùng chính validation để chọn ngưỡng;
test từng được quan sát trong phát triển và được gọi là test nội bộ lịch sử.
Các báo cáo A/B trước Filter vẫn được giữ trong `boosting_comparison/` và những
thư mục lịch sử khác; notebook 04 hiện không còn các mục huấn luyện 15–16 của bản cũ.
