# 🍃 Tea Production Optimization using Gurobi

Dự án áp dụng mô hình Toán học (Quy hoạch Tuyến tính) và bộ giải Gurobi để tối ưu hóa kế hoạch sản xuất tại xưởng chế biến chè truyền thống.

## 1. Bối Cảnh & Vấn Đề Kinh Doanh

Nghề chế biến chè truyền thống không chỉ đòi hỏi kinh nghiệm mà còn là một bài toán tối ưu hóa nguồn lực đầy thách thức. Trong quá trình vận hành thực tế, xưởng sản xuất luôn phải đối mặt với bài toán kiểm soát chất lượng và rủi ro hao hụt theo sự phân cấp rõ rệt:

* **Loại 1**: Thành phẩm cao cấp, mang lại giá trị lớn nhất nhưng có yêu cầu khắt khe về định lượng để đáp ứng đúng các đơn đặt hàng VIP.
* **Loại 2**: Các sản phẩm hàng công nghiệp, thường được bán buôn với số lượng lớn.
* **Loại 3**: Phế phẩm từ khâu nhặt/sàng được gom thành **Loại 3** để vớt vát chi phí.

Bên cạnh đó, năng lực sản xuất của xưởng bị chi phối mạnh mẽ bởi các rào cản hạ tầng theo thời gian:

* **Ca ngày (Điều kiện lý tưởng)**: Lưới điện ổn định, nhân sự đầy đủ, cho phép xưởng vận hành tối đa công suất với tỷ lệ lỗi thấp.
* **Ca tối (Điều kiện rủi ro)**: Tình trạng sụt áp lưới điện và thiếu hụt nhân sự buộc xưởng phải giảm tải máy móc để tránh cháy nổ, kéo theo tỷ lệ rớt hạng sản phẩm tăng cao.

**Mục tiêu:** Thoát khỏi phương pháp lên kế hoạch "cảm tính". Dự án ứng dụng mô hình toán học để tính toán chính xác lượng chè tươi nạp vào từng máy, từng ca nhằm Tối đa hóa lợi nhuận, cam kết trả đủ đơn hàng VIP đúng hạn và tuyệt đối không làm quá tải hệ thống điện.

---

## 2. Mô Hình Toán Học (Mathematical Model)

Bài toán được mã hóa thành một bài Quy hoạch Tuyến tính (Linear Programming) với hai biến quyết định, phản ánh đúng hai ca sản xuất thực tế của xưởng mỗi ngày.

---

### 2.1 Tham Số Đầu Vào (Input Parameters)

**Đơn hàng & Nguyên liệu**

| Ký hiệu | Ý nghĩa | Ví dụ |
|:-------:|---------|:-----:|
| $D_{VIP}$ | Kg chè Loại 1 khách VIP đặt | 20 kg |
| $D_{Merchant}$ | Kg chè Loại 1 thương lái đặt | 20 kg |
| $k$ | Hệ số hao hụt, chuyển đổi tươi → khô (kg tươi / 1 kg khô) | 4.5 |

**Thời gian & Năng lực sản xuất**

| Ký hiệu | Ý nghĩa |
|:-------:|---------|
| $T_1$ | Tổng giờ làm việc ca bình thường (điện khỏe) |
| $T_2$ | Tổng giờ làm việc ca cao điểm (điện yếu) |
| $C_1,\ C_2$ | Công suất tối đa tại $T_1$ và $T_2$ (kg chè tươi/giờ) |

**Chi phí & Giá bán**

| Ký hiệu | Ý nghĩa |
|:-------:|---------|
| $n_1,\ n_2$ | Số thợ bố trí ở ca 1 và ca 2 (người) |

**Tiền công thợ**

| Ký hiệu | Ý nghĩa | Đơn vị | Giá trị |
|:-------:|---------|:-----:|:-----:|
| $W_{wage}$ | Tiền công thợ theo mỗi ca | VNĐ/ca/người | 300.000 - 450.000 |

**Năng suất lao động**

| Ký hiệu | Ý nghĩa | Đơn vị | Giá trị |
|:-------:|---------|:-----:|:-----:|
| $a_1$ | Năng suất của 1 thợ ở ca 1, tức số kg chè tươi xử lý được trong 1 buổi | kg chè tươi/ca/người | nhập theo thực tế |
| $a_2$ | Năng suất của 1 thợ ở ca 2, tức số kg chè tươi xử lý được trong 1 buổi | kg chè tươi/ca/người | nhập theo thực tế |

**Giá bán chè**

