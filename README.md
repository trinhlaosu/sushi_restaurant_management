# Sushi Restaurant Management API

Backend API quản lý nhà hàng sushi, xây dựng bằng Flask. Project tập trung vào
phần API, không làm giao diện frontend. API có thể kiểm thử bằng Postman hoặc
unit test trong thư mục `tests/`.

## 1. Thông Tin Chung

- Nhóm thực hiện: Nhóm 07
- Ngôn ngữ: Python
- Framework: Flask
- ORM: Flask-SQLAlchemy
- Database mặc định: SQLite
- Kiểm thử: `unittest`, Postman

## 2. Kiến Trúc Source

Project tổ chức theo MVC kết hợp service layer:

```text
sushi_restaurant_management/
|-- app/
|   |-- controllers/        # Controller/API endpoint
|   |-- models/             # Model SQLAlchemy
|   |-- services/           # Business logic/service layer
|   |-- utils/              # Auth, response helper
|   |-- extensions.py       # Khởi tạo SQLAlchemy
|   `-- __init__.py         # Tạo Flask app, register blueprint
|-- payment_app/            # App/module riêng cho thanh toán
|   |-- controllers/
|   `-- services/
|-- database/               # SQLite database
|-- docs/                   # Tài liệu, mô tả kiến trúc
|-- postman/                # Postman collection
|-- tests/                  # Unit test API
|-- config.py
|-- run.py
|-- seed.py
`-- requirements.txt
```

Chi tiết kiến trúc nằm ở:

```text
docs/SOURCE_ARCHITECTURE.md
```

## 3. Điểm Đáp Ứng Yêu Cầu Đồ Án

- **OOP**: model là class kế thừa `db.Model`; service là class xử lý nghiệp vụ.
- **MVC rõ ràng**:
  - Model: `app/models/`
  - Controller: `app/controllers/`, `payment_app/controllers/`
  - Service: `app/services/`, `payment_app/services/`
- **Service layer**: controller chỉ nhận request/trả response; nghiệp vụ nằm trong service.
- **Module/app riêng**: `payment_app` là module riêng cho thanh toán.
- **Module gọi module khác**:
  - `PaymentService` gọi `OrderService`.
  - `OrderService` gọi `DiscountService` và `RecipeService`.
  - `InvoiceService` gọi `OrderService`.
  - Payment controller gọi `ActivityLogService`.
- **Unit test API**: `tests/test_api.py` cover các nhóm API chính.

## 4. Chức Năng Chính

- Auth: đăng ký, đăng nhập, đăng xuất, token authentication.
- Phân quyền: `admin`, `staff`, `cashier`.
- Quản lý user, danh mục, món ăn, bàn, khách hàng.
- Tạo đơn gọi món, tính tổng tiền, cập nhật trạng thái đơn.
- Thanh toán trong module riêng `payment_app`.
- Đặt bàn trước.
- Mã giảm giá/voucher.
- Quản lý nguyên liệu tồn kho.
- Công thức món/định lượng nguyên liệu.
- Trừ tồn kho khi tạo đơn.
- Hóa đơn chi tiết.
- Log hoạt động.
- Quản lý ca làm việc.
- Thống kê doanh thu, món bán chạy, doanh thu theo ngày và theo nhân viên.

## 5. Cài Đặt

Mở terminal tại thư mục project:

```powershell
cd E:\DA_Python\Nhom07_Code\sushi_restaurant_management
```

Tạo môi trường ảo:

```powershell
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Nếu dùng Command Prompt:

```bat
venv\Scripts\activate
```

Cài thư viện:

```powershell
pip install -r requirements.txt
```

## 6. Tạo Database Và Dữ Liệu Mẫu

Chạy:

```powershell
python seed.py
```

Lệnh này sẽ xóa database cũ, tạo lại toàn bộ bảng và thêm dữ liệu mẫu.

Database mặc định:

```text
database/sushi_restaurant.db
```

## 7. Chạy Server

```powershell
python run.py
```

Server mặc định chạy tại:

```text
http://127.0.0.1:5000
```

Kiểm tra server:

```http
GET http://127.0.0.1:5000/api/health
```

Kết quả mong đợi:

```json
{
  "message": "Sushi Restaurant API is running"
}
```

## 8. Tài Khoản Mẫu

Sau khi chạy `python seed.py`:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Staff | `staff` | `staff123` |
| Cashier | `cashier` | `cashier123` |

## 9. Cách Gọi API Có Token

Đăng nhập:

```http
POST /api/auth/login
```

Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Copy token trả về và thêm header:

```text
Authorization: Bearer <token>
```

## 10. Chạy Unit Test

```powershell
python -m unittest discover -s tests -v
```

Test hiện tại đã được tách theo nhóm API trong nhiều file:

```text
tests/
|-- base.py
|-- test_health_auth_user.py
|-- test_catalog_api.py
|-- test_people_table_api.py
|-- test_order_payment_api.py
|-- test_reservation_discount_inventory_api.py
`-- test_shift_log_statistics_api.py
```

Bộ test có **56 test case**:

- 54 test tương ứng 54 API endpoint.
- 2 test bổ sung cho auth guard: thiếu token và sai quyền.

## 11. Postman

Import collection:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

Luồng test cơ bản:

1. `GET /api/health`
2. `POST /api/auth/login`
3. Copy token vào header `Authorization`.
4. Tạo món/danh mục/bàn/khách hàng nếu cần.
5. `POST /api/orders`
6. `POST /api/payments`
7. `GET /api/invoices/<order_id>`
8. `GET /api/statistics`

## 12. Tổng Số Và Danh Sách API

Tổng cộng project hiện có **54 API endpoint**:

- 53 API thuộc các blueprint/module nghiệp vụ.
- 1 API health check của Flask app chính.

Thống kê theo nhóm:

| Nhóm API | Số lượng |
|---|---:|
| Health | 1 |
| Auth | 3 |
| User | 2 |
| Category | 5 |
| Menu Item | 7 |
| Table | 4 |
| Customer | 4 |
| Order | 4 |
| Payment | 2 |
| Reservation | 4 |
| Discount | 4 |
| Inventory | 4 |
| Invoice | 1 |
| Shift | 3 |
| Activity Log | 1 |
| Statistics | 5 |
| **Tổng cộng** | **54** |

### Health

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/health` | Kiểm tra server đang chạy |

### Auth

| Method | URL | Chức năng |
|---|---|---|
| POST | `/api/auth/register` | Đăng ký tài khoản |
| POST | `/api/auth/login` | Đăng nhập |
| POST | `/api/auth/logout` | Đăng xuất |

### User

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/users` | Xem danh sách người dùng |
| PUT | `/api/users/<id>/role` | Cập nhật role |

### Category

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/categories` | Danh sách danh mục |
| GET | `/api/categories/<id>` | Chi tiết danh mục |
| POST | `/api/categories` | Thêm danh mục |
| PUT | `/api/categories/<id>` | Cập nhật danh mục |
| DELETE | `/api/categories/<id>` | Xóa danh mục |

### Menu Item

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/menu-items` | Danh sách món |
| GET | `/api/menu-items/<id>` | Chi tiết món |
| POST | `/api/menu-items` | Thêm món |
| PUT | `/api/menu-items/<id>` | Cập nhật món |
| DELETE | `/api/menu-items/<id>` | Ẩn món khỏi menu |
| GET | `/api/menu-items/<id>/ingredients` | Xem công thức món |
| POST | `/api/menu-items/<id>/ingredients` | Cập nhật công thức món |

### Table

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/tables` | Danh sách bàn |
| POST | `/api/tables` | Thêm bàn |
| PUT | `/api/tables/<id>` | Cập nhật bàn |
| DELETE | `/api/tables/<id>` | Xóa bàn |

### Customer

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/customers` | Danh sách khách hàng |
| POST | `/api/customers` | Thêm khách hàng |
| PUT | `/api/customers/<id>` | Cập nhật khách hàng |
| DELETE | `/api/customers/<id>` | Xóa khách hàng |

### Order

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/orders` | Danh sách đơn |
| GET | `/api/orders/<id>` | Chi tiết đơn |
| POST | `/api/orders` | Tạo đơn gọi món |
| PUT | `/api/orders/<id>/status` | Cập nhật trạng thái đơn |

Ví dụ tạo đơn:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "discount_code": "SALE10",
  "items": [
    {"menu_item_id": 1, "quantity": 2}
  ]
}
```

### Payment

| Method | URL | Chức năng |
|---|---|---|
| POST | `/api/payments` | Thanh toán đơn |
| GET | `/api/payments` | Lịch sử thanh toán |

### Reservation

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/reservations` | Danh sách đặt bàn |
| POST | `/api/reservations` | Tạo đặt bàn |
| PUT | `/api/reservations/<id>` | Cập nhật đặt bàn |
| DELETE | `/api/reservations/<id>` | Hủy đặt bàn |

### Discount

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/discounts` | Danh sách mã giảm giá |
| POST | `/api/discounts` | Tạo mã giảm giá |
| PUT | `/api/discounts/<id>` | Cập nhật mã giảm giá |
| DELETE | `/api/discounts/<id>` | Tắt mã giảm giá |

### Inventory

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/ingredients` | Danh sách nguyên liệu |
| POST | `/api/ingredients` | Thêm nguyên liệu |
| PUT | `/api/ingredients/<id>` | Cập nhật nguyên liệu |
| DELETE | `/api/ingredients/<id>` | Xóa nguyên liệu |

### Invoice

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/invoices/<order_id>` | Xem hóa đơn chi tiết |

### Shift

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/shifts` | Danh sách ca làm |
| POST | `/api/shifts/check-in` | Bắt đầu ca |
| POST | `/api/shifts/<id>/check-out` | Kết thúc ca |

### Activity Log

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/activity-logs` | Xem lịch sử hoạt động |

### Statistics

| Method | URL | Chức năng |
|---|---|---|
| GET | `/api/statistics` | Thống kê tổng quan |
| GET | `/api/statistics/revenue` | Doanh thu theo khoảng ngày |
| GET | `/api/statistics/popular-items` | Món bán chạy |
| GET | `/api/statistics/by-day` | Doanh thu theo ngày |
| GET | `/api/statistics/by-staff` | Doanh thu theo nhân viên |

## 13. Ghi Chú

- Đơn vị tiền tệ: VND.
- `payment_app` là module riêng, được Flask app chính register trong `app/__init__.py`.
- `app/controllers/payment_controller.py` và `app/services/payment_service.py` là wrapper để giữ import cũ không bị vỡ.
- Nếu muốn reset dữ liệu demo, chạy lại `python seed.py`.
