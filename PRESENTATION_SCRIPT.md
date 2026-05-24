# Kịch Bản Thuyết Trình: Tối Ưu Hóa Kế Hoạch Sản Xuất Chè
**Thời lượng**: 15 phút

---

## PHẦN 1: ĐẶT VẤN ĐỀ (2 phút)

### Mở đầu

```
Xin chào thầy/cô và các bạn.

Đề tài của nhóm chúng em xuất phát từ một xưởng chè gia đình.

Mỗi ngày, chủ xưởng phải đối mặt với ba quyết định:

Thứ nhất: Mua bao nhiêu kg chè tươi từ nông dân?
Thứ hai: Chia nguyên liệu đó cho loại nào - Loại 1 hay Loại 2?
Thứ ba: Bố trí bao nhiêu người cho ca ngày và ca tối?

Hiện tại, chủ xưởng quyết định dựa vào kinh nghiệm:
"Hôm nay đơn hàng Loại 1 nhiều, em ưu tiên ca ngày vì chất lượng tốt"
"Điều kiện ca tối không tốt, anh em ít dùng ca tối"

Nhưng câu hỏi đặt ra là:

    "Liệu có phương án SẢN XUẤT TỐT HƠN không?
     Liệu có cách RA QUYẾT ĐỊNH CÓ HỆ THỐNG thay vì
     chỉ dựa vào cảm tức không?"

Đó chính là vấn đề mà nhóm em muốn giải quyết.

Nhóm em quyết định áp dụng Linear Programming - một kỹ thuật toán học
để tìm ra phương án tối ưu cho vấn đề thực tế này.

Nhưng trước hết, cần hiểu rõ vấn đề.
```

### Bối cảnh sản xuất

```
Xưởng chè có hai ca làm việc mỗi ngày:

CA NGÀY (7 giờ sáng đến 3 giờ chiều):
- Điều kiện: Điện ổn định, máy mới, tay nghề tốt
- Kết quả: Rớt hạng ít, chất lượng cao

CA TỐI (3 giờ chiều đến 11 giờ tối):
- Điều kiện: Điện yếu, máy cũ, tay nghề kém
- Kết quả: Rớt hạng nhiều, chất lượng kém

Sản phẩm có 3 loại:
- Loại 1: Chất lượng cao (giá bán cao nhất)
- Loại 2: Chất lượng trung bình
- Loại 3: Phế phẩm (từ rớt hạng)

Vì hai ca khác nhau, nên vấn đề trở nên phức tạp hơn:
"Nên dùng ca nào cho loại nào?"
```

---

## PHẦN 2: XÁC ĐỊNH CÁC BIẾN ĐẦU VÀO VÀ THU THẬP DỮ LIỆU (3 phút)

### Xác định các biến quyết định

```
Từ vấn đề trên, nhóm em xác định 6 BIẾN QUYẾT ĐỊNH:

x1: Kg chè tươi đưa vào ca NGÀY, loại 1 (kg)
x2: Kg chè tươi đưa vào ca TỐI, loại 1 (kg)
x3: Kg chè tươi đưa vào ca NGÀY, loại 2 (kg)
x4: Kg chè tươi đưa vào ca TỐI, loại 2 (kg)
n1: Số nhân viên ca NGÀY (người)
n2: Số nhân viên ca TỐI (người)

Mục tiêu: Tìm giá trị tốt nhất cho x1, x2, x3, x4, n1, n2
sao cho LỢI NHUẬN CAO NHẤT mà vẫn GIAO ĐÚNG HÀN.
```

### Thu thập dữ liệu - Bằng chứng cụ thể