| Ký hiệu | Ý nghĩa | Đơn vị | Giá trị |
|:-------:|---------|:-----:|:-----:|
| $P_1$ | Giá bán chè Loại 1 | VNĐ/kg | 95.000 |
| $P_2$ | Giá bán chè Loại 2 | VNĐ/kg | 37.000 |
| $P_3$ | Giá bán chè Loại 3 | VNĐ/kg | 8.000 |

**Nhu cầu đầu ra**

| Ký hiệu | Ý nghĩa | Đơn vị | Giá trị |
|:-------:|---------|:-----:|:-----:|
| $D_1$ | Nhu cầu chè khô Loại 1 cần giao | kg | nhập theo đơn |
| $D_2$ | Nhu cầu chè khô Loại 2 cần giao | kg | nhập theo đơn |

**Biểu giá điện EVN (áp dụng theo cấp điện áp)**

| Cấp điện áp | Giờ bình thường (đồng/kWh) | Giờ thấp điểm (đồng/kWh) | Giờ cao điểm (đồng/kWh) |
|:-----------:|:---------------------------:|:------------------------:|:----------------------:|
| $\ge 110$ kV | 1.728 | 1.094 | 3.141 |
| 22 kV – dưới 110 kV | 1.749 | 1.136 | 3.242 |
| 6 kV – dưới 22 kV | 1.812 | 1.178 | 3.348 |
| Dưới 6 kV | 1.896 | 1.241 | 3.474 |

> `e_1` và `e_2` được hiểu là chi phí điện đơn vị cho mỗi kg chè tươi xử lý ở ca 1 và ca 2, được quy đổi từ biểu giá EVN ở trên kết hợp với mức tiêu thụ điện thực tế của máy.
> 
> Link: https://www.evn.com.vn/d/vi-VN/news/Bieu-gia-ban-le-dien-theo-Quyet-dinh-so-1279QD-BCT-ngay-0952025-cua-Bo-Cong-Thuong-60-28-502668?utm_source=chatgpt.com

**Hệ số rủi ro chất lượng (Risk Factors)**

> Mỗi ca sản xuất đều có rủi ro riêng; dù vận hành cẩn thận đến đâu thì vẫn có thể gặp sự cố hoặc hao hụt ngẫu nhiên, nên mô hình tách riêng rủi ro theo từng ca và từng hướng rớt hạng:
> - `rd_ca1_12`: tại ca 1, mẻ chủ đích làm Loại 1 bị rớt xuống Loại 2
> - `rd_ca1_23`: tại ca 1, mẻ chủ đích làm Loại 2 bị rớt xuống Loại 3
> - `rd_ca2_12`: tại ca 2, mẻ chủ đích làm Loại 1 bị rớt xuống Loại 2
> - `rd_ca2_23`: tại ca 2, mẻ chủ đích làm Loại 2 bị rớt xuống Loại 3

| Ký hiệu | Ý nghĩa | Đơn vị | Giá trị |
|:-------:|---------|:-----:|:-----:|
| $rd_{ca1\_12}$ | Tỷ lệ mẻ chè chủ đích làm Loại 1 bị rớt xuống Loại 2 ở ca 1 | % | 2% |
| $rd_{ca1\_23}$ | Tỷ lệ mẻ chè chủ đích làm Loại 2 bị rớt xuống Loại 3 ở ca 1 | % | 1% |
| $rd_{ca2\_12}$ | Tỷ lệ mẻ chè chủ đích làm Loại 1 bị rớt xuống Loại 2 ở ca 2 | % | 8% |
| $rd_{ca2\_23}$ | Tỷ lệ mẻ chè chủ đích làm Loại 2 bị rớt xuống Loại 3 ở ca 2 | % | 12% |

---

### 2.2 Biến Quyết Định (Decision Variables)

Lúc này, người điều hành có **6 quyết định** cần đưa ra mỗi ngày: 4 biến phân bổ nguyên liệu cho 2 ca và 2 biến nhân công cho 2 ca.

> **Vì sao có thêm 2 biến nhân công?** Vì nếu muốn bài toán tự chọn số người tối thiểu cần dùng, thì số thợ ở mỗi ca không còn là dữ liệu cố định nữa mà trở thành biến quyết định để model tối ưu chi phí.

$$nl\_ca1\_l1 \ge 0 \quad \text{— kg chè tươi vào ca 1, chủ đích làm Loại 1}$$

$$nl\_ca2\_l1 \ge 0 \quad \text{— kg chè tươi vào ca 2, chủ đích làm Loại 1}$$

