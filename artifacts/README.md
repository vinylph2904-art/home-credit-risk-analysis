# Mô hình dùng trong ứng dụng

Nguồn xác định phiên bản đang nạp là [inference_metadata.json](inference_metadata.json),
được `CreditRiskModel.loadModel()` đọc khi khởi tạo runtime.

| Thuộc tính hiện hành | Giá trị |
|---|---|
| Phiên bản | `catboost-selected-a8763faa0c2ef0786f72` |
| Ứng viên | `B_FILTER_CAT_02` |
| Model | CatBoost depth 6, 500 vòng |
| Đầu vào | 182 đặc trưng: 166 số, 16 phân loại |
| Artifact | `catboost_selected_a8763faa0c2ef0786f72/credit_risk_model.joblib` |
| Xác suất | Xác suất lớp 1 gốc từ `predict_proba`, `use_sigmoid=false` |
| Ngưỡng | `0.14539365168823878`, khoảng 14,5394%; cảnh báo khi `score >= threshold` |
| Dữ liệu fit cuối | 184.506 hồ sơ train; không fit lại trên train + validation |

Đây là bản được chốt ngày 30/10 và tích hợp dashboard ngày 31/10/2026.
Metadata còn lưu thứ tự cột, phương án xác suất, hash đăng ký và đường dẫn
đánh giá validation. Bản metadata trong thư mục model giữ cấu hình của chính artifact đó.

## Suy luận và diễn giải

`CreditRiskModel.prepareInput()` yêu cầu đủ đúng schema, đưa cột về đúng thứ tự,
chuyển số sang float32, giữ NaN/0 và từ chối giá trị vô hạn. Biến phân loại nhận
chuỗi hoặc giá trị thiếu; thiếu được thay bằng `__MISSING__`. Nhánh CatBoost
hiện tại không điền trung vị, log, scale hay one-hot trong bước suy luận.

`predict()` trả score từ `predict_proba()[:, 1]`, ngưỡng và cờ cảnh báo.
Đây không phải raw margin. SHAP trên trang chi tiết phân rã raw margin/logit;
sigmoid chuyển margin sang xác suất gốc khác với sigmoid calibration đã được
so sánh rồi không chọn. Web tải mô hình đã fit và không huấn luyện khi chấm điểm.

## Các artifact lịch sử còn giữ

| Vị trí | Vai trò |
|---|---|
| `0f70b06abaf3cbab/` | Pipeline Logistic Regression cũ; có `fit_metadata.json`, `frozen_policy.json` và metadata riêng |
| `catboost_4fec95c745d24f99893d/` | CatBoost bộ B 199 biến của đợt trước lọc, có `fit_metadata.json` và metadata riêng |
| `selected_model.json` | Quyết định LR lịch sử, không phải metadata runtime đang hoạt động |
| `catboost_selected_a8763faa0c2ef0786f72/` | Model sau Filter hiện hành, có `training_metadata.json` và metadata riêng |

## Đăng ký phiên bản trong MySQL

Nếu cần đăng ký bản đã chốt và bổ sung điểm cho hồ sơ hoạt động chưa có điểm của
phiên bản đó, chạy từ gốc dự án sau khi cấu hình MySQL:

```powershell
.venv\Scripts\python.exe scripts/activate_selected_model.py
```

Script kiểm tra hash với quyết định đã chốt, đăng ký `model_versions`, thêm
scoring events và cập nhật metadata hoạt động. Script giữ điểm lịch sử,
phân công, trạng thái rà soát và ghi chú; chạy lại không thêm điểm cho hồ sơ đã
có điểm của phiên bản hiện hành. Dump bàn giao đã đăng ký model nên không cần
chạy lại bước này để mở dashboard.

Xem [quyết định phiên bản](../reports/modeling/selected_model_evaluation_20261030/project_model_decision.md),
[kết quả](../reports/modeling/selected_model_evaluation_20261030/results.md) và
[bằng chứng kích hoạt](../reports/modeling/selected_model_evaluation_20261030/dashboard_activation.json).
Điểm hỗ trợ ưu tiên rà soát theo nhãn nguồn, chưa phải PD 12 tháng hoặc quyết định cho vay.
