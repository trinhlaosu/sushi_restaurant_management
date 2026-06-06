# API Detailed Specification

Tai lieu nay mo ta cac API thuc te cua Sushi Restaurant Management. Danh sach
khop voi Flask route map hien tai: 36 endpoint.

## 1. Quy uoc chung

Base URL:

```text
http://127.0.0.1:5000
```

Header cho API can dang nhap:

```text
Authorization: Bearer <token>
Content-Type: application/json
```

Role hien co:

| Role | Y nghia |
|---|---|
| `admin` | Quan tri he thong, quan ly master data, user, bao cao |
| `staff` | Nhan vien phuc vu, tao order, quan ly khach/ban |
| `cashier` | Thu ngan, thanh toan va xem lich su thanh toan/hoa don |

Response pattern:

- Tao moi: thuong tra `201`.
- Cap nhat/xoa/thao tac: thuong tra `200`.
- Thieu token: `401`.
- Sai role: `403`.
- ID khong ton tai qua `get_or_404`: `404`.

## 2. Health

### GET `/api/health`

- Quyen: public.
- Muc dich: kiem tra server dang chay.
- Response:

```json
{
  "message": "Sushi Restaurant API is running"
}
```

## 3. Auth

### POST `/api/auth/register`

- Quyen: public.
- Muc dich: tao tai khoan moi.
- Body:

```json
{
  "full_name": "New Staff",
  "username": "new_staff",
  "password": "new123"
}
```

- Rule:
  - `full_name`, `username`, `password` bat buoc.
  - Username khong duoc trung.
  - User moi mac dinh role `staff`.

### POST `/api/auth/login`

- Quyen: public.
- Muc dich: dang nhap va cap access token.
- Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

- Rule:
  - Sai username/password tra loi dang nhap that bai.
  - Moi lan login tao token moi trong bang `access_tokens`.

### POST `/api/auth/logout`

- Quyen: `admin`, `staff`, `cashier`.
- Muc dich: revoke token hien tai.
- Rule:
  - Sau logout, token cu khong dung duoc cho API protected.

## 4. User

### GET `/api/users`

- Quyen: `admin`.
- Muc dich: xem danh sach user.
- Rule: staff/cashier bi chan boi role guard.

### PUT `/api/users/<user_id>/role`

- Quyen: `admin`.
- Muc dich: doi role cua user.
- Body:

```json
{
  "role": "cashier"
}
```

- Rule:
  - Role phai ton tai trong bang `roles`.
  - User khong ton tai tra `404`.

## 5. Category

### GET `/api/categories`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach danh muc mon.

### GET `/api/categories/<id>`

- Quyen: `admin`, `staff`.
- Muc dich: xem chi tiet danh muc.

### POST `/api/categories`

- Quyen: `admin`.
- Muc dich: tao danh muc.
- Body:

```json
{
  "name": "Sashimi",
  "description": "Raw fish"
}
```

### PUT `/api/categories/<id>`

- Quyen: `admin`.
- Muc dich: cap nhat danh muc.

### DELETE `/api/categories/<id>`

- Quyen: `admin`.
- Muc dich: xoa danh muc.

## 6. Menu Item

### GET `/api/menu-items`

- Quyen: public.
- Muc dich: xem menu ban hang.

### GET `/api/menu-items/<id>`

- Quyen: public.
- Muc dich: xem chi tiet mon.

### POST `/api/menu-items`

- Quyen: `admin`.
- Muc dich: them mon moi vao menu.
- Body:

```json
{
  "name": "Tuna Nigiri",
  "description": "Tuna sushi",
  "price": 42000,
  "category_id": 1
}
```

- Rule:
  - Gia phai hop le.
  - `category_id` phai ton tai.

### PUT `/api/menu-items/<id>`

- Quyen: `admin`.
- Muc dich: cap nhat mon.
- Body vi du:

```json
{
  "price": 50000,
  "status": "con_mon",
  "is_available": true
}
```

### DELETE `/api/menu-items/<id>`

- Quyen: `admin`.
- Muc dich: an mon khoi menu.
- Rule: delete la xoa mem, set `is_available = false`.

## 7. Table

### GET `/api/tables`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach ban.
- Side effect: giai phong ban `da_dat` da qua han.

### POST `/api/tables`

- Quyen: `admin`.
- Muc dich: tao ban moi.
- Body:

```json
{
  "table_number": "B20",
  "seats": 4,
  "status": "trong"
}
```

- Rule:
  - `table_number` bat buoc va khong trung.
  - `seats > 0`.
  - Status hop le: `trong`, `da_dat`, `dang_phuc_vu`.
  - Status `da_dat` set thoi gian giu ban 15 phut.

### PUT `/api/tables/<table_id>`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat ban/trang thai ban.

### DELETE `/api/tables/<table_id>`

- Quyen: `admin`.
- Muc dich: xoa ban.

## 8. Customer

### GET `/api/customers`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach khach hang.

### POST `/api/customers`

- Quyen: `admin`, `staff`.
- Muc dich: tao khach hang.
- Body:

```json
{
  "full_name": "Nguyen Van A",
  "phone": "0900000001",
  "customer_type": "thanh_vien",
  "member_tier": "vang",
  "birth_date": "1998-06-12",
  "note": "VIP"
}
```

- Rule:
  - `full_name` bat buoc.
  - `customer_type` va `member_tier` phai hop le.
  - Neu `customer_type = khach_le`, service reset `member_tier = thuong` va `birth_date = None`.

### PUT `/api/customers/<customer_id>`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat khach hang.

### DELETE `/api/customers/<customer_id>`

- Quyen: `admin`.
- Muc dich: xoa khach hang.

## 9. Order

