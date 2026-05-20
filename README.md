# 📚 Hệ Thống Quản Lý Thư Viện (Library Management System)

Một ứng dụng web hoàn chỉnh để quản lý các hoạt động của thư viện, bao gồm quản lý sách, độc giả, nhân viên, và các giao dịch mượn/trả sách.

## 🎯 Tính Năng Chính

### 1. **Quản Lý Sách**
- Thêm, sửa, xóa sách
- Quản lý thông tin: tác giả, năm xuất bản, nhà xuất bản
- Phân loại sách theo thể loại
- Theo dõi số lượng sách tại các chi nhánh

### 2. **Quản Lý Độc Giả**
- Đăng ký thành viên mới
- Quản lý thông tin cá nhân
- Cấp và theo dõi thẻ thư viện
- Lịch sử mượn sách

### 3. **Quản Lý Nhân Viên**
- Quản lý nhân viên tại các chi nhánh
- Ghi nhận ca làm việc
- Phân bổ nhân viên theo chi nhánh

### 4. **Quản Lý Mượn/Trả Sách**
- Tạo đơn mượn sách mới
- Ghi nhận trả sách
- **Tính toán phí phạt** tự động khi trả muộn:
  - 5,000 VND/ngày nếu trả sau hạn
  - Hạn mượn mặc định: 30 ngày
- Theo dõi trạng thái đơn mượn

### 5. **Quản Lý Chi Nhánh**
- Thêm chi nhánh mới
- Quản lý sách tại mỗi chi nhánh
- Quản lý nhân viên chi nhánh

### 6. **Dashboard**
- Thống kê tổng quan (tổng sách, thành viên, nhân viên)
- Số đơn mượn đang diễn ra
- Số đơn mượn quá hạn
- Truy cập nhanh đến các tính năng chính

## 🛠️ Công Nghệ Sử Dụng

- **Backend:** Python 3.8+ với Flask 2.3.3
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework:** Flask-SQLAlchemy

## 📋 Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (Python package manager)
- Terminal/Command Prompt

## 📦 Cài Đặt

### Bước 1: Clone hoặc tải project

```bash
cd library_management
```

### Bước 2: Tạo virtual environment (tùy chọn nhưng khuyến khích)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Chạy ứng dụng

```bash
python run.py
```

Ứng dụng sẽ chạy tại `http://localhost:5000`

## 📊 Cấu Trúc Cơ Sở Dữ Liệu

### Các Bảng Chính

| Bảng | Mô tả |
|------|-------|
| `sach` | Lưu thông tin sách |
| `ban_sao` | Lưu bản sao sách tại các chi nhánh |
| `thai_loai` | Thể loại sách |
| `nha_cung_cap` | Nhà cung cấp/nhà xuất bản |
| `chi_nhanh` | Chi nhánh thư viện |
| `thanh_vien` | Thành viên/độc giả |
| `the_thu_vien` | Thẻ thư viện |
| `nhan_vien` | Nhân viên thư viện |
| `ca_lam` | Ca làm việc |
| `don_muon` | Đơn mượn sách |

## 🎨 Giao Diện Chính

### Trang Chủ (Dashboard)
- Thống kê tổng quan
- Nút truy cập nhanh

### Quản Lý Sách
- Danh sách sách với phân trang
- Form thêm/sửa sách

### Quản Lý Thành Viên
- Danh sách thành viên
- Form đăng ký thành viên
- Thông tin thẻ thư viện

### Quản Lý Mượn/Trả
- Danh sách đơn mươn
- Lọc theo trạng thái (Đang mượn, Đã trả, Quá hạn)
- Form trả sách với tính phí phạt tự động

## 💾 Dữ Liệu Mẫu

Ứng dụng tự động tạo dữ liệu mẫu khi khởi động:
- 5 thể loại sách
- 3 nhà cung cấp
- 3 chi nhánh

## 🔧 Cấu Hình

### Chỉnh sửa `app/config.py`:

```python
# Thay đổi số tiền phạt
FINE_PER_DAY = 5000  # VND

# Thay đổi số ngày mượn
BORROW_DAYS = 30

# Thay đổi số item hiển thị trên trang
ITEMS_PER_PAGE = 10
```

## 📝 Hướng Dẫn Sử Dụng

### Quy Trình Mượn Sách

1. **Đăng ký thành viên:**
   - Truy cập "Thành viên" → "Thêm thành viên mới"
   - Nhập thông tin và lưu

2. **Tạo đơn mượn:**
   - Truy cập "Mượn/Trả" → "Tạo đơn mượn mới"
   - Chọn thành viên, sách, nhân viên
   - Hệ thống tự động tính hạn trả (30 ngày)

3. **Trả sách:**
   - Truy cập "Mượn/Trả" → Tìm đơn mượn
   - Nhấp "Trả" → Xác nhận
   - Hệ thống tự động tính phí phạt nếu trả muộn

### Tính Toán Phí Phạt

```
Nếu ngày trả thực tế > hạn trả:
  Số ngày trễ = ngày trả thực tế - hạn trả
  Phí phạt = số ngày trễ × 5,000 VND
```

## 🐛 Khắc Phục Sự Cố

### Lỗi: Database is locked
```bash
# Xóa file database cũ
rm app/library.db
# Khởi động lại ứng dụng
python run.py
```

### Lỗi: Module not found
```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt
```

### Lỗi: Port 5000 đang sử dụng
```bash
# Thay đổi port trong run.py
app.run(port=5001)
```

## 📚 Các File Quan Trọng

```
library_management/
├── run.py                 # Entry point
├── requirements.txt       # Dependencies
├── .env                  # Environment variables
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── config.py         # Configuration
│   ├── database.py       # Database initialization
│   ├── models/
│   │   └── __init__.py   # All database models
│   ├── routes/
│   │   └── __init__.py   # All routes/views
│   ├── templates/        # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── sach/
│   │   ├── thanh_vien/
│   │   ├── nhan_vien/
│   │   ├── don_muon/
│   │   ├── the_thu_vien/
│   │   └── chi_nhanh/
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
└── README.md             # This file
```

## 🚀 Triển Khai Production

1. Thay đổi `FLASK_ENV` thành `production`
2. Thay đổi `SECRET_KEY` trong `.env`
3. Sử dụng PostgreSQL thay vì SQLite
4. Sử dụng Gunicorn để chạy:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

## 📖 Tài Liệu Tham Khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 👨‍💻 Tác Giả

Tạo bởi: **Senior Full-stack Developer**
Ngày: Tháng 5 năm 2026

## 📄 Giấy Phép

MIT License - Tự do sử dụng cho mục đích học tập và thương mại

## 💬 Liên Hệ & Hỗ Trợ

Nếu có bất kỳ câu hỏi hoặc vấn đề nào, vui lòng tạo issue hoặc liên hệ với tác giả.

---

**Enjoy! 🎉**
