# Lựa chọn đặc trưng bằng Filter

Ngày 28/10/2026. Đối chiếu phương pháp với notebook Data Mining: Han et al., mục 7.1 về lựa chọn đặc trưng; Kele Xu, mục 2.4 về variance/correlation và các nhóm phương pháp chọn biến.

## Phương pháp

- Đầu vào: bộ B, 199 biến gồm 183 biến số và 16 biến phân loại; 184.506 hồ sơ train.
- Bỏ cột hằng, tính cả trạng thái thiếu. Không dùng ngưỡng near-zero variance để loại cờ hiếm.
- Tính Pearson giữa các biến số. Chỉ xét cặp có ít nhất 50% hồ sơ fit quan sát được cả hai giá trị.
- Khi |r| ≥ 0,90, ưu tiên biến ít thiếu hơn; nếu bằng nhau, giữ theo thứ tự schema.
- Biến phân loại được giữ trừ khi cột hằng trong phần fit.

Ngưỡng 0,90, mức quan sát chung 50% và quy tắc ưu tiên trên là thiết kế của nghiên cứu, không phải yêu cầu bắt buộc của giáo trình. Selector không nhận TARGET.

## Kết quả lọc

| Phạm vi fit selector | Đầu vào | Giữ lại | Loại |
|---|---:|---:|---:|
| Train của fold 0 | 199 | 181 | 18 |
| Train của fold 1 | 199 | 181 | 18 |
| Train của fold 2 | 199 | 181 | 18 |
| Toàn bộ train để chuẩn bị lần fit cuối | 199 | 182 | 17 |

Danh sách giữa các fold có khác nhau. Mỗi thuật toán trong cùng một fold dùng chung danh sách do phần fit của fold đó tạo ra. Danh sách fit trên toàn train không được dùng ngược lại để đánh giá các fold.

Bộ fit toàn train có **166 biến số và 16 biến phân loại**. Không có cột hằng bị loại; 17 cột bị loại theo quy tắc tương quan.

- [Danh sách 182 biến trên toàn train](final_selected_features_train_only.json)
- [Bảng biến được giữ và kiểu dữ liệu](selected_features_train_only.csv)
- [Schema rút gọn để dùng ở bước huấn luyện cuối](selected_schema_train_only.json)
- [Biến bị loại, biến được giữ thay thế và hệ số tương quan](final_dropped_features_train_only.csv)
- [Danh sách riêng từng fold](selected_features_by_fold.json)
- [Lý do loại biến theo fold](dropped_features_by_fold.csv)
- [Notebook thực hiện](../../../notebooks/05_feature_selection.ipynb)

## Bàn giao

Feature Selection đã hoàn tất, giữ 181 biến/fold và 182 biến toàn train. Notebook 06 đã đánh giá đủ 63 lượt CV, notebook 07 đã fit và đánh giá model cuối, notebook 08 đã giải thích mô hình.

- [Kết quả CV](../feature_selection_redo_20261029/results.md).
- [Đánh giá mô hình](../selected_model_evaluation_20261030/results.md).
- [Quyết định chốt CatBoost 182 biến](../selected_model_evaluation_20261030/project_model_decision.md).