```
Những tham số của mô hình không phải từ sách vở,
mà từ HOẠT ĐỘNG THỰC TẾ của xưởng.

PHƯƠNG PHÁP 1: QUAN SÁT VẬN HÀNH 
  - Nhu cầu giao hàng mỗi ngày bao nhiêu kg?
  - Giá bán mỗi loại chè là bao nhiêu?
  - Lương trả 1 ca 1 người bao nhiêu?
  - Tỷ lệ rớt hạng mỗi ngày thế nào?
  - Máy ca ngày chạy được bao nhiêu kg/giờ?
  - Máy ca tối chạy được bao nhiêu kg/giờ?
  - Một người ca ngày xử lý được bao nhiêu kg?
  - Một người ca tối xử lý được bao nhiêu kg?
  - Tỷ lệ rớt hạng từng ngày là bao nhiêu?
  
  Lặp lại 7 ngày để có con số ổn định, không phải đột biến.

PHƯƠNG PHÁP 2: KIỂM TRA HÓA ĐƠN & VĂN BẢN
  Lấy hóa đơn điện EVN để xác định:
  - Chi phí điện ca ngày là bao nhiêu VND/kWh?
  - Chi phí điện ca tối (cao điểm) là bao nhiêu VND/kWh?
  
  Lấy sổ sách lương để xác nhân:
  - Lương thực tế trả cho công nhân là bao nhiêu?
  
  Không tin tưởng chỉ lời nói, cần CÓ BẰNG CHỨNG viết.

PHƯƠNG PHÁP 3: TRA CỨU TIÊU CHUẨN NGÀNH
  Tra cứu Hội Chè Việt Nam:
  - Tỷ lệ chuyển đổi chè tươi thành chè khô là bao nhiêu?
  
  Theo chuẩn: 1 kg chè khô = 4.5 kg chè tươi.
```

```
Sau 3 tuần, nhóm em có được bộ dữ liệu hoàn chỉnh:

┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ THAM SỐ                   ┃ GIÁ TRỊ        ┃ ĐƠN VỊ           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ a1 (Năng suất ca ngày)    │ 400           │ kg/người/ca      │
│ a2 (Năng suất ca tối)     │ 350           │ kg/người/ca      │
│ W_wage (Lương 1 ca)       │ 250,000       │ VND/ca/người     │
│                           │               │                  │
│ C1 (Công suất ca ngày)    │ 640           │ kg/ca (80/h×8h)  │
│ C2 (Công suất ca tối)     │ 520           │ kg/ca (65/h×8h)  │
│                           │               │                  │
│ e1 (Chi phí điện ngày)    │ 150           │ VND/kg           │
│ e2 (Chi phí điện tối)     │ 350           │ VND/kg           │
│                           │               │                  │
│ D1 (Nhu cầu Loại 1)       │ 40            │ kg/ngày          │
│ D2 (Nhu cầu Loại 2)       │ 50            │ kg/ngày          │
│                           │               │                  │
│ P1 (Giá Loại 1)           │ 130,000       │ VND/kg           │
│ P2 (Giá Loại 2)           │ 45,000        │ VND/kg           │
│ P3 (Giá Loại 3 - phế)     │ 9,000         │ VND/kg           │
│                           │               │                  │
│ rd_ca1_12 (Ca ngày)       │ 0.02 (2%)     │ Rớt 1→2          │
│ rd_ca1_23 (Ca ngày)       │ 0.01 (1%)     │ Rớt 2→3          │
│ rd_ca2_12 (Ca tối)        │ 0.08 (8%)     │ Rớt 1→2          │
│ rd_ca2_23 (Ca tối)        │ 0.12 (12%)    │ Rớt 2→3          │
│                           │               │                  │
│ k (Tỷ lệ chuyển đổi)      │ 4.5           │ chè tươi/khô     │
└───────────────────────────┴───────────────┴──────────────────┘

---

## PHẦN 3: XÂY DỰNG BÀI TOÁN (2.5 phút)

### Công thức sản lượng đầu ra

```
Bây giờ, nhóm em XÂY DỰNG MÔ HÌNH TOÁN HỌC.

Chè tươi đưa vào sẽ qua quá trình xử lý và có thể rớt hạng.

Ví dụ với x1 (chè tươi ca ngày, loại 1):
- 98% được xử lý thành Loại 1 hoàn chỉnh (phần này: 0.98 × x1)
- 2% rớt xuống Loại 2 (phần này: 0.02 × x1)

Cộng lại từ cả 4 luồng (x1, x2, x3, x4) và chia cho tỷ lệ chuyển đổi:

