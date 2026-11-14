# Đánh giá khả năng hỗ trợ rà soát: điểm số, decile và năng lực

Ngày 26/10/2026. Phạm vi đã xác nhận qua trao đổi: hỗ trợ thẩm định viên ưu tiên rà soát hồ sơ hiện tại. Không tự duyệt/từ chối, khóa thẻ, gọi điện hoặc nhắn nhắc nợ.

## Kết luận từ validation của model đang hoạt động

CatBoost có khả năng làm tập trung TARGET=1 vào nhóm điểm cao trong tập validation. Đây là bằng chứng về xếp hạng nội bộ, chưa là chứng nhận sẵn sàng vận hành ngân hàng. Validation đã dùng chọn ngưỡng nên không phải tập độc lập cho chỉ số tại ngưỡng.

| Phạm vi rà soát | Số hồ sơ | TARGET=1 tìm thấy | Cảnh báo TARGET=0 | TARGET=1 bỏ sót | Precision | Recall | Lift so với tỷ lệ dương toàn tập |
|---|---:|---:|---:|---:|---:|---:|---:|
| Top 1% | 616 | 310 | 306 | 4.655 | 50,32% | 6,24% | 6,23 |
| Top 5% | 3.076 | 1.097 | 1.979 | 3.868 | 35,66% | 22,09% | 4,42 |
| Top 10% | 6.151 | 1.783 | 4.368 | 3.182 | 28,99% | 35,91% | 3,59 |
| Top 20% | 12.301 | 2.724 | 9.577 | 2.241 | 22,14% | 54,86% | 2,74 |
| Ngưỡng hiện hành 14,841034% | 8.828 | 2.255 | 6.573 | 2.710 | 25,54% | 45,42% | 3,16 |

Mỗi dòng là một chính sách riêng trên cùng 61.502 hồ sơ, 4.965 hồ sơ TARGET=1. Các kịch bản top-k chỉ mô tả năng lực; chưa thay threshold/model đang phục vụ. Top-k phá hòa theo score giảm dần rồi SK_ID_CURR tăng dần.

Nhóm dưới ngưỡng hiện hành vẫn có 2.710/52.674 = **5,14% TARGET=1**; không gọi là nhóm rất an toàn. Thấp điểm không tự là căn cứ phê duyệt hoặc giản lược quy trình thẩm định.

## Đọc đúng các mẫu số

- 1 − Precision = 74,46%: tỷ lệ TARGET=0 **trong số hồ sơ bị cảnh báo**, thường gọi false discovery rate. Không phải 74,46% toàn bộ hồ sơ đều bị báo nhầm.
- False positive rate = FP/(FP+TN) = **11,63%**: tỷ lệ bị cảnh báo trong các hồ sơ TARGET=0.
- 1 − Recall = **54,58%**: tỷ lệ số hồ sơ TARGET=1 bị bỏ sót; không đồng nghĩa tỷ lệ tổn thất tài chính bị bỏ sót.
- Precision phụ thuộc năng lực xếp hạng, prevalence và điểm cắt. Mất cân bằng ảnh hưởng precision nhưng không làm precision 20–30% trở thành kết quả tất yếu hoặc chuẩn chấp nhận chung.

Định nghĩa metric: [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall), [scikit-learn Precision–Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html).

## Bảng phân tầng thật thay cho ví dụ minh họa

[deciles.csv](deciles.csv) chứa 10 nhóm xấp xỉ bằng nhau, D1 cao điểm nhất. Tỷ lệ TARGET=1 lần lượt khoảng **28,99%; 15,30%; 10,15%; 8,39%; 5,33%; 4,13%; 3,17%; 2,42%; 1,85%; 0,99%**. Top 30% tích lũy tìm thấy 67,43% hồ sơ TARGET=1 trên validation này.

Không gán hành động tín dụng tự động cho từng decile. Các nhóm này là lát cắt của xếp hạng hiện tại, không phải risk bands được một tổ chức tài chính thẩm định và phê duyệt.

