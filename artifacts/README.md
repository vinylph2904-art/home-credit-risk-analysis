# Model dùng cho ứng dụng

Bản cuối cho đồ án được chốt ngày 30/10/2026: **CatBoost 182 biến, raw score, ngưỡng 14,5394%**. Model và metadata nằm trong `catboost_selected_a8763faa0c2ef0786f72/`. Xem [quyết định chốt phiên bản](../reports/modeling/selected_model_evaluation_20261030/project_model_decision.md). Bản này đã được tích hợp vào dashboard ngày 31/10/2026.

Model đang hoạt động: **CatBoost**, raw score, **182 biến**, threshold **14,5394%**.
Runtime đọc `artifacts/inference_metadata.json` và joblib tại `model_path`.
Metadata chứa phiên bản, họ model, thứ tự 182 đặc trưng, input preparation,
calibration, threshold và đường dẫn báo cáo đúng model.

`CreditRiskModel.prepareInput()` nhận đúng schema rồi `predict()` chấm điểm.
Với CatBoost: numeric float32, giữ NaN/0; categorical chuỗi, thiếu thành
`__MISSING__`. Các bước này không học thống kê; không impute/log/scale/one-hot.
Classifier và calibrator đã fit nằm trong artifact; web không huấn luyện.
SHAP trong chi tiết hồ sơ giải thích raw margin của CatBoost; bản hiện hành không dùng sigmoid,
không phải đóng góp vào score cuối hoặc nguyên nhân nhân quả.

LR cũ cùng `fit_metadata.json`, `frozen_policy.json`, `selected_model.json`
được giữ làm lịch sử. Metadata LR lưu tại
`0f70b06abaf3cbab/inference_metadata.json`. Các artifact cũ phục vụ đối chiếu
lịch sử; notebook 06–08 hiện dùng model sau Filter.

Schema MySQL giữ nguyên. Phiên bản mới được đăng ký và bổ sung scoring events;
không ghi đè điểm cũ, trạng thái rà soát hoặc ghi chú. `legacy_registration`
giữ hai trường hash tương thích với schema đã có.

Xem [kết quả](../reports/modeling/selected_model_evaluation_20261030/results.md) và
[bằng chứng chuyển phiên bản](../reports/modeling/selected_model_evaluation_20261030/dashboard_activation.json).
Chạy `py scripts/activate_selected_model.py` trên DB đã có dữ liệu để đăng ký model và bổ sung điểm cho hồ sơ hoạt động chưa có điểm của phiên bản mới. Chạy lại không thêm điểm cho hồ sơ đã chấm phiên bản này.
Score hỗ trợ ưu tiên rà soát theo nhãn nguồn, chưa phải PD 12 tháng hoặc quyết định vay.