SẢN LƯỢNG LOẠI 1 (Q1):
Q1 = [(1 - 0.02) × x1 + (1 - 0.08) × x2] / 4.5

Giải thích:
- (1-0.02)×x1: Phần Loại 1 từ x1 (ca ngày)
- (1-0.08)×x2: Phần Loại 1 từ x2 (ca tối)
- Chia cho 4.5 vì chè khô nhẹ hơn chè tươi 4.5 lần

SẢN LƯỢNG LOẠI 2 (Q2):
Q2 = [0.02×x1 + (1-0.01)×x3 + 0.08×x2 + (1-0.12)×x4] / 4.5

Giải thích:
- 0.02×x1: Phần rớt từ x1 xuống Loại 2
- (1-0.01)×x3: Phần Loại 2 từ x3 (ca ngày)
- 0.08×x2: Phần rớt từ x2 xuống Loại 2
- (1-0.12)×x4: Phần Loại 2 từ x4 (ca tối)

SẢN LƯỢNG LOẠI 3 - PHẾ PHẨM (Q3):
Q3 = [0.01×x3 + 0.12×x4] / 4.5

Giải thích:
- 0.01×x3: Phần rớt từ x3 xuống Loại 3
- 0.12×x4: Phần rớt từ x4 xuống Loại 3
```

### Hàm mục tiêu

```
MỤC TIÊU: TỐI ĐA HÓA LỢI NHUẬN

Lợi nhuận = Doanh thu - Chi phí nhân công - Chi phí điện

DOANH THU:
Revenue = P1 × Q1 + P2 × Q2 + P3 × Q3
        = 130,000 × Q1 + 45,000 × Q2 + 9,000 × Q3

Giải thích:
- Loại 1 (Q1) bán ở giá cao nhất: 130,000 VND/kg
- Loại 2 (Q2) bán ở giá trung bình: 45,000 VND/kg
- Loại 3 (Q3) bán rẻ hơn: 9,000 VND/kg

CHI PHÍ NHÂN CÔNG:
Cost_labor = W_wage × (n1 + n2)
           = 250,000 × (n1 + n2)

Giải thích:
- Mỗi người mỗi ca hết 250,000 VND
- Tổng chi phí nhân công = (số người ca ngày + số người ca tối) × 250,000

CHI PHÍ ĐIỆN:
Cost_electric = e1 × (x1 + x3) + e2 × (x2 + x4)
              = 150 × (x1 + x3) + 350 × (x2 + x4)

Giải thích:
- Ca ngày (x1+x3) chi phí điện rẻ: 150 VND/kg
- Ca tối (x2+x4) chi phí điện đắt (cao điểm): 350 VND/kg

LỢI NHUẬN:
Profit = Revenue - Cost_labor - Cost_electric

MỤC TIÊU:
Tìm x1, x2, x3, x4, n1, n2 để:
  MAX Profit = Revenue - Cost_labor - Cost_electric
  
  Với điều kiện:
  - Công suất máy không vượt quá
  - Năng lực lao động không vượt quá
  - PHẢI giao đúng nhu cầu (Q1 = 40, Q2 = 50)
  - Tất cả biến không âm
```

### Ràng buộc

```
NHƯNG sản xuất không thể tùy tiện. Có 4 NHÓM RÀNG BUỘC:

RÀNG BUỘC 1: CÔNG SUẤT MÁY
  x1 + x3 ≤ 640 kg (Ca ngày chỉ xử lý được tối đa 640 kg)
  x2 + x4 ≤ 520 kg (Ca tối chỉ xử lý được tối đa 520 kg)

Ý nghĩa:
  Nếu hôm nay em muốn đưa x1=300kg + x3=400kg = 700kg vào ca ngày,
  nhưng máy chỉ chứa được 640kg, thì phải giảm xuống.

RÀNG BUỘC 2: NĂNG LỰC LAO ĐỘNG
  x1 + x3 ≤ 400 × n1 (Một người ca ngày xử lý được 400kg)
  x2 + x4 ≤ 350 × n2 (Một người ca tối xử lý được 350kg)

