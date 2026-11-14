# Đánh giá CatBoost sau Feature Selection — 30/10/2026

## Thiết kế

Chọn CatBoost depth=6 theo AP trung bình ba fold ở notebook 06. Giữ 500 vòng boosting và các tham số của đợt CV. Raw OOF của ứng viên được đối soát với dữ liệu, nhãn và fold của notebook 06.

So sánh raw và sigmoid trên train bằng ba outer fold. Trong mỗi outer train, ba inner fold tạo dự báo OOF để học sigmoid; selector được fit lại trong từng inner fit, rồi refit trên toàn outer train. Mỗi outer fold cần bốn base fits, tổng cộng 12. Danh sách refit outer khớp 181 biến của notebook 05–06. Đây là đánh giá calibration cho ứng viên đã chọn, không phải nested CV cho toàn bộ việc lựa chọn mô hình.

Chọn sigmoid chỉ khi Brier ngoài fold thấp hơn raw. Sau đó fit phương án đã chọn trên toàn train với danh sách 182 biến. Ngưỡng được chọn trên validation theo 5FN + FP, khi hòa ưu tiên recall rồi ngưỡng cao hơn. Quy tắc này được lưu trước khi đọc validation/test; model và ngưỡng được đóng băng trước khi đọc test lịch sử.

## Kết quả và giới hạn

**Kết luận:** chọn **raw** theo Brier ngoài fold trên train: raw = 0.06662082, sigmoid = 0.06770763. Model cuối là CatBoost depth=6, 500 vòng, fit trên 184.506 hồ sơ train với **182 biến**.

Ngưỡng cảnh báo chọn trên validation là **14,5394%** theo 5FN + FP. Kết quả tại ngưỡng đã đóng băng:

| Phạm vi | AP | ROC-AUC | Precision | Recall | Tỷ lệ cảnh báo |
| --- | ---: | ---: | ---: | ---: | ---: |
| Validation | 0.264876 | 0.775364 | 25,21% | 46,57% | 14,91% |
| Test nội bộ lịch sử | 0.280743 | 0.781073 | 26,05% | 46,53% | 14,42% |

Tại ngưỡng này, 74,79% số cảnh báo validation là ca TARGET = 0 và 53,43% ca TARGET = 1 bị bỏ sót. Model hỗ trợ xếp thứ tự rà soát; các chỉ số hiện tại chưa đủ để tự chốt chính sách duyệt hoặc từ chối tự động khi chưa có giới hạn chi phí, năng lực xử lý và mục tiêu rủi ro của đơn vị sử dụng.

Model, ngưỡng và các dự báo mới đã lưu trong `reports/modeling/selected_model_evaluation_20261030/` cùng thư mục artifact ghi trong `execution.json`. Đã kiểm tra nạp model bằng `CreditRiskModel` và đối chiếu điểm chấm với dự báo trực tiếp. Dashboard vẫn dùng model đã triển khai trước đó.

Notebook 08 đã cập nhật theo artifact 182 biến để giải thích đặc trưng, minh họa sai số và phân tầng rủi ro. Phiên bản này đã được chốt cho đồ án; tích hợp lên dashboard là bước tiếp theo. Test trong bảng là test lịch sử đã được xem; model và ngưỡng được đóng băng trước lần chấm này và không được chọn lại từ các chỉ số test.


## Đầu ra

- `protocol.json`: ứng viên, tham số và quy tắc đánh giá đã chốt.
- `source_data_identity.json`: đối soát đầu vào MySQL với đợt CV trước.
- `calibration_comparison.csv`, `calibration_folds.csv`: so sánh calibration và thời gian từng outer fold.
- `train_oof_predictions.parquet`: raw và sigmoid OOF trên train.
- `threshold_sensitivity.csv`, `validation_metrics.csv`: ngưỡng và kết quả validation của model 182 biến.
- `final_decision_before_test.json`: model và ngưỡng đã đóng băng.
- `evaluation_metrics.csv`, `capacity_metrics.csv`: chỉ số tại ngưỡng và tại top 5/10/20%.
- `validation_predictions.parquet`, `historical_test_predictions.parquet`: dự báo của bản 182 biến.
- `figures/`: calibration, ROC, Precision–Recall và ma trận nhầm lẫn ở định dạng PNG/PDF.
- `execution.json`: đường dẫn model, metadata và trạng thái hoàn tất.

Các cell notebook đã được thực thi tuần tự bằng Python; output và hình được lưu vào notebook. Không ghi đè metadata mặc định của model dashboard.
