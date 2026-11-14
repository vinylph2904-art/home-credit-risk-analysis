# Kết quả so sánh bổ sung

Đã hoàn tất 24 lượt CV: tám cấu hình XGBoost/CatBoost trên A/B, đúng ba fold train đã có. Tổng thời gian đợt chạy: 23.34 phút; tổng fit_s: 21.72 phút. Peak working set toàn process: 1640.2 MiB, gồm import và dữ liệu đầu vào.

| Họ | Best A AP | Best B AP |
|---|---:|---:|
| LR | 0.227260 | 0.252262 |
| DT | 0.185308 | 0.182051 |
| RF | 0.221540 | 0.243515 |
| XGB | 0.239296 | 0.267258 |
| CAT | 0.241262 | 0.269328 |

Ứng viên CV đứng đầu: **B_CAT_02**, AP = **0.269328**, std = 0.000637, ROC-AUC = 0.777032. So với B_LR_02 (0.252262), chênh AP tuyệt đối là 0.017066.

Đây là kết quả trong ngân sách cấu hình đã thử; ba fold không đủ để tự kết luận khác biệt có ý nghĩa thống kê. Preprocessing native của boosting khác pipeline LR/DT/RF, nên đây là so sánh toàn bộ learning procedure. Đợt này được bổ sung sau đánh giá test lịch sử.

**Dashboard vẫn dùng B_LR_02**, pipeline sigmoid và threshold cũ. Chưa fit model mới trên toàn train để triển khai, chưa calibration/chọn threshold cho model mới, không đọc nhãn validation/test.

Đã kiểm tra đầy đủ 24 checkpoint, tính lại AP/ROC-AUC/Brier từ các điểm OOF, và chạy warm resume với chốt chặn không cho tạo model mới. artifacts/configs/web và output cũ trong notebook giữ nguyên.

[Biểu đồ](cv_ap_comparison.png) · [CV từng fold](cv_folds.csv) · [Tám cấu hình](cv_summary.csv) · [Xếp hạng mở rộng](expanded_ranking.csv) · [Thiết kế](experiment_plan.json) · [Kiểm chứng](execution.json)

Phân tích bổ sung: [hiệu quả tại top 5%, 10%, 20% hồ sơ](capacity/results.md).
