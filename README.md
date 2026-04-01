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
| $n_1,\ n_2$ | Số thợ làm việc ở ca 1 và ca 2 (người) |
| $W_{wage}$ | Tiền công thợ (VNĐ/giờ/người) |
| $E_1,\ E_2$ | Chi phí điện/vận hành máy ở ca 1 và ca 2 (VNĐ/giờ) |
| $P_1,\ P_2,\ P_3$ | Giá bán chè Loại 1, Loại 2, Loại 3 (VNĐ/kg) |

**Hệ số rủi ro chất lượng (Risk Factors)**

> Tại ca $T_1$ (điện khỏe): Máy chạy chuẩn — chủ đích làm Loại 1 ra 100% Loại 1, chủ đích làm Loại 2 ra 100% Loại 2.
> Tại ca $T_2$ (điện yếu / sụt áp): Lỗi sụt áp khiến chè rớt hạng theo **bậc thang** — mẻ đang cố làm Loại 1 rớt xuống Loại 2, mẻ đang cố làm Loại 2 rớt xuống Loại 3.

| Ký hiệu | Ý nghĩa |
|:-------:|---------|
| $r_{12}$ | Tỷ lệ mẻ chè chủ đích làm Loại 1 bị rớt xuống Loại 2 tại ca $T_2$ |
| $r_{23}$ | Tỷ lệ mẻ chè chủ đích làm Loại 2 bị rớt xuống Loại 3 tại ca $T_2$ |

---

### 2.2 Biến Quyết Định (Decision Variables)

Lúc này, người điều hành có **4 quyết định** cần đưa ra mỗi ngày — không chỉ phân bổ theo ca, mà còn xác định rõ chủ đích sản xuất của từng luồng:

$$x_1 \ge 0 \quad \text{— kg chè tươi vào ca } T_1 \text{, chủ đích làm Loại 1}$$

$$x_2 \ge 0 \quad \text{— kg chè tươi vào ca } T_2 \text{, chủ đích làm Loại 1}$$

$$y_1 \ge 0 \quad \text{— kg chè tươi vào ca } T_1 \text{, chủ đích làm Loại 2}$$

$$y_2 \ge 0 \quad \text{— kg chè tươi vào ca } T_2 \text{, chủ đích làm Loại 2}$$

---

### 2.3 Tính Toán Đầu Ra (Output Computations)

#### A. Kế Hoạch Thu Mua (Purchasing Plan)

Thay vì bị giới hạn bởi kho chứa sẵn có, hệ thống tính ngược ra đúng lượng nguyên liệu cần đi mua cho ngày hôm đó — không thừa, không thiếu:

$$W_{buy} = x_1 + x_2 + y_1 + y_2$$

#### B. Báo cáo Sản lượng

Chè khô Loại 1 — thu từ các mẻ **chủ đích Loại 1** (ca $T_1$ đạt 100%; ca $T_2$ trừ phần rớt hạng):

$$Q_1 = \frac{x_1}{k} + \frac{x_2}{k} \cdot (1 - r_{12})$$

Chè khô Loại 2 — gồm từ **2 nguồn**: mẻ chủ đích Loại 2 thành công + mẻ Loại 1 bị rớt hạng tại ca $T_2$:

$$Q_2 = \frac{y_1}{k} + \frac{y_2}{k} \cdot (1 - r_{23}) + \frac{x_2}{k} \cdot r_{12}$$

Chè khô Loại 3 — phế phẩm sinh ra **chỉ khi** mẻ Loại 2 bị rớt hạng tại ca $T_2$:

$$Q_3 = \frac{y_2}{k} \cdot r_{23}$$

Tổng sản lượng chè khô:

$$Q_{total} = Q_1 + Q_2 + Q_3$$

#### C. Báo cáo Chi phí

Tổng tiền nhân công:

$$Cost_{labor} = (n_1 \cdot T_1 + n_2 \cdot T_2) \cdot W_{wage}$$

Tổng tiền điện và vận hành máy:

$$Cost_{electric} = E_1 \cdot T_1 + E_2 \cdot T_2$$

Tổng chi phí sản xuất trong ngày:

$$Cost_{total} = Cost_{labor} + Cost_{electric}$$

#### D. Báo cáo Tài chính

Doanh thu dự kiến:

$$Revenue = Q_1 \cdot P_1 + Q_2 \cdot P_2 + Q_3 \cdot P_3$$

Lợi nhuận ròng:

$$Profit = Revenue - Cost_{total}$$

---

### 2.4 Hệ Ràng Buộc Kỹ Thuật (Constraints)

Hệ thống có hai luồng sản xuất song song (luồng $x$ — chủ đích Loại 1, luồng $y$ — chủ đích Loại 2), cùng chia sẻ tải của máy theo từng khung giờ.

**(C1) Đáp ứng đơn hàng** — Tổng Loại 1 thực thu (sau khi khấu trừ rờt hạng) phải đủ giao khách:

$$\frac{x_1}{k} + \frac{x_2}{k} \cdot (1 - r_{12}) \ge D_{VIP} + D_{Merchant}$$

**(C2) Công suất máy theo khung giờ** — Tổng nguyên liệu đưa vào mỗi ca (bất kể chủ đích loại nào) không vượt tải máy:

$$x_1 + y_1 \le C_1 \cdot T_1$$

$$x_2 + y_2 \le C_2 \cdot T_2$$

**(C3) Điều kiện thực tế** — Mọi biến phân bổ không âm:

$$x_1,\ x_2,\ y_1,\ y_2 \ge 0$$

> **Cơ chế tự động:** Gurobi sẽ tự cân đối hai luồng. Nếu phần lỗi $r_{12}$ từ luồng $x_2$ đã đủ đảm bảo lợi nhuận từ Loại 2, nó có thể đặt $y = 0$ hoàn toàn. Chỉ khi đơn Loại 2 có giá cạnh tranh đủ hấp dẫn, luồng $y$ mới được đẩy lên.

---

### 2.5 Hàm Mục Tiêu (Objective Function)

Tìm $x_1,\ x_2,\ y_1,\ y_2$ sao cho lợi nhuận trong ngày đạt mức lớn nhất:

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


