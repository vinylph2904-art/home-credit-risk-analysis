# Chốt mô hình cho đồ án — 30/10/2026

Nhóm chốt CatBoost depth=6, 500 vòng, dùng 182 đặc trưng và raw score làm phiên bản cuối cho đồ án. Ngưỡng cảnh báo là 0,14539365168823878 (14,5394%), được chọn trên validation theo điểm phạt giả định 5FN + FP. Không mở rộng tuning trong phạm vi hiện tại.

Ứng viên được chọn theo AP trên train CV; calibration được chọn theo Brier ngoài fold trên train. Kết quả test lịch sử được dùng để báo cáo, không làm căn cứ chọn lại mô hình hoặc ngưỡng. Việc chốt phiên bản không phải là xác nhận mô hình đã đủ điều kiện vận hành tín dụng tự động.

Model hỗ trợ xếp thứ tự ưu tiên rà soát hồ sơ. Giới hạn về cảnh báo nhầm, bỏ sót, dữ liệu mới và giả định chi phí được giữ trong báo cáo đánh giá.

- Model: `artifacts/catboost_selected_a8763faa0c2ef0786f72/credit_risk_model.joblib`.
- Metadata: `artifacts/catboost_selected_a8763faa0c2ef0786f72/inference_metadata.json`.
- Quyết định và mã đối chiếu artifact: `project_model_decision.json` trong thư mục này.

Notebook 08 đã cập nhật và thực thi theo artifact đã chốt. Dashboard đã chuyển sang cùng model 182 biến ngày 31/10/2026; đăng ký phiên bản mới và bổ sung 200 sự kiện chấm điểm, giữ nguyên 402 sự kiện cũ, hồ sơ, phân công, trạng thái và ghi chú. Xem `dashboard_activation.json` và `dashboard_integration.md`.
