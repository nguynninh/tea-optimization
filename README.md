# Tea Production Optimization

Du an toi uu hoa ke hoach san xuat che bang mo hinh quy hoach tuyen tinh. Chuong trinh tinh cach phan bo che tuoi vao ca ngay, ca toi va so lao dong can dung de dap ung don hang voi loi nhuan cao nhat.

## 1. Bai toan

Xuong che co 2 ca san xuat:

- Ca ngay: dien on dinh, rui ro rot hang thap.
- Ca toi: dieu kien kem hon, rui ro rot hang cao hon.

Thanh pham co 3 loai:

- Loai 1: che chat luong cao, gia ban cao nhat.
- Loai 2: che chat luong trung binh.
- Loai 3: che rot hang/phe pham, van co the ban voi gia thap.

Muc tieu cua chuong trinh la tra loi cac cau hoi:

- Mua bao nhieu kg che tuoi?
- Chia che tuoi vao ca ngay va ca toi nhu the nao?
- Nen san xuat theo huong Loai 1 hay Loai 2 o tung ca?
- Can bao nhieu nguoi cho moi ca?
- Phuong an nao dat loi nhuan cao nhat ma van giao du Loai 1 va Loai 2?

## 2. Mo hinh

### Bien quyet dinh

| Bien | Y nghia |
| --- | --- |
| `x1` | Kg che tuoi vao ca ngay, chu dich lam Loai 1 |
| `x2` | Kg che tuoi vao ca toi, chu dich lam Loai 1 |
| `x3` | Kg che tuoi vao ca ngay, chu dich lam Loai 2 |
| `x4` | Kg che tuoi vao ca toi, chu dich lam Loai 2 |
| `n1` | So tho ca ngay |
| `n2` | So tho ca toi |

### Dau vao chinh

Du lieu mac dinh nam o `data/baseline_scenario.json`.

| Tham so | Y nghia |
| --- | --- |
| `D1`, `D2` | Nhu cau che kho Loai 1 va Loai 2 can giao |
| `k` | He so quy doi che tuoi sang che kho |
| `T1`, `T2` | So gio ca ngay va ca toi |
| `C1`, `C2` | Cong suat may moi gio o tung ca |
| `a1`, `a2` | Nang suat lao dong moi nguoi moi ca |
| `W_wage` | Tien cong moi nguoi moi ca |
| `e1`, `e2` | Chi phi dien quy doi tren moi kg che tuoi |
| `P1`, `P2`, `P3` | Gia ban che Loai 1, Loai 2, Loai 3 |
| `rd_ca1_12` | Ty le Loai 1 rot xuong Loai 2 o ca ngay |
| `rd_ca1_23` | Ty le Loai 2 rot xuong Loai 3 o ca ngay |
| `rd_ca2_12` | Ty le Loai 1 rot xuong Loai 2 o ca toi |
| `rd_ca2_23` | Ty le Loai 2 rot xuong Loai 3 o ca toi |

### Cong thuc san luong

```text
Q1 = [(1 - rd_ca1_12) * x1 + (1 - rd_ca2_12) * x2] / k

Q2 = [rd_ca1_12 * x1
      + (1 - rd_ca1_23) * x3
      + rd_ca2_12 * x2
      + (1 - rd_ca2_23) * x4] / k

Q3 = [rd_ca1_23 * x3 + rd_ca2_23 * x4] / k
```

Trong code hien tai, mo hinh dat `Q1 == D1` va `Q2 == D2`. Nghia la chuong trinh tim phuong an giao dung nhu cau Loai 1 va Loai 2, tranh san xuat du thua hai loai nay.

### Rang buoc

- Tong che tuoi moi ca khong vuot cong suat may.
- Tong che tuoi moi ca khong vuot nang luc xu ly cua so tho duoc bo tri.
- San luong Loai 1 va Loai 2 phai bang nhu cau can giao.
- Cac bien san luong khong am.
- `n1`, `n2` la so nguyen khong am.

### Ham muc tieu

```text
Maximize Profit = Revenue - Cost_labor - Cost_electric

Revenue       = P1 * Q1 + P2 * Q2 + P3 * Q3
Cost_labor    = W_wage * (n1 + n2)
Cost_electric = e1 * (x1 + x3) + e2 * (x2 + x4)
```

## 3. Cau truc du an

```text
tea-optimization/
├── main.py                         # Entry point de chay chuong trinh
├── src/
│   ├── main.py                     # CLI, in ket qua, goi solver
│   └── solver.py                   # Data model va solver noi bo
├── data/
│   └── baseline_scenario.json      # Bo du lieu mac dinh
├── analysis_heuristic_vs_optimal.py # So sanh cach lam thu cong va toi uu
└── README.md
```

## 4. Cach chay

### Yeu cau

