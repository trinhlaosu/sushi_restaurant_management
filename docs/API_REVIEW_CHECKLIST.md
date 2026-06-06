# API Review Checklist

Tai lieu nay dung de duyet API thuc te cua project Sushi Restaurant Management.
Danh sach ben duoi khop voi route map hien tai trong `app/__init__.py`: 36 endpoint.

## 1. Chuan bi moi truong

```powershell
python seed.py
python run.py
```

Base URL:

```text
http://127.0.0.1:5000
```

Tai khoan mau:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Staff | `staff` | `staff123` |
| Cashier | `cashier` | `cashier123` |

Header cho API can dang nhap:

```text
Authorization: Bearer <token>
Content-Type: application/json
```

## 2. Thu tu demo de xuat

1. Goi `GET /api/health`.
2. Dang nhap admin, staff, cashier de lay token.
3. Admin tao/cap nhat category, menu item, table.
4. Staff tao customer va order.
5. Cashier hoac staff thanh toan order.
6. Xem invoice.
7. Admin xem statistics.
8. Test loi phan quyen: thieu token, sai role, token da logout.

## 3. Checklist tong quan

| Nhom | So API | Trang thai |
|---|---:|---|
| Health | 1 | [ ] |
| Auth | 3 | [ ] |
| User | 2 | [ ] |
| Category | 5 | [ ] |
| Menu Item | 5 | [ ] |
| Table | 4 | [ ] |
| Customer | 4 | [ ] |
| Order | 4 | [ ] |
| Payment | 2 | [ ] |
| Invoice | 1 | [ ] |
| Statistics | 5 | [ ] |
| **Tong** | **36** | [ ] |

## 4. Public va Auth

### GET `/api/health`

- Role: public.
- Expected: `200`.
- Can kiem tra:
  - [ ] Response co `message = "Sushi Restaurant API is running"`.
  - [ ] Khong can token.

### POST `/api/auth/register`

- Role: public.
- Body mau:

