# So sánh hiệu quả theo năng lực rà soát

Dùng các cấu hình đã chọn bằng CV AP: B_LR_02 (raw và sigmoid), B_XGB_01, B_CAT_02. Không chọn lại cấu hình theo kết quả capacity. Chỉ đọc checkpoint OOF train; không fit mới, không đọc nhãn validation/test, không thay model dashboard.

Kết quả chính: chọn top k riêng trong từng fold (k = ceil(tỷ lệ × số hồ sơ fold)), cộng số hồ sơ rà soát và TARGET = 1 tìm thấy của ba fold. Recall = tổng tìm thấy / tổng TARGET = 1; precision = tổng tìm thấy / tổng rà soát. Đây là năng lực phân bổ đều theo tỷ lệ cho từng fold, không phải một ngưỡng score chung. Xếp score giảm dần, hòa điểm theo Application ID tăng dần.

Có 184,506 hồ sơ, 14,895 TARGET = 1.

| Rà soát | Model | Số rà soát | TARGET = 1 tìm thấy | Recall | Precision | Thêm so với LR sigmoid |
|---|---|---:|---:|---:|---:|---:|
| 5% | LR raw | 9,228 | 3,151 | 21.15% | 34.15% | +0 |
| 5% | LR sigmoid | 9,228 | 3,151 | 21.15% | 34.15% | +0 |
| 5% | XGBoost | 9,228 | 3,292 | 22.10% | 35.67% | +141 |
| 5% | CatBoost | 9,228 | 3,331 | 22.36% | 36.10% | +180 |
| 10% | LR raw | 18,453 | 5,152 | 34.59% | 27.92% | +0 |
| 10% | LR sigmoid | 18,453 | 5,152 | 34.59% | 27.92% | +0 |
| 10% | XGBoost | 18,453 | 5,310 | 35.65% | 28.78% | +158 |
| 10% | CatBoost | 18,453 | 5,369 | 36.05% | 29.10% | +217 |
| 20% | LR raw | 36,903 | 7,985 | 53.61% | 21.64% | +0 |
| 20% | LR sigmoid | 36,903 | 7,985 | 53.61% | 21.64% | +0 |
| 20% | XGBoost | 36,903 | 8,194 | 55.01% | 22.20% | +209 |
| 20% | CatBoost | 36,903 | 8,185 | 54.95% | 22.18% | +200 |

## Nhận xét

Ở mức 10%, CatBoost tìm thấy 5,369 TARGET = 1, hơn LR sigmoid 217 hồ sơ với cùng 18,453 lượt rà soát. Recall tăng 1.46 điểm phần trăm; số tìm thấy tăng tương đối 4.21%.

CatBoost dẫn đầu ở 5% và 10%; tại 20%, XGBoost tìm thêm 9 hồ sơ so với CatBoost. CatBoost hơn LR ở cả ba fold tại cả ba mức capacity. Lợi ích có thật trong các phép đo này nhưng chưa phải bước nhảy lớn hoặc bằng chứng độc lập; CatBoost đáng đánh giá tiếp nếu hệ thống ưu tiên nhóm top 5–10%, còn LR vẫn là baseline đơn giản và model dashboard hiện tại.

Kiểm tra phụ bằng pooled OOF cũng giữ xu hướng: tại 10%, CatBoost tìm thêm 205 TARGET = 1 so với LR sigmoid. Số này khác bảng chính do cách phân bổ workload và thang score giữa các fold.

## Đối chiếu theo từng fold

| Rà soát | Fold | LR sigmoid tìm thấy | CatBoost tìm thấy | Chênh lệch |
|---|---:|---:|---:|---:|
| 5% | 0 | 1,030 | 1,098 | +68 |
| 5% | 1 | 1,059 | 1,131 | +72 |
| 5% | 2 | 1,062 | 1,102 | +40 |
| 10% | 0 | 1,689 | 1,786 | +97 |
| 10% | 1 | 1,730 | 1,793 | +63 |
| 10% | 2 | 1,733 | 1,790 | +57 |
| 20% | 0 | 2,651 | 2,718 | +67 |
| 20% | 1 | 2,645 | 2,730 | +85 |
| 20% | 2 | 2,689 | 2,737 | +48 |

## Cách hiểu và giới hạn

- TARGET = 1 là nhãn của dataset; không quy đổi thành default pháp lý, khoản lỗ hay lợi nhuận.
- Số tìm thêm là chênh lệch ròng ở cùng workload trên OOF train, không bảo đảm số tương tự khi triển khai.
- LR sigmoid là đối chứng gần với quy trình dashboard, nhưng ở đây dùng mô hình outer-fold; không dùng dự báo in-sample của artifact cuối.
- Sigmoid có thể đổi thứ hạng giữa các outer fold. Do đó bảng chính chọn riêng từng fold. Bảng pooled OOF là kiểm tra phụ, có thể chịu ảnh hưởng thang score khác nhau giữa các fold.
- Ba fold và các cấu hình đã chọn trên cùng train không phải đánh giá độc lập cuối cùng hoặc bằng chứng ý nghĩa thống kê.
- Không dùng ngưỡng 16,24% của LR cho CatBoost/XGBoost. Chưa hiệu chỉnh hoặc chọn threshold cho hai ứng viên mới.

[Bảng tổng hợp](capacity_summary.csv) · [Từng fold](fold_capacity.csv) · [Pooled OOF — kiểm tra phụ](pooled_oof_capacity.csv) · [Biểu đồ](recall_at_capacity.png) · [Nguồn checkpoint](checkpoint_manifest.json) · [Kiểm tra thực thi](execution.json)
