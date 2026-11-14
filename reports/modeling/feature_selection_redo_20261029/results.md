# Huấn luyện và so sánh mô hình sau Feature Selection

## Phương pháp

Đầu vào là bộ B trước Filter. Trong từng fold, selector chỉ fit trên 123.004 hồ sơ thuộc phần train, giữ 181 biến và áp dụng danh sách đó cho 61.502 hồ sơ giữ lại. Khi fit selector trên toàn bộ 184.506 hồ sơ train, danh sách giữ 182 biến và được dành cho mô hình cuối.

Đã hoàn tất 21 cấu hình × ba fold = 63 lượt CV thuộc Dummy, Logistic Regression, Decision Tree, Random Forest, XGBoost và CatBoost. Tiêu chí chính là AP trung bình ngoài fold; đọc thêm độ lệch chuẩn, ROC-AUC, Brier và khoảng cách train–CV. Không dùng validation/test để chọn cấu hình.

## Kết quả

| Mô hình | AP trung bình | Độ lệch chuẩn AP | ROC-AUC trung bình |
| --- | ---: | ---: | ---: |
| CAT | 0.267634 | 0.001476 | 0.776217 |
| XGB | 0.266853 | 0.003741 | 0.776353 |
| LR | 0.252025 | 0.001026 | 0.767299 |
| RF | 0.243669 | 0.000888 | 0.757852 |
| DT | 0.182422 | 0.001711 | 0.699892 |
| Dummy | 0.080729 | 0.000000 | 0.500000 |

CatBoost depth=6 đứng đầu theo AP trong ngân sách cấu hình đã thử. Chênh lệch nhỏ với XGBoost chưa đủ để khẳng định mô hình nào luôn tốt hơn trên dữ liệu mới. Nhóm chốt CatBoost làm ứng viên cho calibration và đánh giá tại ngưỡng.

## Đầu ra và bàn giao

- `selected_cv_folds.csv`: kết quả 63 lượt CV.
- `selected_cv_summary.csv`: tổng hợp toàn bộ cấu hình.
- `selected_best_by_family.csv`: cấu hình tốt nhất theo từng họ mô hình.
- `selected_features_by_fold.json`: danh sách biến theo fold.
- `selected_schema_train_only.json`: schema 182 biến để fit cuối.

Notebook 07 đã hoàn tất calibration, fit model cuối và chọn ngưỡng trên validation. Notebook 08 đã cập nhật giải thích mô hình. Xem [quyết định chốt phiên bản](../selected_model_evaluation_20261030/project_model_decision.md).
