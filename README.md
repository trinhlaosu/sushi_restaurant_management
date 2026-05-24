# Web API quản lý đặt món và bán hàng cho nhà hàng sushi

Đề tài xây dựng backend API bằng Python Flask. Ứng dụng không có frontend, kiểm thử API bằng Postman.

## 1. Công nghệ sử dụng

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- SQLite
- Postman

## 2. Cài đặt

```bash
cd Nhom07_Code\sushi_restaurant_management
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
python seed.py
python run.py
```

Sau khi chạy, API mở tại:

```text
http://127.0.0.1:5000
```

## 3. Tài khoản mẫu

| Quyền | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Nhân viên | staff | staff123 |

## 4. Cách kiểm thử nhanh bằng Postman

1. Gửi `POST /api/auth/login` với tài khoản `admin/admin123`.
2. Copy token trả về.
3. Với các API cần đăng nhập, thêm Header:

```text
Authorization: Bearer <token>
```

## 5. Chạy unit test

```bash
python -m unittest discover -s tests -v
```

## 6. API quan trọng nhất

`POST /api/orders` dùng để tạo đơn gọi món. Hệ thống tự lấy giá món trong CSDL, tính thành tiền từng dòng và tổng tiền hóa đơn.

Ví dụ body:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "items": [
    {"menu_item_id": 1, "quantity": 2},
    {"menu_item_id": 4, "quantity": 1},
    {"menu_item_id": 14, "quantity": 2}
  ]
}
```

## 7. Cấu trúc thư mục

Project dùng Flask nên cấu trúc khác mẫu Django của giảng viên, nhưng vẫn chia theo MVC và service:

```text
sushi_restaurant_management/
├── app/
│   ├── controllers/      # Tương đương views/urls: định nghĩa REST API endpoints
│   ├── models/           # Định nghĩa các bảng CSDL bằng SQLAlchemy
│   ├── services/         # Xử lý nghiệp vụ: gọi món, thanh toán, thống kê
│   ├── utils/            # Code dùng chung: xác thực, phân quyền
│   ├── extensions.py     # Khởi tạo SQLAlchemy
│   └── __init__.py       # Tạo Flask app và đăng ký routes
├── database/
│   ├── schema.sql
│   └── sushi_restaurant.db
├── docs/                 # Hình ERD, kiến trúc, minh họa Postman
├── postman/              # Collection kiểm thử API
├── tests/                # Unit test cho API
├── config.py             # Cấu hình project
├── run.py                # Chạy API server
├── seed.py               # Tạo CSDL mẫu
└── requirements.txt
```
