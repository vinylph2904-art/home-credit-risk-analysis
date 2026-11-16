# So sánh XGBoost và CatBoost trước Filter

Đây là **kết quả lịch sử của đợt so sánh A/B trước chọn biến**: bộ A có 127,
bộ B có 199 đặc trưng. Đã hoàn tất hai cấu hình mỗi họ × hai bộ đặc trưng ×
ba fold = 24 lượt fit bổ sung trên 184.506 hồ sơ train. Đợt này không đọc
nhãn validation/test hoặc đổi model dashboard tại thời điểm chạy; nó được bổ sung
sau khi test lịch sử đã từng được quan sát.

Model hiện hành là CatBoost **sau Filter, 182 biến**, được chọn trong đợt khác.
Xem [kết quả mô hình hiện tại](../README.md). Các câu “dashboard vẫn dùng LR”
trong `results.md` mô tả trạng thái của đợt lịch sử, không phải runtime hiện nay.

## Thiết kế đã chạy

| Họ | Cấu hình thay đổi | Thiết lập chung |
|---|---|---|
| XGBoost | max_depth 3 / 5 | 500 cây, learning_rate 0,05; hist, max_bin 128; min_child_weight 20; L2=5; subsample/colsample=0,8 |
| CatBoost | depth 4 / 6 | 500 vòng, learning_rate 0,05; L2=5; Plain; Bernoulli subsample=0,8, rsm=0,8; max_ctr_complexity=1 |

Seed 42, bốn luồng/fit, chạy tuần tự, không tăng trọng số lớp và không dừng sớm
trên fold probe. Số vòng cố định 500. Numeric chuyển float32 và giữ NaN/0;
CatBoost nhận phân loại chuỗi, XGBoost lấy vocabulary từ phần fit, mức mới ở
probe thành missing. Đây là so sánh pipeline hoàn chỉnh, không ép dùng cùng encoder.

Tiêu chí chính là mean CV Average Precision. Quy tắc xử lý hòa của đợt này
dùng AP làm tròn bốn chữ số, ROC-AUC, thứ tự họ, fit time và case ID theo thiết kế
đã lưu. Brier ghi nhận thêm trên dự báo chưa hiệu chỉnh. Ba fold không tự tạo
thành kiểm định ý nghĩa thống kê. Phiên bản ghi trong execution: XGBoost 3.4.1,
CatBoost 1.2.10.

## Đọc và đối chiếu kết quả

- [results.md](results.md): kết quả và phạm vi của đợt chạy.
- [experiment_plan.json](experiment_plan.json): cấu hình đã lưu trước fit.
- [execution.json](execution.json): trạng thái hoàn tất và kiểm chứng 24 checkpoint.
- [cv_folds.csv](cv_folds.csv): chỉ số từng fold và thời gian fit/predict gốc.
- [cv_summary.csv](cv_summary.csv): tám cấu hình bổ sung, mean/std AP và train–CV gap.
- [expanded_ranking.csv](expanded_ranking.csv): đối chiếu với LR/DT/RF đã có.
- [best_by_family.csv](best_by_family.csv): cấu hình tốt nhất theo họ và A/B.
- [capacity/results.md](capacity/results.md): top 5%, 10%, 20% từ OOF train đã lưu.

Notebook 04 hiện chỉ chuẩn bị dữ liệu và đặc trưng; các mục huấn luyện 15–16
của notebook cũ không còn ở đó. Notebook 06 hiện chạy **CV sau Filter**, không
phải chạy lại nguyên đợt A/B trước Filter này. Repository giữ các kết quả và
thiết kế để tra cứu, không cung cấp lệnh một bước riêng tái chạy đợt lịch sử này.