### GET `/api/orders`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach order.
- Side effect: giai phong ban dat qua han.

### GET `/api/orders/<order_id>`

- Quyen: `admin`, `staff`.
- Muc dich: xem chi tiet order kem danh sach mon.

### POST `/api/orders`

- Quyen: `admin`, `staff`.
- Muc dich: tao don goi mon.
- Body:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    }
  ]
}
```

- Luong chay:
  1. Controller gan `user_id = g.current_user.id`.
  2. Service kiem tra `items` khong rong.
  3. Kiem tra ban ton tai va khong dang `dang_phuc_vu`.
  4. Tao `Order` status `dang_xu_ly`.
  5. Tao `OrderDetail` cho tung item hop le.
  6. Tinh `total_amount` va `final_amount`.
  7. Chuyen ban sang `dang_phuc_vu`.
  8. Commit DB.

- Rule:
  - So luong mon phai lon hon 0.
  - Mon phai ton tai, `is_available = true`, `status = con_mon`.

### PUT `/api/orders/<order_id>/status`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat trang thai order.
- Body:

```json
{
  "status": "da_phuc_vu"
}
```

- Rule:
  - Status hop le: `dang_xu_ly`, `da_phuc_vu`, `da_thanh_toan`, `da_huy`.
  - Don da thanh toan khong duoc huy.
  - Status `da_thanh_toan` hoac `da_huy` giai phong ban ve `trong`.

## 10. Payment

### POST `/api/payments`

- Quyen: `admin`, `staff`, `cashier`.
- Muc dich: thanh toan order.
- Body:

```json
{
  "order_id": 1,
  "payment_method": "tien_mat"
}
```

- Luong chay:
  1. Lay order qua `OrderService.get_by_id`.
  2. Kiem tra order chua co payment.
  3. Tao `Payment` voi amount = `order.final_amount`.
  4. Cap nhat order sang `da_thanh_toan`.
  5. Giai phong ban ve `trong`.

- Rule:
  - Mot order chi thanh toan mot lan.
  - Order da huy khong duoc thanh toan.

### GET `/api/payments`

- Quyen: `admin`, `cashier`.
- Muc dich: xem lich su thanh toan.

## 11. Invoice

### GET `/api/invoices/<order_id>`

- Quyen: `admin`, `staff`, `cashier`.
- Muc dich: lay hoa don chi tiet cho order da thanh toan.
- Rule:
  - Order chua thanh toan chua co invoice hop le.
  - `invoice_code` co dang `HD000001`.

## 12. Statistics

### GET `/api/statistics`

- Quyen: `admin`.
- Muc dich: thong ke tong quan.
- Response gom:
  - `tong_don_da_thanh_toan`
  - `tong_doanh_thu`
  - `top_5_mon_ban_chay`
  - `currency = VND`

### GET `/api/statistics/revenue`

- Quyen: `admin`.
- Query params:

```text
?tu_ngay=2026-06-01&den_ngay=2026-06-30
```

- Muc dich: doanh thu theo khoang ngay.

### GET `/api/statistics/popular-items`

- Quyen: `admin`.
- Query params:

```text
?top=5
```

- Muc dich: mon ban chay theo so luong.

### GET `/api/statistics/by-day`

- Quyen: `admin`.
- Muc dich: doanh thu group theo ngay.

### GET `/api/statistics/by-staff`

- Quyen: `admin`.
- Muc dich: doanh thu group theo nhan vien tao order.

## 13. Danh sach API nhanh

| Method | URL | Quyen | Nhom |
|---|---|---|---|
| GET | `/api/health` | public | Health |
| POST | `/api/auth/register` | public | Auth |
| POST | `/api/auth/login` | public | Auth |
| POST | `/api/auth/logout` | admin, staff, cashier | Auth |
| GET | `/api/users` | admin | User |
| PUT | `/api/users/<id>/role` | admin | User |
| GET | `/api/categories` | admin, staff | Category |
| GET | `/api/categories/<id>` | admin, staff | Category |
| POST | `/api/categories` | admin | Category |
| PUT | `/api/categories/<id>` | admin | Category |
| DELETE | `/api/categories/<id>` | admin | Category |
| GET | `/api/menu-items` | public | Menu |
| GET | `/api/menu-items/<id>` | public | Menu |
| POST | `/api/menu-items` | admin | Menu |
| PUT | `/api/menu-items/<id>` | admin | Menu |
| DELETE | `/api/menu-items/<id>` | admin | Menu |
| GET | `/api/tables` | admin, staff | Table |
| POST | `/api/tables` | admin | Table |
| PUT | `/api/tables/<id>` | admin, staff | Table |
| DELETE | `/api/tables/<id>` | admin | Table |
| GET | `/api/customers` | admin, staff | Customer |
| POST | `/api/customers` | admin, staff | Customer |
| PUT | `/api/customers/<id>` | admin, staff | Customer |
| DELETE | `/api/customers/<id>` | admin | Customer |
| GET | `/api/orders` | admin, staff | Order |
| GET | `/api/orders/<id>` | admin, staff | Order |
| POST | `/api/orders` | admin, staff | Order |
| PUT | `/api/orders/<id>/status` | admin, staff | Order |
| POST | `/api/payments` | admin, staff, cashier | Payment |
| GET | `/api/payments` | admin, cashier | Payment |
| GET | `/api/invoices/<order_id>` | admin, staff, cashier | Invoice |
| GET | `/api/statistics` | admin | Statistics |
| GET | `/api/statistics/revenue` | admin | Statistics |
| GET | `/api/statistics/popular-items` | admin | Statistics |
| GET | `/api/statistics/by-day` | admin | Statistics |
| GET | `/api/statistics/by-staff` | admin | Statistics |
