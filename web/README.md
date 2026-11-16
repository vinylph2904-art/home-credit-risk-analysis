# Dashboard Flask

Từ thư mục `project/`, sau khi cài thư viện và khôi phục database, chạy:

```powershell
.venv\Scripts\python.exe web/app.py
```

Mở `http://127.0.0.1:5000`; dùng `--port 5001` nếu cần đổi cổng. Ứng dụng chỉ
bind `127.0.0.1` và chạy với `debug=False`. Xem [cài đặt](../README.md) và
[khôi phục database](../data/database/README.md). Lệnh `--help` cũng import
runtime/model, nên cần môi trường thư viện và artifact hợp lệ.

## Chức năng và quyền truy cập

| Vai trò | Phạm vi |
|---|---|
| `admin` | Quản lý tài khoản, vai trò, trạng thái hoạt động và nhật ký tài khoản; vào `/admin/users` sau đăng nhập |
| `risk_manager` | Xem danh mục, lịch sử tín dụng, phân tích; thêm/nhập, phân công, lưu trữ/xóa hồ sơ; chấm điểm và rà soát |
| `analyst` | Xem, chấm điểm và rà soát hồ sơ được phân công; xem lịch sử trong phạm vi đó, sửa/xóa ghi chú do mình tạo |

Tổng quan tài chính và phân tích phân khúc mặc định dùng dữ liệu train nghiên cứu;
một số trang hỗ trợ đổi sang danh mục quản lý. Dư nợ/quá hạn và thanh toán/thẻ
sử dụng lịch sử của danh mục được lọc. Số hồ sơ trên màn hình phụ thuộc dữ liệu,
bộ lọc và vai trò, không cố định ở 200 sau khi người dùng cập nhật danh mục.

- Danh sách `/applications` có hàng đợi, phân công, tìm kiếm, bộ lọc và xuất CSV/Excel/PDF.
- Nhập CSV UTF-8 hoặc `.xlsx` theo mẫu tải từ giao diện: tối đa 1.000 dòng, request tối đa 1 MiB; Excel cần đúng một sheet và không chứa công thức.
- Chấm điểm đơn lẻ hoặc hàng loạt; mỗi sự kiện lưu điểm, ngưỡng, phiên bản và snapshot đầu vào. Nút chấm các hồ sơ chưa có điểm xử lý tối đa 200 hồ sơ mỗi lượt.
- Cập nhật trạng thái Mới / Đang xem xét / Đã rà soát và ghi chú theo sự kiện chấm.
- Mô phỏng đầu vào một hồ sơ hoặc kịch bản ngưỡng/năng lực rà soát trên danh mục; các mô phỏng không ghi điểm chính thức hoặc đổi ngưỡng đã lưu.
- Trang `/model` đọc kết quả validation của phiên bản hiện hành; `/history` lưu riêng các lần chấm điểm.

Hồ sơ quản lý liên kết với `application_test` đã có đặc trưng. Nhập tệp là nhập
danh sách quản lý, chưa phải tiếp nhận hồ sơ gốc bất kỳ rồi tự tạo đặc trưng.
Ghi chú và trạng thái rà soát không phải nhãn kết quả thanh toán.

## Mô hình và cấu trúc mã

Runtime đọc `artifacts/inference_metadata.json`: CatBoost 182 đặc trưng,
`use_sigmoid=false`, ngưỡng `0.14539365168823878`. Score là xác suất lớp 1 gốc
từ `predict_proba`; SHAP giải thích raw margin/logit, không phải điểm phần trăm
xác suất hay tác động nhân quả. Xem [artifact](../artifacts/README.md).

`app.py` khởi tạo Flask và đăng ký các module `*_routes.py`. `runtime.py` tải model
và cấp kết nối MySQL theo request. Template nằm trong `templates/`, CSS/JavaScript
và logo trong `static/`, font xuất báo cáo trong `assets/fonts/`.

## Khởi tạo khi đã có database nghiên cứu

Dump bàn giao đã có bảng ứng dụng, tài khoản và điểm demo nên không cần bước này.
Nếu database chỉ có dữ liệu nghiên cứu, `application_features`, `application_split`
và metadata phù hợp, dùng:

```powershell
.venv\Scripts\python.exe web/app.py --init-db --seed-demo 200
```

`--init-db` đã gọi khởi tạo users, đăng ký model và thêm hồ sơ demo. Tham số
`--seed-demo` nhận từ 0 đến 1.000. Lệnh `--init-users` riêng chỉ phục vụ khởi tạo
bảng người dùng/liên kết phân công trên database đã có `demo_profiles`.
Các biến `HC_ADMIN_PASSWORD`, `HC_MANAGER_PASSWORD`, `HC_DASHBOARD_PASSWORD`
được dùng khi tạo ba tài khoản ban đầu; chạy lại không đặt lại mật khẩu tài khoản đã có.

`scripts/activate_selected_model.py` đăng ký bản 182 biến, bổ sung điểm còn thiếu
và cập nhật metadata hoạt động. Đây là thao tác ghi database/artifact, chỉ dùng
khi cần chuyển phiên bản; mở web hoặc chạy notebook không tự thực hiện thao tác này.

## Cache và phiên đăng nhập

Ứng dụng chuẩn bị báo cáo tổng quan ở luồng nền khi chạy `web/app.py`.
Cache dữ liệu nghiên cứu nằm ở `tmp/dashboard_research_cache/`; báo cáo tổng quan
và phân khúc còn giữ tối đa 16 context theo phiên bản dữ liệu, đường dẫn và bộ lọc
trong bộ nhớ. Tài khoản, session, ghi chú và trạng thái tác nghiệp không được lưu
trong cache báo cáo. Đổi `dataset_metadata.data_version` khi thay snapshot nghiên cứu
và khởi động lại Flask sau khi sửa Python.

CSS/JavaScript được gắn phiên bản theo nội dung; Plotly được phục vụ từ gói cài
cục bộ. Có thể đặt `FLASK_SECRET_KEY` để giữ khóa phiên qua các lần khởi động;
nếu không, ứng dụng tạo khóa mới mỗi lần chạy và phiên đăng nhập cũ mất hiệu lực.