- Python 3.10 tro len.
- Khong bat buoc cai Gurobi neu dung solver noi bo `exact`.

Kiem tra Python:

```bash
python3 --version
```

### Chay nhanh bang solver noi bo

Lenh nay chay duoc ngay, khong can cai them thu vien:

```bash
python3 main.py --solver exact
```

Ket qua mau voi `data/baseline_scenario.json`:

```text
=== KẾT QUẢ TỐI ƯU ===
Solver su dung: exact-enumeration
Biến quyết định:
  x1 = 183.6735 kg -> che tuoi ca 1, luong 1
  x2 = 0.0000 kg -> che tuoi ca 2, luong 1
  x3 = 0.0000 kg -> che tuoi ca 1, luong 2
  x4 = 251.5074 kg -> che tuoi ca 2, luong 2
  n1 = 1 nguoi
  n2 = 1 nguoi

Tổng hợp sản lượng:
  W_buy = 435.1809 kg che tuoi
  Q1 = 40.0000 kg che kho loai 1
  Q2 = 50.0000 kg che kho loai 2
  Q3 = 6.7069 kg che kho loai 3

Chi phí và doanh thu:
  Chi phi nhan cong = 500,000 VND
  Chi phi dien      = 115,579 VND
  Doanh thu         = 7,510,362 VND
  Loi nhuan         = 6,894,783 VND
```

### Chay che do tu dong

```bash
python3 main.py
```

Che do `auto` se dung Gurobi neu may da cai `gurobipy`; neu khong co Gurobi thi tu dong dung solver noi bo.

### Chay voi Gurobi neu co license

```bash
python3 -m pip install gurobipy
python3 main.py --solver gurobi
```

Neu may chua co license Gurobi hop le, hay dung:

```bash
python3 main.py --solver exact
```

### Chay voi file du lieu rieng

Tao mot file JSON moi, vi du `data/my_scenario.json`, voi dung cac key giong `data/baseline_scenario.json`, sau do chay:

```bash
python3 main.py --data data/my_scenario.json --solver exact
```

Vi du noi dung file:

```json
{
  "D1": 40.0,
  "D2": 50.0,
  "k": 4.5,
  "T1": 8.0,
  "T2": 8.0,
  "C1": 80.0,
  "C2": 65.0,
  "a1": 400.0,
  "a2": 350.0,
  "W_wage": 250000.0,
  "e1": 150.0,
  "e2": 350.0,
  "P1": 130000.0,
  "P2": 45000.0,
  "P3": 9000.0,
  "rd_ca1_12": 0.02,
  "rd_ca1_23": 0.01,
  "rd_ca2_12": 0.08,
  "rd_ca2_23": 0.12
}
```

## 5. Phan tich heuristic vs optimal

Script nay so sanh cach lap ke hoach thu cong voi nghiem toi uu:

```bash
python3 analysis_heuristic_vs_optimal.py
```

Ket qua hien tai cho thay nghiem toi uu cai thien loi nhuan khoang `1,397 VND/ngay` so voi quy tac thu cong tren bo du lieu mac dinh.

## 6. Luu y quan trong

- Cac ty le rui ro nhu `0.02` nghia la `2%`, khong nhap `2`.
- `C1`, `C2` la cong suat kg che tuoi moi gio; tong cong suat ca se la `C1 * T1` va `C2 * T2`.
- `a1`, `a2` la kg che tuoi moi nguoi xu ly duoc trong mot ca.
- `e1`, `e2` la chi phi dien da quy doi theo kg che tuoi, khong phai don gia kWh truc tiep.
- Neu tang `D1` hoac `D2` qua kha nang may/nhan cong, chuong trinh se bao khong co nghiem kha thi.
- Solver noi bo phu hop cho bai demo nho trong repo. Neu mo rong bai toan lon hon, nen dung Gurobi hoac mot solver toi uu hoa chuyen dung.

## 7. Loi thuong gap

### `FileNotFoundError: data/baseline_scenario.json`

Hay chay lenh tu thu muc goc cua repo:

```bash
cd tea-optimization
python3 main.py --solver exact
```

### `RuntimeError: gurobipy is not installed`

Ban dang ep dung Gurobi bang `--solver gurobi` nhung may chua cai thu vien. Dung solver noi bo:

```bash
python3 main.py --solver exact
```

Hoac cai Gurobi:

```bash
python3 -m pip install gurobipy
```

### `No feasible solution for the provided scenario`

Du lieu dau vao dang yeu cau san luong vuot kha nang san xuat. Hay kiem tra lai:

- `D1`, `D2` co qua cao khong?
- `T1`, `T2`, `C1`, `C2` co qua thap khong?
- `a1`, `a2` co qua thap khong?
- Ty le rot hang co qua cao khong?

## 8. License

Du an su dung license trong file `LICENSE`.
