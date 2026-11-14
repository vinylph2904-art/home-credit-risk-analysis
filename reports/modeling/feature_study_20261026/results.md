# Ablation, chọn đặc trưng và đánh giá model đã chốt

Ngày 26/10/2026. Giữ nguyên model B đầy đủ đang hoạt động. Các phương án rút gọn chưa vượt đủ gate đã công bố.

## Thiết kế và phạm vi

Đợt bổ sung được người dùng đồng ý sau khi test LR lịch sử đã được xem. Protocol
được ghi trước khi fit mới, không mô tả là thí nghiệm có trước lần xem test đó.
Giữ CatBoost depth6/500 iterations/seed42/raw probability và ba fold train.
Không early stopping, không đổi hyperparameter, không dùng validation/test để
chọn danh sách feature trong CV. Model web, input 199 cột và metadata hiện hành
được giữ nguyên trong đợt nghiên cứu.

Đã tạo 30 checkpoint fit CV mới: ba full-B để học ranking trong từng outer-fit,
ba top150 và 24 lượt bỏ nhóm nguồn/cờ/lịch sử. Ba fold A127 được reuse từ đợt
boosting cùng dữ liệu/fold/settings; ghi riêng, không gọi là fit mới. Có
0 fit ứng viên cuối bổ sung trên toàn train.
Thời gian lượt thực thi đầu: 64.4 phút.

## 1. Kết quả CV cặp theo cùng fold

| Phương án | Số feature | Mean AP | Std AP (3 fold) | Delta AP so full B | Mean Brier | Đủ gate CV để thay full B? |
|---|---:|---:|---:|---:|---:|---|
| B đầy đủ | 199 | 0.269328 | 0.000637 | +0.000000 | 0.06655722 | Đối chứng |
| Chọn 150 biến trong từng fold | 150 | 0.269476 | 0.001215 | +0.000148 | 0.06654692 | Không |
| Bỏ Bureau và cờ | 184 | 0.263571 | 0.001919 | -0.005757 | 0.06680018 | Không |
| Bỏ Bureau Balance và cờ | 188 | 0.269253 | 0.001151 | -0.000075 | 0.06656039 | Không |
| Bỏ hồ sơ vay trước và cờ | 188 | 0.266736 | 0.001690 | -0.002593 | 0.06668849 | Không |
| Bỏ POS và cờ | 189 | 0.268090 | 0.002030 | -0.001238 | 0.06662947 | Không |
| Bỏ thẻ tín dụng và cờ | 185 | 0.266056 | 0.001034 | -0.003272 | 0.06669949 | Không |
| Bỏ lịch sử trả góp và cờ | 188 | 0.265576 | 0.001613 | -0.003752 | 0.06675155 | Không |
| Bỏ 6 cờ, giữ lịch sử | 193 | 0.268789 | 0.000749 | -0.000540 | 0.06656407 | Không |
| Bỏ 66 biến lịch sử, giữ 6 cờ | 133 | 0.241157 | 0.001359 | -0.028172 | 0.06790895 | Không |
| A: chỉ hồ sơ hiện tại (reuse CV) | 127 | 0.241262 | 0.002252 | -0.028067 | 0.06791452 | Không |

Mean AP cao nhất quan sát được: **Chọn 150 biến trong từng fold**
(0.269476). Gate không chỉ nhìn giá trị lớn nhất: AP tăng ít nhất
0,001, ít nhất 2/3 fold không giảm, không fold nào giảm quá 0,003 và Brier không
tăng quá 0,0005. Các biên này là tiêu chí nghiên cứu đã công bố, không phải
ngưỡng nghiệp vụ hay kiểm định ý nghĩa thống kê.

Các nguồn có phụ thuộc: Bureau Balance được chuẩn bị qua bureau; thiếu nguồn
cũng thể hiện qua counts/NaN. Bỏ một nhóm chỉ đo hiệu ứng có điều kiện khi giữ
các nhóm còn lại; không là đóng góp nhân quả hoặc độc lập tuyệt đối.

## 2. Thử chọn 150 biến

Trong mỗi fold, full model chỉ fit trên hai fold train; dùng
PredictionValuesChange của model đó để xếp hạng, chọn150 rồi refit trên cùng
phần train. Fold probe chỉ dùng đánh giá. Không dùng importance của model đã
fit cả train để chọn biến cho các probe trong CV.