```json
{
  "full_name": "New Staff",
  "username": "new_staff",
  "password": "new123"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] User moi duoc tao.
  - [ ] Role mac dinh la `staff`.
  - [ ] Username trung bi bao loi.

### POST `/api/auth/login`

- Role: public.
- Expected: `200`.
- Can kiem tra:
  - [ ] Response co `token`.
  - [ ] Sai username/password bi tu choi.

### POST `/api/auth/logout`

- Role: `admin`, `staff`, `cashier`.
- Expected: `200`.
- Can kiem tra:
  - [ ] Token hien tai bi revoke.
  - [ ] Token da logout goi API protected bi `401`.

## 5. User

### GET `/api/users`

- Role: `admin`.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach user.
  - [ ] Staff/cashier bi `403`.
  - [ ] Thieu token bi `401`.

### PUT `/api/users/<id>/role`

- Role: `admin`.
- Body mau:

```json
{
  "role": "cashier"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Role user duoc cap nhat dung.
  - [ ] Role khong ton tai bi bao loi.

## 6. Category

- [ ] `GET /api/categories`: admin/staff xem danh sach.
- [ ] `GET /api/categories/<id>`: admin/staff xem chi tiet.
- [ ] `POST /api/categories`: admin tao danh muc.
- [ ] `PUT /api/categories/<id>`: admin cap nhat danh muc.
- [ ] `DELETE /api/categories/<id>`: admin xoa danh muc.

Body tao mau:

```json
{
  "name": "Sashimi",
  "description": "Raw fish"
}
```

Can test them: thieu `name`, ID khong ton tai, staff tao/sua/xoa bi `403`.

## 7. Menu Item

- [ ] `GET /api/menu-items`: public xem menu.
- [ ] `GET /api/menu-items/<id>`: public xem chi tiet mon.
- [ ] `POST /api/menu-items`: admin them mon.
- [ ] `PUT /api/menu-items/<id>`: admin cap nhat mon.
- [ ] `DELETE /api/menu-items/<id>`: admin an mon khoi menu.

Body tao mau:

```json
{
  "name": "Tuna Nigiri",
  "description": "Tuna sushi",
  "price": 42000,
  "category_id": 1
}
```

Can test them: gia am, category khong ton tai, mon bi an khong tao order duoc.

## 8. Table

- [ ] `GET /api/tables`: admin/staff xem danh sach ban.
- [ ] `POST /api/tables`: admin tao ban.
- [ ] `PUT /api/tables/<id>`: admin/staff cap nhat ban.
- [ ] `DELETE /api/tables/<id>`: admin xoa ban.

Body tao mau:

```json
{
  "table_number": "B20",
  "seats": 4,
  "status": "trong"
}
```

Can test them: `table_number` trung, `seats <= 0`, status khong hop le, giu ban `da_dat` het han sau 15 phut.

## 9. Customer

- [ ] `GET /api/customers`: admin/staff xem danh sach.
- [ ] `POST /api/customers`: admin/staff tao khach.
- [ ] `PUT /api/customers/<id>`: admin/staff cap nhat khach.
- [ ] `DELETE /api/customers/<id>`: admin xoa khach.

Body tao mau:

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

Can test them: thieu ten, loai khach/hang thanh vien khong hop le.

## 10. Order

- [ ] `GET /api/orders`: admin/staff xem danh sach don.
- [ ] `GET /api/orders/<id>`: admin/staff xem chi tiet don.
- [ ] `POST /api/orders`: admin/staff tao don.
- [ ] `PUT /api/orders/<id>/status`: admin/staff cap nhat trang thai.

Body tao mau:

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

Can test them:

- [ ] Don phai co item.
- [ ] So luong mon phai lon hon 0.
- [ ] Ban dang `dang_phuc_vu` khong tao don moi.
- [ ] Mon `het_mon` hoac `is_available = false` bi chan.
- [ ] Tao order tinh dung `total_amount` va `final_amount`.
- [ ] Tao order chuyen ban sang `dang_phuc_vu`.
- [ ] Status hop le: `dang_xu_ly`, `da_phuc_vu`, `da_thanh_toan`, `da_huy`.

## 11. Payment

- [ ] `POST /api/payments`: admin/staff/cashier thanh toan don.
- [ ] `GET /api/payments`: admin/cashier xem lich su thanh toan.

Body tao mau:

```json
{
  "order_id": 1,
  "payment_method": "tien_mat"
}
```

Can test them:

- [ ] Payment amount bang `order.final_amount`.
- [ ] Order chuyen sang `da_thanh_toan`.
- [ ] Ban ve `trong`.
- [ ] Thanh toan lai cung order bi chan.
- [ ] Staff tao payment duoc nhung khong xem danh sach payment.

## 12. Invoice

### GET `/api/invoices/<order_id>`

- Role: `admin`, `staff`, `cashier`.
- Expected: `200` voi order da thanh toan.
- Can kiem tra:
  - [ ] Response co `invoice_code`, item, subtotal, total amount, payment.
  - [ ] Order chua thanh toan bi bao loi.

## 13. Statistics

- [ ] `GET /api/statistics`: admin xem tong quan.
- [ ] `GET /api/statistics/revenue`: admin xem doanh thu theo khoang ngay.
- [ ] `GET /api/statistics/popular-items?top=5`: admin xem mon ban chay.
- [ ] `GET /api/statistics/by-day`: admin xem doanh thu theo ngay.
- [ ] `GET /api/statistics/by-staff`: admin xem doanh thu theo nhan vien.

Can test them:

- [ ] Chi tinh order co status `da_thanh_toan`.
- [ ] Tong doanh thu khop payment/order da thanh toan.
- [ ] Staff/cashier bi chan `403`.

## 14. Checklist loi va phan quyen

- [ ] API public khong can token: health, login, register, menu list/detail.
- [ ] API admin bi chan khi dung staff/cashier token.
- [ ] Thieu token tra `401`.
- [ ] Token da logout tra `401`.
- [ ] ID khong ton tai tra loi ro rang, khong crash server.
- [ ] Body thieu field bat buoc tra loi ro rang.
- [ ] Du lieu trung unique field nhu username, table_number duoc chan.
- [ ] Gia tien, so luong, so ghe khong nhan gia tri am.

## 15. Lenh test tu dong

```powershell
python -m unittest discover -s tests/unittest -v
```

Integration test voi database that:

```powershell
$env:RUN_REAL_DB_TESTS='1'
python -m unittest tests.test_all_api -v
```