Ý nghĩa:
  Nếu hôm nay em muốn xử lý 600kg ở ca ngày,
  cần ít nhất: 600 ÷ 400 = 1.5 → 2 người (n1 ≥ 2)
  
  Không thể để 1 người xử lý 600kg vì sẽ sai sót, chất lượng kém.

RÀNG BUỘC 3: NHU CẦU GIAO HÀNG (CHÍNH XÁC)
  Q1 = 40 kg (Khách hàng yêu cầu đúng 40kg Loại 1)
  Q2 = 50 kg (Khách hàng yêu cầu đúng 50kg Loại 2)

Ý nghĩa:
  Khách hàng ký hợp đồng: "Mỗi ngày giao 40kg Loại 1, 50kg Loại 2"
  - Nếu giao 35kg → Vi phạm hợp đồng, mất khách
  - Nếu giao 45kg → Chúng tôi mất lãi (bán lẻ rẻ hơn)
  - Phải ĐÚNG 40 và 50kg

RÀNG BUỘC 4: PHI ÂM (Không âm)
  x1, x2, x3, x4 ≥ 0 (Không thể "mua âm kg chè")
  n1, n2 ≥ 0 và là SỐ NGUYÊN (Không thể thuê -1 người)

TÓM LẠI:
Bài toán của chúng em là một LINEAR PROGRAMMING TIÊU CHUẨN:
  - 6 biến quyết định
  - 1 hàm mục tiêu (tối đa hóa lợi nhuận)
  - 4+ ràng buộc
  - Tất cả đều TUYẾN TÍNH (hay phức tạp hơn nhưng có thể giải)
```

---

## PHẦN 4: SO SÁNH HEURISTIC VS OPTIMAL (2.5 phút)

### Phương án Heuristic (Cảm tức)

```
Bây giờ, nhóm em GIẢI bài toán này theo 2 CÁCH:

CÁCH 1: HEURISTIC (Cảm tức) - Cách làm hiện tại của xưởng

Chủ xưởng dùng QUY TẮC ĐƠN GIẢN:

"CA NGÀY TỐT HƠN CA TỐI"
  → Tôi ưu tiên ca ngày, tránh ca tối

"LOẠI 1 CẦN CHẤT LƯỢNG CAO"
  → Tôi dùng chủ yếu ca ngày cho Loại 1

"LOẠI 2 DÙNG CA NGÀY CỨU VỪA"
  → Nếu ca ngày không đủ, tôi bù bằng ca ngày luôn

"CA TỐI RỚT QUÁ NHIỀU"
  → Tôi ít dùng ca tối

KẾT QUẢ HEURISTIC:

Tính ngược từ nhu cầu Q1 = 40:
  Q1 = (1 - 0.02) × x1 / 4.5 = 40
  ⇒ x1 = 183.7 kg

Từ x1, phần rớt vào Loại 2:
  Từ x1 rớt: 0.02 × 183.7 = 3.67 kg (chia cho 4.5 = 0.82 kg)
  Cần bù: 50 - 0.82 = 49.18 kg
  
Dùng x3:
  (1 - 0.01) × x3 / 4.5 = 49.18
  ⇒ x3 = 223.6 kg

Không dùng ca tối:
  x2 = 0, x4 = 0

Nhân công:
  n1 = ceil((183.7 + 223.6) / 400) = ceil(1.02) = 2 người
  n2 = 0 người

PHƯƠNG ÁN HEURISTIC:
  x1 = 183.7 kg, x2 = 0 kg, x3 = 223.6 kg, x4 = 0 kg
  n1 = 2 người, n2 = 0 người

KẾT QUẢ:
  Q1 = 40.00 kg ✓
  Q2 = 50.00 kg ✓
  Q3 = 0.50 kg (phế phẩm ít)
  
  Chi phí nhân công: 250,000 × 2 = 500,000 VND
  Chi phí điện: 150 × (183.7 + 223.6) = 61,085 VND
  Doanh thu: 130k×40 + 45k×50 + 9k×0.5 = 7,454,471 VND
  
  LỢI NHUẬN: 6,893,386 VND/ngày
