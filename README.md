# Sushi Restaurant Management API

Backend REST API quan ly nha hang sushi, xay dung bang Python Flask. Project tap
trung vao API/server, khong co frontend, phu hop Chu de 2 cua do an.

## 1. Thong tin chung

- Nhom thuc hien: Nhom 07
- Ngon ngu: Python
- Framework: Flask
- ORM: Flask-SQLAlchemy
- Database mac dinh: SQLite
- Kiem thu: `unittest`, Postman
- Don vi tien te: VND

## 2. Kien truc source

Project to chuc theo MVC ket hop service layer:

```text
sushi_restaurant_management/
|-- app/
|   |-- controllers/        # Controller/API endpoint
|   |-- models/             # Model SQLAlchemy
|   |-- services/           # Business logic/service layer
|   |-- utils/              # Auth, response helper
|   |-- extensions.py       # Khoi tao SQLAlchemy
|   `-- __init__.py         # Tao Flask app, register blueprint
|-- payment_app/            # Module rieng cho thanh toan
|-- database/               # SQLite database va schema tom tat
|-- docs/                   # Tai lieu source/API
|-- postman/                # Postman collection
|-- tests/                  # Unit test va integration test tuy chon
|-- config.py
|-- run.py
|-- seed.py
`-- requirements.txt
```

Chi tiet kien truc: `docs/Source_Architecture.md`.

## 3. Diem dap ung yeu cau Chu de 2

- Co REST API backend, khong yeu cau giao dien frontend.
- Co CSDL SQLite voi 10 bang chinh, dung gioi han 5-10 bang.
- Co API dang ky, dang nhap, dang xuat va Bearer token.
- Co toi thieu hai doi tuong nguoi dung: `admin`, `staff`, `cashier`; trong do `admin` la quan tri vien, `staff/cashier` la nguoi dung da dang ky theo vai tro nghiep vu.
- Co REST API dung `GET`, `POST`, `PUT`, `DELETE`.
- Co Postman collection de kiem thu API.
- Co unit test tu dong cho cac nhom API chinh.
- Ap dung OOP, MVC va service layer.

## 4. Chuc nang chinh

- Auth: dang ky, dang nhap, dang xuat.
- User: xem danh sach user, cap nhat role.
- Category: CRUD danh muc mon.
- Menu Item: xem menu public, CRUD/an mon.
- Table: quan ly ban va giu ban tam 15 phut.
- Customer: quan ly khach hang.
- Order: tao don goi mon, xem don, cap nhat trang thai.
- Payment: thanh toan don va xem lich su thanh toan.
- Invoice: xem hoa don chi tiet cho don da thanh toan.
- Statistics: tong quan doanh thu, doanh thu theo ngay/nhan vien, mon ban chay.

## 5. Cai dat

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Neu dung Command Prompt:

```bat
venv\Scripts\activate
```

## 6. Tao database va du lieu mau

```powershell
python seed.py
```

Lenh nay xoa database cu, tao lai bang va them du lieu mau.

Tai khoan mau:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Staff | `staff` | `staff123` |
| Cashier | `cashier` | `cashier123` |

## 7. Chay server

```powershell
python run.py
```

Server mac dinh:

```text
http://127.0.0.1:5000
```

Kiem tra:

```http
GET http://127.0.0.1:5000/api/health
```

## 8. Cach goi API co token

Dang nhap:

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

Them token vao header:

```text
Authorization: Bearer <token>
```

## 9. Chay test

Chay unit test:

```powershell
python -m unittest discover -s tests/unittest -v
```

Ket qua kiem tra gan nhat: 42 test passed.

Integration test voi database that duoc skip mac dinh de tranh ghi vao DB dang dung:

```powershell
$env:RUN_REAL_DB_TESTS='1'
python -m unittest tests.test_all_api -v
```

## 10. Postman

Import collection:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

Thu tu demo de xuat:

1. Health va Auth.
2. Admin tao category, menu item, table.
3. Staff tao customer va order.
4. Cashier/Admin/Staff thanh toan order.
5. Xem invoice va statistics.

## 11. Danh sach API thuc te

Tong cong co 36 endpoint dang duoc register trong Flask app.

| Nhom | So API |
|---|---:|
| Health | 1 |
| Auth | 3 |
| User | 2 |
| Category | 5 |
| Menu Item | 5 |
| Table | 4 |
| Customer | 4 |
| Order | 4 |
| Payment | 2 |
| Invoice | 1 |
| Statistics | 5 |
| **Tong** | **36** |

### Health

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/health` | Kiem tra server |

### Auth

| Method | URL | Chuc nang |
|---|---|---|
| POST | `/api/auth/register` | Dang ky |
| POST | `/api/auth/login` | Dang nhap |
| POST | `/api/auth/logout` | Dang xuat |

### User

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/users` | Danh sach user |
| PUT | `/api/users/<id>/role` | Cap nhat role |

### Category

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/categories` | Danh sach danh muc |
| GET | `/api/categories/<id>` | Chi tiet danh muc |
| POST | `/api/categories` | Them danh muc |
| PUT | `/api/categories/<id>` | Cap nhat danh muc |
| DELETE | `/api/categories/<id>` | Xoa danh muc |

### Menu Item

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/menu-items` | Danh sach mon |
| GET | `/api/menu-items/<id>` | Chi tiet mon |
| POST | `/api/menu-items` | Them mon |
| PUT | `/api/menu-items/<id>` | Cap nhat mon |
| DELETE | `/api/menu-items/<id>` | An mon khoi menu |

### Table

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/tables` | Danh sach ban |
| POST | `/api/tables` | Them ban |
| PUT | `/api/tables/<id>` | Cap nhat ban |
| DELETE | `/api/tables/<id>` | Xoa ban |

### Customer

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/customers` | Danh sach khach hang |
| POST | `/api/customers` | Them khach hang |
| PUT | `/api/customers/<id>` | Cap nhat khach hang |
| DELETE | `/api/customers/<id>` | Xoa khach hang |

### Order

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/orders` | Danh sach don |
| GET | `/api/orders/<id>` | Chi tiet don |
| POST | `/api/orders` | Tao don goi mon |
| PUT | `/api/orders/<id>/status` | Cap nhat trang thai don |

### Payment

| Method | URL | Chuc nang |
|---|---|---|
| POST | `/api/payments` | Thanh toan don |
| GET | `/api/payments` | Lich su thanh toan |

### Invoice

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/invoices/<order_id>` | Hoa don chi tiet |

### Statistics

| Method | URL | Chuc nang |
|---|---|---|
| GET | `/api/statistics` | Thong ke tong quan |
| GET | `/api/statistics/revenue` | Doanh thu theo khoang ngay |
| GET | `/api/statistics/popular-items` | Mon ban chay |
| GET | `/api/statistics/by-day` | Doanh thu theo ngay |
| GET | `/api/statistics/by-staff` | Doanh thu theo nhan vien |
