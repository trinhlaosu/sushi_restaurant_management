# Web API quản lý nhà hàng sushi

Đề tài xây dựng backend API cho hệ thống quản lý đặt món và bán hàng tại nhà hàng sushi.
Project chỉ làm phần API, không làm giao diện frontend. Việc kiểm thử API thực hiện bằng Postman.

## 1. Thông tin chung

- Nhóm thực hiện: Nhóm 07
- Ngôn ngữ: Python
- Framework: Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Công cụ test API: Postman

## 2. Chức năng chính

- Đăng ký, đăng nhập, đăng xuất.
- Phân quyền người dùng: admin và nhân viên.
- Quản lý danh mục món ăn.
- Quản lý món ăn trong menu.
- Quản lý bàn ăn.
- Quản lý khách hàng.
- Tạo đơn gọi món.
- Tự động tính tổng tiền đơn hàng.
- Thanh toán đơn hàng.
- Thống kê doanh thu và món bán chạy.

## 3. Cấu trúc thư mục

Project dùng Flask nên cấu trúc khác mẫu Django, nhưng vẫn chia theo model, controller và service.

```text
sushi_restaurant_management/
├── app/
│   ├── controllers/      # Các API endpoint
│   ├── models/           # Các bảng trong database
│   ├── services/         # Xử lý nghiệp vụ
│   ├── utils/            # Hàm dùng chung, xác thực token
│   ├── extensions.py     # Khởi tạo SQLAlchemy
│   └── __init__.py       # Tạo app Flask và đăng ký route
├── database/
│   ├── schema.sql
│   └── sushi_restaurant.db
├── docs/                 # ERD, hình minh họa
├── postman/              # File Postman collection
├── tests/                # Unit test
├── config.py
├── run.py
├── seed.py
└── requirements.txt
```

## 4. Cơ sở dữ liệu

Database sử dụng SQLite:

```text
database/sushi_restaurant.db
```

CSDL có 10 bảng:

```text
roles
users
access_tokens
categories
menu_items
tables
customers
orders
order_details
payments
```

ERD nằm trong thư mục:

```text
docs/
```

## 5. Cài đặt và chạy project

Mở terminal tại thư mục project, sau đó chạy:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Tạo lại dữ liệu mẫu:

```bash
python seed.py
```

Chạy server:

```bash
python run.py
```

Sau khi chạy, API mở tại:

```text
http://127.0.0.1:5000
```

Kiểm tra server:

```text
GET http://127.0.0.1:5000/api/health
```

## 6. Tài khoản mẫu

| Quyền | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Nhân viên | staff | staff123 |

## 7. Kiểm thử bằng Postman

Import file sau vào Postman:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

Thứ tự test cơ bản:

```text
Health check
Đăng nhập admin
Xem danh sách món
Thêm món mới
Tạo đơn gọi món
Xem chi tiết đơn hàng
Thanh toán đơn hàng
Thống kê doanh thu
Món bán chạy
```

Sau khi đăng nhập, copy token hoặc dùng biến `{{token}}` trong collection.
Các API cần đăng nhập dùng header:

```text
Authorization: Bearer <token>
```

## 8. Chạy unit test

```bash
python -m unittest discover -s tests -v
```

Các test hiện có kiểm tra:

- Đăng nhập đúng/sai.
- Admin thêm món được.
- Nhân viên không được thêm món.
- Tạo đơn và tính tổng tiền.
- Thanh toán đơn hàng.

## 9. API quan trọng

API tạo đơn gọi món:

```text
POST /api/orders
```

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

Hệ thống tự lấy giá món trong database, tính thành tiền từng dòng và tổng tiền đơn hàng.

## 10. Danh sách API

### Auth

| Method | URL | Chức năng |
|---|---|---|
| POST | `/api/auth/register` | Đăng ký tài khoản |
| POST | `/api/auth/login` | Đăng nhập |
| POST | `/api/auth/logout` | Đăng xuất |

### Danh mục

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/categories` | Xem danh sách danh mục |
| GET | `/api/categories/<id>` | Xem chi tiết danh mục |
| POST | `/api/categories` | Thêm danh mục |
| PUT | `/api/categories/<id>` | Cập nhật danh mục |
| DELETE | `/api/categories/<id>` | Xóa danh mục |

### Món ăn

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/menu-items` | Xem danh sách món |
| GET | `/api/menu-items/<id>` | Xem chi tiết món |
| POST | `/api/menu-items` | Thêm món |
| PUT | `/api/menu-items/<id>` | Cập nhật món |
| DELETE | `/api/menu-items/<id>` | Ẩn món khỏi menu |

### Bàn ăn

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/tables` | Xem danh sách bàn |
| POST | `/api/tables` | Thêm bàn |
| PUT | `/api/tables/<id>` | Cập nhật bàn |
| DELETE | `/api/tables/<id>` | Xóa bàn |

### Khách hàng

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/customers` | Xem danh sách khách hàng |
| POST | `/api/customers` | Thêm khách hàng |
| PUT | `/api/customers/<id>` | Cập nhật khách hàng |
| DELETE | `/api/customers/<id>` | Xóa khách hàng |

### Đơn hàng

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/orders` | Xem danh sách đơn hàng |
| GET | `/api/orders/<id>` | Xem chi tiết đơn hàng |
| POST | `/api/orders` | Tạo đơn gọi món |
| PUT | `/api/orders/<id>/status` | Cập nhật trạng thái đơn |

### Thanh toán

| Method | URL | Chức năng |
|---|---|---|
| POST | `/api/payments` | Thanh toán đơn hàng |
| GET | `/api/payments` | Xem lịch sử thanh toán |

### Người dùng

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/users` | Xem danh sách người dùng |
| PUT | `/api/users/<id>/role` | Đổi quyền người dùng |

### Thống kê

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/statistics` | Thống kê tổng quan |
| GET | `/api/statistics/revenue` | Thống kê doanh thu |
| GET | `/api/statistics/popular-items` | Món bán chạy |

## 11. Ghi chú

- Dữ liệu dùng tiếng Việt có dấu.
- Đơn vị tiền tệ là VND.
- Số bảng trong CSDL: 10 bảng.
- Chạy `python seed.py` sẽ xóa dữ liệu cũ và tạo lại dữ liệu mẫu.