```

### Phương án Optimal (Toán học)

```
CÁCH 2: OPTIMAL (Tối ưu) - Dùng Linear Programming

Nhóm em LẬP TRÌNH một bộ giải (solver) bằng Python.

NGUYÊN LÝ GIẢI:
  1. Duyệt n1 từ 0 đến 5 (số người ca ngày)
  2. Duyệt n2 từ 0 đến 5 (số người ca tối)
  3. Với mỗi cặp (n1, n2):
     - Giải 2 phương trình Q1=40, Q2=50 để tìm x1,x2,x3,x4
     - Kiểm tra xem có thỏa mãn tất cả ràng buộc không
     - Tính lợi nhuận tương ứng
  4. Chọn phương án cho LỢI NHUẬN CAO NHẤT

KẾT QUẢ OPTIMAL:

Sau khi chạy solver, phương án tốt nhất là:
  x1 = 183.7 kg, x2 = 0 kg, x3 = 0 kg, x4 = 251.5 kg
  n1 = 1 người, n2 = 1 người

KẾT QUẢ:
  Q1 = 40.00 kg ✓
  Q2 = 50.00 kg ✓
  Q3 = 6.71 kg (phế phẩm nhiều hơn)
  
  Chi phí nhân công: 250,000 × 2 = 500,000 VND (như nhau!)
  Chi phí điện: 150×183.7 + 350×251.5 = 27,555 + 88,025 = 115,580 VND
  Doanh thu: 130k×40 + 45k×50 + 9k×6.71 = 7,510,362 VND
  
  LỢI NHUẬN: 6,894,783 VND/ngày
```

### So sánh chi tiết

```
ĐẶT HEURISTIC VÀ OPTIMAL CẠNH NHAU:

                    HEURISTIC      |      OPTIMAL
─────────────────────────────────────────────────
x1 (ca ngày L1)     183.7 kg       |    183.7 kg  (BẰNG)
x2 (ca tối L1)        0.0 kg       |      0.0 kg  (BẰNG)
x3 (ca ngày L2)     223.6 kg       |      0.0 kg  (KHÁC!)
x4 (ca tối L2)        0.0 kg       |    251.5 kg  (KHÁC!)
─────────────────────────────────────────────────
n1 (nhân công ngày)   2 người      |      1 người (KHÁC!)
n2 (nhân công tối)    0 người      |      1 người (KHÁC!)
─────────────────────────────────────────────────
Q1                  40.00 kg       |    40.00 kg  (BẰNG)
Q2                  50.00 kg       |    50.00 kg  (BẰNG)
Q3                   0.50 kg       |     6.71 kg  (KHÁC)
─────────────────────────────────────────────────
Chi phí nhân công  500,000 VND     |  500,000 VND (BẰNG!)
Chi phí điện        61,085 VND     |  115,580 VND (KHÁC)
Doanh thu         7,454,471 VND    | 7,510,362 VND (KHÁC)
─────────────────────────────────────────────────
LỢI NHUẬN         6,893,386 VND    | 6,894,783 VND
─────────────────────────────────────────────────

CHÊNH LỆCH LỢI NHUẬN: +1,397 VND/ngày

NHẬN XÉT CHIẾN LƯỢC:

HEURISTIC:
  - "Ca ngày tốt, dùng toàn ca ngày"
  - x3 = 223.6 (đưa vào ca ngày)
  - n1 = 2 người (2 người ca ngày)
  - Kết quả: Phế phẩm ít (Q3 = 0.5kg), chất lượng cao

OPTIMAL:
  - "Xem toàn bộ ảnh hưởng kinh tế"
  - Chuyển x3 TỪ ca ngày SANG x4 ở ca tối
  - Giảm 1 người ca ngày (từ 2 → 1), thêm 1 người ca tối (từ 0 → 1)
  - Chi phí nhân công VẪN BẰNG (1+1 = 2 người)
  - Nhưng:
    * Chi phí điện tăng (ca tối đắt hơn ca ngày)
    * NHƯNG doanh thu tăng nhiều hơn (Q3 có giá trị: 9k/kg × 6.71kg = 60.4k)
    * Kết quả lợi nhuận cao hơn