$$nl\_ca1\_l2 \ge 0 \quad \text{— kg chè tươi vào ca 1, chủ đích làm Loại 2}$$

$$nl\_ca2\_l2 \ge 0 \quad \text{— kg chè tươi vào ca 2, chủ đích làm Loại 2}$$

$$n_1 \in \mathbb{Z}_{\ge 0} \quad \text{— số thợ bố trí ở ca 1}$$

$$n_2 \in \mathbb{Z}_{\ge 0} \quad \text{— số thợ bố trí ở ca 2}$$

---

### 2.3 Tính Toán Đầu Ra (Output Computations)

Gọi:

$$x_1 = nl\_ca1\_l1,\quad x_2 = nl\_ca2\_l1,\quad x_3 = nl\_ca1\_l2,\quad x_4 = nl\_ca2\_l2$$

Kế hoạch thu mua:

$$W_{buy} = x_1 + x_2 + x_3 + x_4$$

Sản lượng đầu ra:

$$Q_1 = \frac{x_1(1-rd_{ca1\_12}) + x_2(1-rd_{ca2\_12})}{k}$$

$$Q_2 = \frac{x_1 rd_{ca1\_12} + x_3(1-rd_{ca1\_23}) + x_2 rd_{ca2\_12} + x_4(1-rd_{ca2\_23})}{k}$$

$$Q_3 = \frac{x_3 rd_{ca1\_23} + x_4 rd_{ca2\_23}}{k}$$

Chi phí:

$$Cost_{labor} = (n_1 + n_2)\cdot W_{wage}$$

$$Cost_{electric} = e_1(x_1+x_3) + e_2(x_2+x_4)$$

$$Cost_{total} = Cost_{labor} + Cost_{electric}$$

Doanh thu và lợi nhuận:

$$Revenue = P_1Q_1 + P_2Q_2 + P_3Q_3$$

$$Profit = Revenue - Cost_{total}$$

---

### 2.4 Hệ Ràng Buộc Kỹ Thuật (Constraints)

Hệ thống có hai luồng sản xuất song song (luồng `l1` — chủ đích Loại 1, luồng `l2` — chủ đích Loại 2), cùng chia sẻ tải của máy theo từng khung giờ.

**(C1) Công suất máy theo khung giờ** — Tổng nguyên liệu đưa vào mỗi ca (bất kể chủ đích loại nào) không vượt tải máy:

$$x_1 + x_3 \le C_1T_1$$

$$x_2 + x_4 \le C_2T_2$$

**(C2) Năng lực nhân công** — Khối lượng xử lý của mỗi ca không vượt năng suất theo số thợ bố trí:

$$x_1 + x_3 \le a_1n_1$$

$$x_2 + x_4 \le a_2n_2$$

**(C3) Đáp ứng nhu cầu đầu ra** — Sản lượng loại 1 và loại 2 phải đủ yêu cầu đặt trước:

> `D_1` và `D_2` được hiểu là kg chè khô thành phẩm.

$$Q_1 \ge D_1$$

$$Q_2 \ge D_2$$

**(C4) Điều kiện thực tế** — Mọi biến phân bổ và số thợ không âm:

$$x_1, x_2, x_3, x_4 \ge 0,\quad n_1, n_2 \in \mathbb{Z}_{\ge 0}$$

> **Cơ chế tự động:** Gurobi sẽ tự cân đối hai luồng. Nếu phần lợi nhuận biên của luồng Loại 2 không đủ tốt, mô hình có thể giảm hoặc bỏ luồng này; nếu có lợi, mô hình sẽ phân bổ thêm nguyên liệu vào luồng đó.

---

### 2.5 Hàm Mục Tiêu (Objective Function)

Tìm $x_1, x_2, x_3, x_4, n_1, n_2$ sao cho lợi nhuận trong ngày là lớn nhất:

$$\max \; Profit = Revenue - Cost_{total}$$

---

## 3. Cài Đặt & Chạy Thử (How to run)

Dự án sử dụng Python và bộ giải `gurobipy`.

**Bước 1: Clone repository**
```bash
git clone [https://github.com/nguynninh/tea-optimization.git](https://github.com/nguynninh/tea-optimization.git)
cd tea-optimization
```

**Bước 2: Cài đặt thư viện**

```bash
pip install gurobipy
```

> **Lưu ý:** Bạn cần có license của Gurobi để chạy các bài toán cỡ lớn, tuy nhiên với bài toán demo này, bản dùng thử/academic mặc định là đủ.

**Bước 3: Chạy chương trình**

```bash
python main.py
```
