# Giải thích model 182 biến — 30/10/2026

**Kết luận:** notebook đã được cập nhật và thực thi bằng CatBoost 182 biến, raw score, ngưỡng 14,5394%. Ba biến đứng đầu theo PredictionValuesChange là `EXT_SOURCE_3` (14.57), `EXT_SOURCE_2` (13.70) và `EXT_SOURCE_1` (5.41). Đây là mức quan trọng toàn cục trong model, không phải đóng góp riêng của từng hồ sơ hoặc quan hệ nhân quả.

Trên validation, top 10% score có tỷ lệ TARGET = 1 là **28.66%**, tìm được **35.51%** tổng số ca TARGET = 1 và lift **3.55 lần**. Các chỉ số tương ứng trên test lịch sử là **29.59%**, **36.66%** và **3.67 lần**. Khả năng tập trung rủi ro hỗ trợ phân bổ lượt rà soát; chưa đủ để tự thiết lập chính sách cho vay.

Đã lưu importance của toàn bộ 182 biến, 10 ví dụ sai số, bảng decile/capacity và kết quả chấm năm hồ sơ chưa có nhãn trong `reports/modeling/selected_model_evaluation_20261030/interpretation/`. Biểu đồ được xuất PNG/PDF; ví dụ nạp model dùng metadata riêng của bản đã chốt.

Notebook 05–08 hiện thống nhất cùng quy trình sau Feature Selection. Artifact đã chốt đã được tích hợp lên dashboard ngày 31/10/2026. Các kết quả test được ghi rõ là lịch sử và không được dùng để chọn lại model hoặc ngưỡng.

Phần sử dụng trained model phù hợp với MLBA 08 và MLBA 13; cách diễn giải nghiệp vụ được đối chiếu với Rose & Hudgins (2008), chương 16 và 18.