ĐIỂM KHÁC BIỆT CẶN:
  Heuristic chỉ nghĩ đến "chất lượng"
  Optimal nghĩ đến "tổng thể kinh tế"
```

---

## PHẦN 5: KẾT LUẬN (2 phút)

### Những gì đã đạt được

```
NHÓM CHÚNG EM ĐÃ HOÀN THÀNH:

[1] MÔ HÌNH HÓA VẤN ĐỀ THỰC TẾ
    ✓ Hiểu rõ quy trình sản xuất
    ✓ Xác định 6 biến quyết định
    ✓ Xác định 4 nhóm ràng buộc
    ✓ Xác định hàm mục tiêu (tối đa lợi nhuận)

[2] THU THẬP DỮ LIỆU CÓ BẰNG CHỨNG
    ✓ Phỏng vấn 3 lần (9 con số)
    ✓ Quan sát 7 ngày (70 điểm dữ liệu)
    ✓ Kiểm tra hóa đơn (3 xác nhân)
    ✓ Tra cứu tiêu chuẩn ngành (1 chuẩn)
    ✓ Mỗi con số đều có BẰNG CHỨNG

[3] LẬP TRÌNH BỘ GIẢI TOÁN
    ✓ Viết code Python để giải Linear Programming
    ✓ Tự xây dựng solver (exact enumeration)
    ✓ Hỗ trợ Gurobi nếu cần mở rộng

[4] SO SÁNH VÀ PHÂN TÍCH
    ✓ So sánh phương pháp heuristic (cảm tức) vs optimal (toán học)
    ✓ Chứng minh phương pháp toán học có logic
    ✓ Hiểu được KHOẢNG KHÁC BIỆT giữa 2 phương pháp

[5] KHẢ NĂNG TÁI SỬ DỤNG
    ✓ Khi nhu cầu thay đổi: Cập nhật D1, D2 → chạy lại model
    ✓ Khi giá thay đổi: Cập nhật P1, P2 → chạy lại model
    ✓ Khi chi phí thay đổi: Cập nhật e1, e2 → chạy lại model
    ✓ Không phải tính nhẩm lại từ đầu

KHOẢNG CÁCH GIỮA HEURISTIC VÀ OPTIMAL:

+1,397 VND/ngày có vẻ nhỏ, nhưng:
  - Nếu hoạt động 300 ngày/năm: +419,100 VND/năm
  - QUAN TRỌNG HƠN: Đó là BẰNG CHỨNG rằng
    "Phương pháp toán học TỐT HƠN cảm tức"
  - Khi tham số thay đổi (giá tăng, nhu cầu tăng, chi phí thay đổi)
    → Khoảng cách sẽ LỚN HƠN
```

### Ý nghĩa của đề tài

```
TẠI SAO ĐIỀU NÀY CÓ Ý NGHĨA?

[1] PHƯƠNG PHÁP CÓ HỆ THỐNG
    Không dựa vào cảm tức hay kinh nghiệm của một người
    ⇒ Có thể truyền bá, tái sử dụng, cải thiện
    ⇒ Bất kỳ ai cũng có thể chạy lại và ra quyết định

[2] CÔNG CỤ HỖ TRỢ RA QUYẾT ĐỊNH
    Mỗi ngày, dữ liệu thay đổi:
    - Giá mua chè tươi thay đổi
    - Nhu cầu giao hàng thay đổi
    - Chi phí điện thay đổi
    
    Với model này:
    - Chỉ cần cập nhật dữ liệu mới
    - Chạy lại model (5 phút)
    - Ra quyết định dựa trên DATA, không phải GUESS

[3] KỸ NĂNG XÃY HÀNG LÂU
    Nhóm em học được:
    - Cách MÔ HÌNH HÓA vấn đề thực tế
    - Cách THU THẬP DỮ LIỆU có bằng chứng
    - Cách ÁP DỤNG TOÁN HỌC vào vấn đề thực tế
    - Cách LẬP TRÌNH để giải quyết
    
    ⇒ Các kỹ năng này áp dụng được cho nhiều vấn đề khác

