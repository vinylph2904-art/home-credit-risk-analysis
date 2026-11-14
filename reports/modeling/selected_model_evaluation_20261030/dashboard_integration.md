# Tích hợp model cuối và đồng bộ tài liệu — 31/10/2026

Dashboard đã dùng **CatBoost 182 biến, raw score, ngưỡng 0,14539365168823878 (14,5394%)**.
Version: `catboost-selected-a8763faa0c2ef0786f72`.
SHA-256 joblib vẫn là `943571ed90e8ea591966dd27865c8348d7b43b77376a0770dbdd56548871435b`, khớp quyết định chốt. Không train hoặc chọn lại ngưỡng.

## Thay đổi

- Metadata runtime và metadata của artifact đã chốt được bổ sung đường dẫn báo cáo validation, importance, hình đánh giá và thông tin đăng ký MySQL. `log_columns` rỗng vì CatBoost không dùng log. Artifact 199 biến và metadata đối chứng lịch sử giữ nguyên.
- Trang Mô hình đọc tên file/policy từ metadata cho cả KPI, PR, ROC, confusion matrix, calibration, threshold và gains; không lấy báo cáo 199 biến. Hiển thị rõ validation đã dùng chọn ngưỡng; test lịch sử báo cáo riêng.
- Đầu vào inference, SHAP, bảng đặc trưng và CSV đầu vào dùng đúng thứ tự 182 biến. Thông tin hồ sơ/lịch sử vẫn đọc dữ liệu nguồn đầy đủ; các trường không được model chọn như giá hàng hóa không bị mất khỏi hồ sơ.
- Mô phỏng nhận dữ liệu nguồn để tính lại tỷ số khi đổi khoản vay/niên kim hoặc thu nhập, rồi chọn đúng 182 biến để predict. Không lưu điểm mô phỏng.
- `scripts/activate_selected_model.py` kiểm tra artifact đã chốt, đăng ký phiên bản và chỉ bổ sung điểm cho hồ sơ hoạt động chưa có điểm của phiên bản này. Đổi metadata runtime sau khi đăng ký/chấm điểm/đối soát xong. Không reseed hồ sơ hoặc xóa lịch sử.

## Dữ liệu MySQL

Lần kích hoạt đầu bổ sung **200 sự kiện cho 200 hồ sơ hoạt động**, giữ nguyên **402 sự kiện cũ**, toàn bộ hồ sơ, phân công, trạng thái và ghi chú. Bằng chứng: [dashboard_activation.json](dashboard_activation.json).

Hai lần POST chấm điểm khi xác minh HTTP tạo thêm hai sự kiện kiểm thử thật cho hồ sơ số 1. Tổng sau xác minh là 604 sự kiện; các sự kiện trước đó được đối chiếu toàn bộ cột và giữ nguyên. Lượt đầu đã chấm thành công nhưng kiểm tra đếm dùng snapshot đọc cũ của MySQL; đã sửa công cụ kiểm tra để kết thúc transaction đọc trước khi đếm lại dữ liệu do connection của Flask ghi.

Chạy lại activation ghi nhận **0 sự kiện mới**, 200 hồ sơ đã có điểm và 604 sự kiện được giữ nguyên: [dashboard_activation_latest.json](dashboard_activation_latest.json).

## Kiểm tra

- **135 test Python đạt**: 101 test runtime/scenario/capacity/login/RBAC/workspace; 3 regression mới cho artifact 182 biến, SHAP, mô phỏng với giá hàng hóa gốc và HTTP trang model; 31 test hàng đợi/analytics/financial reporting.
- Dự báo trên 100 hồ sơ validation khớp dự báo đã lưu với sai số tuyệt đối tối đa cho phép `1e-12`. SHAP khớp raw margin và danh sách đóng góp của đúng artifact.
- HTTP với MySQL thật: 10 URL chính đều trả 200, CSV đúng 182 cột, ba kịch bản mô phỏng đạt, POST score khớp inference trực tiếp, JSON event có đúng 182 đầu vào; đọc được lịch sử các phiên bản. Công cụ dùng fixture phiên đăng nhập của manager đang hoạt động; đăng nhập/mật khẩu được kiểm tra riêng bằng bộ test login/RBAC. Chi tiết: [dashboard_http_verification.json](dashboard_http_verification.json).
- **48 trường hợp trình duyệt đạt**, kích thước 1440/1024/390px, không lỗi JavaScript; trang model render sáu chart từ báo cáo mới. Audit browser dùng template thật, DB tài khoản độc lập và dữ liệu tài chính fixture, không phải toàn bộ dữ liệu MySQL thật. Fixture audit được bổ sung `scope_total` và `queue_tabs` để khớp trang hồ sơ hiện hành. Kết quả, ảnh model desktop.

Không chạy lại toàn bộ notebook hoặc CV/calibration; đợt này chỉ triển khai artifact đã chốt và kiểm tra các luồng liên quan.

## Tài liệu đã đồng bộ

README chính, hướng dẫn notebook/web/artifact, chỉ mục modeling, thiết kế hệ thống, checklist bàn giao, khung **35 slide**, kịch bản demo/vấn đáp, quyết định chốt và trạng thái diễn giải model.
Các tài liệu hiện hành dùng thống nhất 8 notebook, 21 cấu hình × 3 fold = 63 lượt CV, 181 biến riêng mỗi fold, 182 biến khi fit cuối. Các đợt 199 biến/102 lượt CV cũ được ghi là lịch sử. Bảng CV, calibration, validation, test và capacity trong khung slide đã lấy từ báo cáo model cuối.

Khung slide vẫn là nội dung Markdown, chưa phải deck PPTX; các mục tên thành viên, thời lượng và link bộ nộp còn cần nhóm điền theo thực tế.

## Chạy lại và sao lưu

Trên database đã có dữ liệu nghiên cứu/bảng web: `py scripts/activate_selected_model.py`, sau đó `py web/app.py`. Nếu có tiến trình web cũ, khởi động lại để tải metadata mới.

Metadata mặc định trước chuyển phiên bản nằm ở `backups/dashboard_activation_20261031/inference_metadata.json`; bản sao tài liệu trước đồng bộ ở `backups/dashboard_docs_20261031/`. Model và metadata 199 biến vẫn ở thư mục artifact lịch sử để đối chiếu; không xóa các scoring event đã ghi.