Ví dụ “10% hồ sơ có 65% dương và 20% tiếp theo có 30% dương” đã đòi hỏi ít nhất 12,5% dương trên toàn tập. Nó không thể đồng thời mô tả cohort này có 8,07% dương. Không dùng các số minh họa như kết quả dự án.

## Test nội bộ lịch sử sau khi chốt finalist

Đã chốt giữ full B trước khi đọc test trong đợt này. Trên 61.503 hồ sơ test lịch sử,
CatBoost đạt AP **0,281933**, ROC-AUC **0,781842**, Precision **26,48%**, Recall
**45,78%**, alert rate **13,96%** tại ngưỡng giữ nguyên. Còn 2.692 FN và 6.311 FP.

| Phạm vi rà soát trên test lịch sử | Precision | Recall | TARGET=1 tìm thấy |
|---|---:|---:|---:|
| Top 1% | 54,06% | 6,71% | 333 |
| Top 5% | 37,29% | 23,10% | 1.147 |
| Top 10% | 29,95% | 37,10% | 1.842 |
| Top 20% | 22,91% | 56,76% | 2.818 |

Đây vẫn là test từng được xem khi nghiên cứu LR, không phải một phép kiểm định
độc lập mới. Những dòng này không dùng để đổi model, chọn threshold hoặc gán
hành động tín dụng. Hai hàng biểu đồ trong PNG tách validation và test lịch sử.

## Đối chiếu các phát biểu bên ngoài

- Đội giải nhất Home Credit tự báo cáo CV AUC 0,80657, public 0,80828 và private 0,80570 trong [bài viết của đội](https://www.kaggle.com/c/home-credit-default-risk/discussion/64480). Không gộp các tập này thành một khoảng private 0,806–0,812. Trang leaderboard cần JavaScript; giá trị ở đây được dẫn đúng là đội tự báo cáo.
- Điểm private Kaggle và validation của dự án không phải cùng phép thử; không suy ra mức “gần chuẩn ngân hàng” bằng cách trừ hai điểm AUC.
- [arXiv:2106.07954v3](https://arxiv.org/html/2106.07954v3) nghiên cứu dữ liệu SBA doanh nghiệp nhỏ tại Mỹ; nguồn này không chứng minh decile Home Credit của dự án có precision 60–70%.
- Dự án đã có threshold tuning validation theo phạt giả định 5:1; chưa được phép đồng nhất giảm điểm phạt với tiền tiết kiệm. Cần xác định tổn thất, nguồn lực, thời gian và kết quả can thiệp thực để đánh giá tài chính.

## Muốn kết luận dùng thực tế cần bổ sung gì?

Phải làm rõ cohort/thời điểm dùng, outcome/horizon phù hợp, dữ liệu mới, baseline quy trình hiện hành, số hồ sơ có thể rà soát, chi phí và kết quả can thiệp, cùng thẩm định độc lập phù hợp. Một AUC hoặc lift đơn lẻ không xác nhận các điều kiện đó.

Định hướng quản trị model có thể tham khảo [hướng dẫn quản trị rủi ro mô hình sửa đổi của Fed ngày 17/04/2026](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm). Đây là nguồn tham khảo về validation/monitoring/outcomes analysis, không phải bằng chứng project đã tuân thủ yêu cầu pháp lý hay quy trình ngân hàng tại Việt Nam.

Theo dõi PSI/phân phối chỉ giúp nhận biết thay đổi đầu vào hoặc điểm. Muốn biết Precision/Recall/calibration còn tốt phải có outcome đủ điều kiện. Kế hoạch cụ thể: đánh giá lại sau vận hành.

## Minh chứng và biểu đồ

- [Precision–Recall, Cumulative Gains và deciles](pr_gains_deciles.png).
- [Capacity](capacity.csv), [deciles](deciles.csv), [metric tại ngưỡng cố định](fixed_threshold_metrics.csv), [đối soát mẫu số](verification.json).
- Dự đoán validation lấy từ báo cáo đúng model/metadata đang hoạt động. Biểu đồ/CSV đã bổ sung riêng finalist trên test lịch sử sau khi chốt; không dùng test để chọn model/điểm cắt.