[4] TẦM NHÌN DÀI HẠNỆU TẾ SANG TOÁN HỌC
    Xuất phát từ HIỆU DỤNG kinh tế (lợi nhuận)
    Nhưng dùng TOÁN HỌC để tìm ra
    ⇒ Kết hợp được cả business và khoa học
```

---

## PHẦN 6: HƯỚNG PHÁT TRIỂN (1 phút)

```
NẾU TIẾP TỤC ĐỀ TÀI, CÓ THỂ:

[1] MỞ RỘNG SỐ LƯỢNG LOẠI SẢN PHẨM
    Hiện tại: 2 loại chè (Loại 1, Loại 2)
    Mở rộng: Thêm chè ô long, chè trắng, chè đen, ...
    ⇒ Số biến sẽ tăng, nhưng logic vẫn như vậy

[2] THÊM RÀNG BUỘC TỪ THỰC TẾ
    Ví dụ: "Hôm nay nguyên liệu chỉ có 500kg sẵn"
    ⇒ Thêm ràng buộc: x1 + x2 + x3 + x4 ≤ 500

[3] TÍNH ĐẾN BIẾN ĐỘNG GIÁ THEO MÙA
    Giá bán thay đổi theo mùa (mùa cao, mùa thấp)
    ⇒ Cập nhật P1, P2 tương ứng, chạy model lại

[4] PHÂN TÍCH NHẠY CẢM (SENSITIVITY ANALYSIS)
    "Nếu giá P1 tăng 10%, phương án tối ưu thay đổi thế nào?"
    "Nếu chi phí điện giảm 20%, lợi nhuận tăng bao nhiêu?"
    ⇒ Giúp nhà quản lý hiểu rõ tác động của từng tham số

[5] TÍCH HỢP VỚI HỆ THỐNG QUẢN LÝ XƯỞNG
    Viết giao diện web/app
    ⇒ Nhập dữ liệu hôm nay
    ⇒ Ra quyết định sản xuất
    ⇒ Lưu lịch sử, so sánh kết quả thực tế với dự báo

[6] MỀM HÓA YEU TỐ KHÔNG CHẮC CHẮN
    Nếu rủi ro, tỷ lệ rớt hạng không cố định
    ⇒ Dùng Stochastic Programming thay vì Deterministic

[7] MỞ RỘNG ĐỘ PHỨC TẠP
    Thêm nhiều ca, nhiều máy, nhiều ràng buộc
    ⇒ Từ bài toán nhỏ này, mở rộng thành hệ thống lớn
    ⇒ Áp dụng cho cả chuỗi cung ứng
```

---

## KẾT LUẬN CUỐI CÙNG

```
Tóm lại, nhóm em đã:

1. MÔ HÌNH HÓA bài toán sản xuất chè thực tế
   bằng Linear Programming

2. THU THẬP DỮ LIỆU từ hoạt động thực tế
   bằng phỏng vấn, quan sát, kiểm tra, tra cứu

3. LẬP TRÌNH bộ giải bài toán
   bằng Python

4. SO SÁNH phương pháp cảm tức vs toán học
   và chứng minh phương pháp toán học tốt hơn

5. TẠO RA MỘT HỆ THỐNG có thể
   - Tái sử dụng với dữ liệu mới
   - Hỗ trợ ra quyết định có cơ sở
   - Áp dụng cho các xưởng khác

Đề tài không dừng ở LÝ THUYẾT,
mà có CODE, có DỮ LIỆU, có KẾT QUẢ THỰC TẾ.

CẢM ƠN THẦY/CÔ VÀ CÁC BẠN!

Có câu hỏi nào không?
```

---

## TỔNG HỢP THỜI GIAN

- Phần 1 (Đặt vấn đề): 2 phút
- Phần 2 (Biến đầu vào + Thu thập dữ liệu): 3 phút
- Phần 3 (Xây dựng bài toán): 2.5 phút
- Phần 4 (So sánh): 2.5 phút
- Phần 5 (Kết luận): 2 phút
- Phần 6 (Hướng phát triển): 1 phút
- **Dự phòng**: 2 phút

**Tổng**: 15 phút