# Hoàn thiện CatBoost và đối chiếu với LR

Ứng viên **B_CAT_02**; bản cuối **CatBoost**, threshold **14.841034%**. Gate chi phí validation: **đạt**.

## Trạng thái dashboard

Đã kích hoạt phiên bản `catboost-4fec95c745d24f99893d-ff1d1fde` và bổ sung điểm cho 200 hồ sơ đang quản lý (31 cảnh báo). Giữ nguyên 202 scoring events cũ, artifact LR và review status. Phạm vi 200 hồ sơ dashboard khác tập validation bên dưới.

Đã đạt 21 kiểm tra tự động, kiểm tra 10 route trên MySQL và xác nhận trang đang chạy tại `http://127.0.0.1:5000/model`. Mục 17 notebook 04 chạy lại đầy đủ với model constructors/fit bị chặn: không fit thêm và số liệu/artifact metadata giữ nguyên.

[Nhật ký triển khai](deployment.json) · [Kiểm tra web](web_checks.json)

## Calibration trên train

Brier ngoài fold: raw **0.06655722**, sigmoid **0.06765967**. Theo quy tắc đã chốt, giữ raw. Mỗi outer probe tách khỏi cả fit model và fit calibrator; sigmoid chỉ học từ inner OOF của outer train. Đây là đánh giá calibration sau chọn ứng viên trên cùng train, không phải nested evaluation toàn bộ model search.

## Validation: cùng giả định chi phí FN:FP = 5:1

| Model | AP | ROC-AUC | Brier | Threshold | Precision | Recall | Alert rate | FN | FP | Cost / hồ sơ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LR_frozen | 0.246268 | 0.766496 | 0.06753235 | 16.2388% | 25.61% | 40.26% | 12.69% | 2,966 | 5,806 | 0.335534 |
| CatBoost_selected_5_to_1 | 0.266151 | 0.776024 | 0.06664714 | 14.8410% | 25.54% | 45.42% | 14.35% | 2,710 | 6,573 | 0.327193 |

Chênh lệch: cost giảm **2.49%**; recall đổi **+5.16 điểm phần trăm**; workload cảnh báo đổi **+1,023 hồ sơ**.

## Cùng năng lực rà soát trên validation

| Rà soát | Model | Số rà soát | TARGET = 1 tìm thấy | Recall | Precision |
|---|---|---:|---:|---:|---:|
| 5% | LR | 3,076 | 1,041 | 20.97% | 33.84% |
| 10% | LR | 6,151 | 1,712 | 34.48% | 27.83% |
| 20% | LR | 12,301 | 2,660 | 53.58% | 21.62% |
| 5% | CatBoost | 3,076 | 1,097 | 22.09% | 35.66% |
| 10% | CatBoost | 6,151 | 1,783 | 35.91% | 28.99% |
| 20% | CatBoost | 12,301 | 2,724 | 54.86% | 22.14% |

## Phạm vi và quyết định

- Candidate và quy tắc calibration/gate được lưu trước khi chạy. Không điều chỉnh hyperparameter theo validation/test.
- Threshold chọn trên validation theo cost 5:1, tie-break recall cao rồi threshold cao. LR dùng đúng threshold đã đóng băng.
- Validation đã dùng để chọn threshold; các chỉ số tại ngưỡng có tính lạc quan do selection và không phải đánh giá độc lập cuối cùng.
- Test lịch sử đã được xem trong thực nghiệm LR. Đợt mở rộng không đọc nhãn test và không trình bày như protocol có trước lần test đó.
- Không refit train + validation. Bản cuối chỉ fit trên train; schema và 199 đặc trưng gốc giữ nguyên.
- Score phản ánh TARGET dataset, chưa phải regulatory PD 12 tháng; alert hỗ trợ rà soát, không tự duyệt/từ chối.

[Protocol](protocol.json) · [Calibration](calibration_decision.json) · [Validation](validation_comparison.csv) · [Capacity](validation_capacity.csv) · [Biểu đồ](validation_evaluation.png) · [Kiểm tra](verification.json)
