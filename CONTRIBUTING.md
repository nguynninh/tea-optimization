# Hướng Dẫn Đóng Góp (Contributing Guide)

Cảm ơn bạn đã quan tâm đến dự án **Tea Production Optimization**! Mọi đóng góp — dù là sửa lỗi nhỏ, cải thiện tài liệu hay đề xuất mô hình mới — đều được trân trọng.

---

## Mục Lục

1. [Quy Tắc Ứng Xử](CODE_OF_CONDUCT.md)
2. [Cách Bắt Đầu](#2-cách-bắt-đầu)
3. [Quy Trình Đóng Góp](#3-quy-trình-đóng-góp)
4. [Tiêu Chuẩn Code](#4-tiêu-chuẩn-code)
5. [Báo Cáo Lỗi](#5-báo-cáo-lỗi)
6. [Đề Xuất Tính Năng](#6-đề-xuất-tính-năng)

---

## 1. Quy Tắc Ứng Xử

Xem chi tiết tại [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 2. Cách Bắt Đầu

### Yêu Cầu Hệ Thống

- **Python** ≥ 3.8
- **Gurobi** (bản academic hoặc có license) — xem [Gurobi Academic Program](https://www.gurobi.com/academia/academic-program-and-licenses/)
- `pip install gurobipy`

### Thiết Lập Môi Trường Phát Triển

```bash
# 1. Fork repository trên GitHub, sau đó clone về máy
git clone https://github.com/<your-username>/tea-optimization.git
cd tea-optimization

# 2. Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Cài đặt dependencies
pip install gurobipy

# 4. Chạy thử để xác nhận môi trường ổn định
python main.py
```

---

## 3. Quy Trình Đóng Góp

### Bước 1 — Tạo Issue Trước

Trước khi viết code, hãy mở một Issue để:
- Mô tả lỗi bạn gặp, hoặc
- Thảo luận về tính năng / thay đổi mô hình bạn muốn đề xuất.

Điều này giúp tránh công sức bị lãng phí do trùng lặp hoặc hướng đi không phù hợp.

### Bước 2 — Tạo Branch

Đặt tên branch theo định dạng:

```
feat/<mô-tả-ngắn>      # Tính năng mới
fix/<mô-tả-ngắn>       # Sửa lỗi
docs/<mô-tả-ngắn>      # Cải thiện tài liệu
refactor/<mô-tả-ngắn>  # Tái cấu trúc code
```

Ví dụ:

```bash
git checkout -b feat/add-night-shift-constraint
```

### Bước 3 — Commit

Tuân theo định dạng commit có cấu trúc:

```
<type>: <mô tả ngắn gọn>

[Mô tả chi tiết nếu cần — giải thích tại sao, không phải làm gì]

Refs: #<issue-number>
```

**Các type được chấp nhận:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Ví dụ:

```
feat: thêm ràng buộc giới hạn tổng nguyên liệu mua trong ngày

Bổ sung constraint W_buy <= W_max để phản ánh giới hạn
vốn thu mua chè tươi thực tế của xưởng.

Refs: #12
```

### Bước 4 — Mở Pull Request

- Mở PR từ branch của bạn vào `main`.
- Điền đầy đủ mô tả: thay đổi là gì, tại sao cần, cách kiểm tra.
- Liên kết Issue liên quan (`Closes #<issue-number>`).

---

## 4. Tiêu Chuẩn Code

### Python

- Tuân theo [PEP 8](https://peps.python.org/pep-0008/).
- Đặt tên biến rõ ràng, ưu tiên khớp với ký hiệu toán học trong README (ví dụ: `x1`, `y2`, `r12`).
- Thêm comment giải thích ý nghĩa kinh tế / toán học của từng đoạn code quan trọng.
- Không commit file `.env`, dữ liệu nhạy cảm hay Gurobi license key.

### Mô Hình Toán Học

Nếu bạn thay đổi mô hình LP:

- Cập nhật phần **Mô Hình Toán Học** trong `README.md` tương ứng.
- Giải thích ý nghĩa kinh tế của ràng buộc / biến mới trong PR description.
- Cung cấp ví dụ số minh họa nếu có thể.

---

## 5. Báo Cáo Lỗi

Khi mở Issue báo lỗi, vui lòng cung cấp:

1. **Môi trường:** Python version, Gurobi version, OS.
2. **Bước tái hiện:** Lệnh đã chạy, input parameters đã dùng.
3. **Kết quả thực tế** vs. **Kết quả kỳ vọng**.
4. **Log / Traceback** (nếu có).

---

## 6. Đề Xuất Tính Năng

Một số hướng đóng góp có giá trị cao cho dự án:

- **Mở rộng mô hình:** Thêm biến quyết định cho số ca, lập lịch bảo trì máy, tối ưu đa ngày.
- **Giao diện:** Xây dựng CLI hoặc web UI để nhập tham số và xem kết quả trực quan.
- **Phân tích độ nhạy:** Tự động chạy sensitivity analysis khi thay đổi `r12`, `r23`, giá bán.
- **Dữ liệu thực:** Kết nối với file CSV / Excel để load tham số thực tế từ xưởng.
- **Tài liệu:** Dịch README sang tiếng Anh hoặc bổ sung giải thích học thuật.

---

Mọi câu hỏi, vui lòng mở một Issue với nhãn **`question`**. Chúng tôi sẽ phản hồi sớm nhất có thể.