Top150 có mean AP 0.269476, so full B 0.269328;
delta +0.000148. Jaccard giữa các tập chọn theo fold:
0.829, 0.807, 0.840. Danh sách feature có
thể khác giữa các fold; đây là đánh giá một procedure chọn biến, không giả
định đã có một subset150 bất biến ngay từ đầu.

Xem [tần suất được chọn](selection_frequency.csv), [độ ổn định](selection_stability.csv),
[danh sách theo fold](selected_features_by_fold.json). Thời gian fit/predict CV
chỉ là số đo trên máy hiện tại; dữ liệu A reuse thuộc lượt chạy cũ nên không
dùng chênh thời gian đó để tuyên bố hơn/kém tốc độ triển khai.

## 3. Quyết định trước test

Ứng viên CV: **full_B**. Gate validation:
**không kích hoạt đổi model**.
Finalist: **full_B**, 199 feature,
threshold **0.14841034110254**, raw probability.

Gate validation yêu cầu cost5:1 giảm so active, AP không giảm quá0,001,
Brier không tăng quá0,0005 và alert rate không tăng quá2 điểm phần trăm.
Đây là điều kiện của study để hạn chế đổi model vì cải thiện nhỏ, chưa phải
SLA/capacity hay chi phí được một ngân hàng xác nhận.

Quyết định và hash được lưu trong [final_decision_before_test.json](final_decision_before_test.json)
trước khi SELECT test labels. Nếu đã có test output đúng hash thì chỉ đọc
output đó khi replay, không chọn lại hoặc fit lại theo kết quả test.

## 4. Test nội bộ lịch sử của finalist

| Chỉ số | Giá trị |
|---|---:|
| Hồ sơ / TARGET=1 | 61,503 / 4,965 |
| AP | 0.281933 |
| ROC-AUC | 0.781842 |
| Brier | 0.06600079 |
| Precision | 26.48% |
| Recall | 45.78% |
| F1 | 0.335523 |
| Alert rate | 13.96% |
| TN / FP / FN / TP | 50,227 / 6,311 / 2,692 / 2,273 |
| Điểm phạt giả định 5FN+FP trên hồ sơ | 0.321464 |

Đây là test đã được đánh giá ở giai đoạn LR trước nghiên cứu boosting/feature,
không phải holdout độc lập mới. Không thay model hoặc điểm cắt sau bảng này.
Phạt5:1 không là tiền tiết kiệm; FN là số hồ sơ, không phải tỷ lệ giá trị tổn thất.

## 5. Đã ổn chưa, khi nào quay lại preprocessing?

Finalist **đạt**
các benchmark demo đã công bố trên validation: AP vượt prevalence, ROC vượt
ngẫu nhiên, cost giả định thấp hơn không cảnh báo và LR đóng băng. Kết luận
đó chỉ là so sánh nghiên cứu; còn bỏ sót 54.58%
hồ sơ TARGET=1 ở validation và chưa có tiêu chí năng lực/chi phí thực tế.

Nếu benchmark hoặc yêu cầu nghiệp vụ phù hợp chưa đạt, quay lại chẩn đoán
missing/sentinel, coverage nguồn, mốc thời gian và thiết kế feature trên train;
ghi một protocol sửa trước vòng thí nghiệm mới. Không mặc định phải xóa outlier,
SMOTE hoặc đổi thuật toán. Không dùng test lịch sử để tối ưu vòng tiếp theo.

Xem quy trình đánh giá lại
và [đánh giá theo ngân sách/decile](../operational_assessment_20261026/results.md).
Hệ thống hỗ trợ xếp thứ tự rà soát, chưa tự duyệt/từ chối hoặc nhắc nợ tự động.

## Minh chứng

- [Protocol](protocol.json), [CV từng fold](cv_folds.csv), [CV summary](cv_summary.csv),
  [CV decision](cv_decision.json), [validation](validation_comparison.csv).
- [Test metrics](historical_test_metrics.csv), [test capacity](historical_test_capacity.csv),
  [biểu đồ](feature_study_summary.png), [execution](execution.json).
- Notebook thực nghiệm gốc, mục18;
  [HomeCreditTraining](../../../models/HomeCreditTraining.py).
- Chọn feature trong fold theo nguyên tắc chống leakage của
  [scikit-learn](https://scikit-learn.org/stable/common_pitfalls), importance theo
  [CatBoost](https://catboost.ai/docs/en/concepts/python-reference_catboost_get_feature_importance).
