# So sánh bổ sung XGBoost và CatBoost

Phạm vi: hai cấu hình mỗi họ × A/B × ba fold đã có = **24 lượt fit mới**.
Chỉ dùng 184.506 hồ sơ train; không đọc nhãn validation/test và không thay model dashboard.
Đợt này được bổ sung sau đánh giá test lịch sử, không trình bày như protocol có trước lần test đó.

## Thiết kế đã chốt trước fit

| Họ | Cấu hình thay đổi | Thiết lập chung |
|---|---|---|
| XGBoost | max_depth 3 / 5 | 500 cây, learning_rate 0,05; hist, max_bin 128; min_child_weight 20; L2=5; subsample/colsample=0,8 |
| CatBoost | depth 4 / 6 | 500 vòng, learning_rate 0,05; L2=5; Plain boosting; Bernoulli subsample=0,8, rsm=0,8; max_ctr_complexity=1 |

Seed 42, bốn luồng mỗi fit, các fit chạy tuần tự. Không tăng trọng số lớp trong
đợt nhỏ này. Không early stopping trên fold probe; số vòng cố định 500.
Ngân sách nhỏ được công bố rõ, chưa gọi là tối ưu toàn bộ không gian tham số.

Numeric được chuyển float32, giữ NaN và số 0; không scale/log/impute. CatBoost
nhận category chuỗi. XGBoost học vocabulary từ phần fit của mỗi fold; category
mới tại probe thành missing. Chỉ so sánh các pipeline hoàn chỉnh trên cùng
đặc trưng gốc và cùng fold, không ép mọi thuật toán dùng cùng encoder.

Tiêu chí chính là mean CV Average Precision tính bởi sklearn, không đồng nhất
với PR-AUC hình thang. Tie-break giữ AP làm tròn bốn chữ số, ROC-AUC, thứ tự họ
LR/DT/RF/XGB/CAT, thời gian fit và case ID. Ba fold không phải kiểm định ý nghĩa
thống kê. Brier bổ sung là điểm thô, chưa hiệu chỉnh; không dùng ngưỡng LR cho
các mô hình mới.

## Chạy và tiếp tục

Cài `xgboost==3.4.1` và `catboost==1.2.10` bằng cùng Python chạy notebook.
Chạy cell import/đường dẫn đầu notebook 04 rồi các cell mục 15 để chỉ chạy phần mới.
Chạy toàn notebook cũng dùng lại cache cũ khi input/settings không đổi.

`experiment_plan.json` được lưu trước khi fit. Cache riêng nằm tại
`tmp/phase4_checkpoints/boosting-v1/<cache_id>`, có kiểm tra input/schema,
phiên bản thư viện, cấu hình, ID/nhãn và thứ tự fold. Mỗi fold xong được lưu
ngay; lần sau dùng checkpoint. `fit_s` trong checkpoint là thời gian fit đã lưu.
Không đổi `plan` hoặc key của thực nghiệm LR/DT/RF.

## Đầu ra

Các CSV dưới đây chỉ xuất khi đủ 24 fold, không có số liệu minh họa được ghi
thành kết quả thật:

- `cv_folds.csv`: 24 kết quả mới, AP/ROC-AUC/Brier, train AP, fit/predict time.
- `cv_summary.csv`: tám cấu hình mới, mean/std AP và gap train/CV.
- `expanded_ranking.csv`: so sánh ứng viên mới với LR/DT/RF đã hội tụ.
- `best_by_family.csv`: cấu hình A/B tốt nhất đã thử theo họ.

`Assets`, threshold, scoring history và dashboard giữ nguyên. Nếu muốn đưa
ứng viên mới lên web, calibration, threshold và artifact là bước riêng.

## So sánh theo năng lực rà soát

Đã đối chiếu LR, LR sigmoid, XGBoost và CatBoost ở top 5%, 10%, 20% bằng checkpoint OOF train. Xem [kết quả capacity](capacity/results.md) hoặc mục 16 trong notebook 04. Không train lại và giữ nguyên model dashboard.
