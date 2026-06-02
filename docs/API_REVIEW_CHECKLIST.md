# API Review Checklist

Tai lieu nay dung de duyet tung API cua project Sushi Restaurant Management, kiem tra:

- API co chay dung method, URL, role va status code mong doi khong.
- Payload dau vao co tao/cap nhat dung du lieu khong.
- Luong nghiep vu giua cac module co lien ket dung khong.
- Phan quyen, token va cac case loi co duoc chan dung khong.

## 1. Chuan bi moi truong

Chay lai database mau:

```powershell
python seed.py
```

Chay server:

```powershell
python run.py
```

Base URL:

```text
http://127.0.0.1:5000
```

Tai khoan mau:

| Role | Username | Password | Token bien goi y |
|---|---|---|---|
| Admin | `admin` | `admin123` | `admin_token` |
| Staff | `staff` | `staff123` | `staff_token` |
| Cashier | `cashier` | `cashier123` | `cashier_token` |

Header cho API can dang nhap:

```text
Authorization: Bearer <token>
Content-Type: application/json
```

## 2. Thu tu duyet API de kiem tra luong

Nen duyet theo thu tu nay de tranh thieu du lieu phu thuoc:

1. Public va Auth.
2. Admin tao du lieu nen: category, menu item, table, discount, ingredient, recipe.
3. Staff tao customer, reservation, shift, order.
4. Cashier thanh toan order va xem invoice.
5. Admin xem activity log, statistics va kiem tra cleanup/logout.

## 3. Checklist tong quan

| Nhom | So API | Trang thai |
|---|---:|---|
| Health | 1 | [ ] |
| Auth | 3 | [ ] |
| User | 2 | [ ] |
| Category | 5 | [ ] |
| Menu Item + Recipe | 7 | [ ] |
| Table | 4 | [ ] |
| Customer | 4 | [ ] |
| Order | 4 | [ ] |
| Payment | 2 | [ ] |
| Reservation | 4 | [ ] |
| Discount | 4 | [ ] |
| Inventory | 4 | [ ] |
| Invoice | 1 | [ ] |
| Shift | 3 | [ ] |
| Activity Log | 1 | [ ] |
| Statistics | 5 | [ ] |

## 4. Public va Auth

### GET `/api/health`

- Role: public.
- Muc dich: kiem tra server dang chay.
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
- Body mau:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Response co `token`.
  - [ ] Luu token de goi API can quyen.
  - [ ] Sai username/password bi tu choi.

### POST `/api/auth/logout`

- Role: user da dang nhap.
- Expected: `200`.
- Can kiem tra:
  - [ ] Sau logout, token cu goi API protected bi `401`.

## 5. User

### GET `/api/users`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach user.
  - [ ] Staff/cashier goi API nay bi `403`.
  - [ ] Thieu token bi `401`.

### PUT `/api/users/<id>/role`

- Role: admin.
- Body mau:

```json
{
  "role": "admin"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Role user duoc cap nhat dung.
  - [ ] Role khong hop le bi bao loi.

## 6. Category

### GET `/api/categories`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach category.

### GET `/api/categories/<id>`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] ID hop le tra dung chi tiet.
  - [ ] ID khong ton tai tra loi phu hop.

### POST `/api/categories`

- Role: admin.
- Body mau:

```json
{
  "name": "Sashimi",
  "description": "Raw fish"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Category moi duoc tao.
  - [ ] Thieu `name` bi bao loi.

### PUT `/api/categories/<id>`

- Role: admin.
- Body mau:

```json
{
  "name": "Updated Temp"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Du lieu category duoc cap nhat.

### DELETE `/api/categories/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Category bi xoa hoac khong con hien thi trong danh sach.

## 7. Menu Item va Recipe

### GET `/api/menu-items`

- Role: public.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach mon dang co san.
  - [ ] Mon da bi an/xoa mem khong nen hien thi nhu mon dang ban neu service dang xu ly theo `is_available`.

### GET `/api/menu-items/<id>`

- Role: public.
- Expected: `200`.
- Can kiem tra:
  - [ ] ID hop le tra dung mon.

### POST `/api/menu-items`

- Role: admin.
- Body mau:

```json
{
  "name": "Tuna Nigiri",
  "description": "Tuna sushi",
  "price": 42000,
  "category_id": 1
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Mon moi co gia, category dung.
  - [ ] `price` am hoac `category_id` khong ton tai bi bao loi.

### PUT `/api/menu-items/<id>`

- Role: admin.
- Body mau:

```json
{
  "price": 50000,
  "is_available": true
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Gia/status mon duoc cap nhat.

### DELETE `/api/menu-items/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Mon khong bi xoa cung khoi DB neu dang xoa mem.
  - [ ] `is_available` chuyen thanh `false`.

### GET `/api/menu-items/<id>/ingredients`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach nguyen lieu trong cong thuc mon.

### POST `/api/menu-items/<id>/ingredients`

- Role: admin.
- Body mau:

```json
{
  "ingredients": [
    {
      "ingredient_id": 1,
      "quantity": 10
    }
  ]
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Cong thuc duoc gan/cap nhat dung.
  - [ ] Nguyen lieu khong ton tai hoac quantity <= 0 bi bao loi.

## 8. Table

### GET `/api/tables`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach ban va trang thai.

### POST `/api/tables`

- Role: admin.
- Body mau:

```json
{
  "table_number": "B02",
  "seats": 6,
  "status": "trong"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Ban moi duoc tao.
  - [ ] `table_number` trung bi bao loi.

### PUT `/api/tables/<id>`

- Role: staff/admin.
- Body mau:

```json
{
  "status": "dang_phuc_vu"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Trang thai ban duoc cap nhat.

### DELETE `/api/tables/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Ban bi xoa hoac khong con duoc tra ve.

## 9. Customer

### GET `/api/customers`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach khach hang.

### POST `/api/customers`

- Role: staff/admin.
- Body mau:

```json
{
  "full_name": "Nguyen Van A",
  "phone": "0900000001",
  "note": "VIP"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Khach hang moi duoc tao.
  - [ ] Phone trung hoac sai dinh dang neu co validate thi bi bao loi.

### PUT `/api/customers/<id>`

- Role: staff/admin.
- Body mau:

```json
{
  "note": "VIP"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Thong tin khach hang duoc cap nhat.

### DELETE `/api/customers/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Khach hang bi xoa hoac khong con hien thi.

## 10. Reservation

### GET `/api/reservations`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach dat ban.

### POST `/api/reservations`

- Role: staff/admin.
- Body mau:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "reservation_time": "2030-01-01T18:00:00",
  "guest_count": 2,
  "note": "Dat ban buoi toi"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Tao reservation thanh cong.
  - [ ] Trung ban cung khung gio bi chan.
  - [ ] `guest_count` vuot so ghe nen duoc xu ly dung theo rule service.

### PUT `/api/reservations/<id>`

- Role: staff/admin.
- Body mau:

```json
{
  "status": "da_xac_nhan"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Trang thai dat ban duoc cap nhat.

### DELETE `/api/reservations/<id>`

- Role: staff/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Reservation bi huy/xoa dung rule.

## 11. Discount

### GET `/api/discounts`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach ma giam gia.

### POST `/api/discounts`

- Role: admin.
- Body mau:

```json
{
  "code": "SALE10",
  "discount_type": "percent",
  "value": 10,
  "usage_limit": 5
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Ma giam gia duoc tao.
  - [ ] Code trung bi bao loi.
  - [ ] `percent` vuot 100 hoac value am bi bao loi.

### PUT `/api/discounts/<id>`

- Role: admin.
- Body mau:

```json
{
  "value": 15
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Gia tri giam gia duoc cap nhat.

### DELETE `/api/discounts/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Voucher bi tat hoac xoa dung rule.

## 12. Inventory

### GET `/api/ingredients`

- Role: staff tro len.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach nguyen lieu va ton kho.

### POST `/api/ingredients`

- Role: admin.
- Body mau:

```json
{
  "name": "Salmon",
  "unit": "gram",
  "stock_quantity": 100,
  "min_quantity": 10
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Nguyen lieu duoc tao.
  - [ ] Ton kho ban dau dung.

### PUT `/api/ingredients/<id>`

- Role: admin.
- Body mau:

```json
{
  "min_quantity": 5
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Thong tin ton kho duoc cap nhat.

### DELETE `/api/ingredients/<id>`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Nguyen lieu bi xoa hoac khong con duoc dung trong recipe.

## 13. Order

### GET `/api/orders`

- Role: staff/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach order.
  - [ ] Danh sach khong can tra chi tiet `details` day du neu API dang toi uu response list.

### GET `/api/orders/<id>`

- Role: staff/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra dung order va cac item trong order.

### POST `/api/orders`

- Role: staff/admin.
- Body mau:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "discount_code": "SALE10",
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    }
  ]
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Tong tien tinh dung theo gia mon va so luong.
  - [ ] Voucher duoc ap dung neu hop le.
  - [ ] Ton kho nguyen lieu bi tru theo recipe.
  - [ ] Ban chuyen sang trang thai phu hop neu service co xu ly.
  - [ ] Mon het hang/khong du nguyen lieu bi chan.

### PUT `/api/orders/<id>/status`

- Role: staff/admin.
- Body mau:

```json
{
  "status": "da_phuc_vu"
}
```

- Expected: `200`.
- Can kiem tra:
  - [ ] Trang thai order duoc cap nhat.
  - [ ] Trang thai khong hop le bi bao loi.

## 14. Payment

### POST `/api/payments`

- Role: cashier/admin.
- Body mau:

```json
{
  "order_id": 1,
  "payment_method": "tien_mat"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Payment duoc tao voi amount bang tong tien order.
  - [ ] Order chuyen sang trang thai da thanh toan.
  - [ ] Activity log co action `create_payment`.
  - [ ] Thanh toan lai cung order bi chan.

### GET `/api/payments`

- Role: cashier/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra lich su thanh toan.
  - [ ] Payment vua tao co trong danh sach.

## 15. Invoice

### GET `/api/invoices/<order_id>`

- Role: staff/cashier/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Chi tao/tra invoice cho order da thanh toan.
  - [ ] Response co `invoice_code`, thong tin order, item, amount.
  - [ ] Order chua thanh toan bi bao loi.

## 16. Shift

### GET `/api/shifts`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tra danh sach ca lam.

### POST `/api/shifts/check-in`

- Role: staff/admin.
- Body mau:

```json
{
  "user_id": 2,
  "note": "Morning shift"
}
```

- Expected: `201`.
- Can kiem tra:
  - [ ] Tao ca moi voi `is_active = true`.
  - [ ] User dang co ca active thi check-in lai bi chan.

### POST `/api/shifts/<id>/check-out`

- Role: staff/admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Ca lam chuyen sang `is_active = false`.
  - [ ] Co thoi gian checkout.

## 17. Activity Log

### GET `/api/activity-logs`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Sau khi thanh toan co log `create_payment`.
  - [ ] Log co user/action/thoi gian du ro de audit.

## 18. Statistics

### GET `/api/statistics`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tong doanh thu tinh tu cac payment/order da thanh toan.
  - [ ] So don, so payment, so mon ban ra neu co field tuong ung la hop ly.

### GET `/api/statistics/revenue`

- Role: admin.
- Query goi y: `?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD`.
- Expected: `200`.
- Can kiem tra:
  - [ ] Tong doanh thu theo khoang ngay dung.
  - [ ] Khong truyen ngay thi tra mac dinh dung theo service.

### GET `/api/statistics/popular-items?top=5`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Mon ban chay sap xep theo tong so luong giam dan.
  - [ ] Tham so `top` gioi han dung so dong.

### GET `/api/statistics/by-day`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Doanh thu group theo ngay dung.

### GET `/api/statistics/by-staff`

- Role: admin.
- Expected: `200`.
- Can kiem tra:
  - [ ] Doanh thu group theo nhan vien tao/phu trach order dung.

## 19. Checklist phan quyen va loi nen test them

- [ ] API public khong can token: health, login, register, list/detail menu item.
- [ ] API admin bi chan khi dung staff/cashier token.
- [ ] API cashier bi chan khi dung staff token neu khong du quyen.
- [ ] Thieu token tra `401`.
- [ ] Token da logout tra `401`.
- [ ] ID khong ton tai tra loi ro rang, khong crash server.
- [ ] Body thieu field bat buoc tra loi ro rang.
- [ ] Du lieu trung unique field nhu username, table_number, discount code duoc chan.
- [ ] Gia tien, so luong, ton kho, so ghe, percent discount khong nhan gia tri am.

## 20. Luong nghiep vu can duyet ky

### Luong tao order va tru kho

1. Admin tao ingredient.
2. Admin gan recipe cho menu item.
3. Staff tao order voi menu item do.
4. Kiem tra:
   - [ ] Order tao thanh cong.
   - [ ] `total_amount` dung.
   - [ ] Stock ingredient giam dung theo `quantity order * quantity recipe`.
   - [ ] Neu stock khong du thi order bi chan.

### Luong voucher

1. Admin tao discount.
2. Staff tao order kem `discount_code`.
3. Kiem tra:
   - [ ] Tong tien sau giam dung.
   - [ ] Voucher het luot/khong active/khong ton tai bi chan hoac khong duoc ap dung theo rule service.

### Luong thanh toan va hoa don

1. Staff tao order.
2. Cashier goi `POST /api/payments`.
3. Cashier/staff goi `GET /api/invoices/<order_id>`.
4. Kiem tra:
   - [ ] Payment amount dung.
   - [ ] Order da thanh toan.
   - [ ] Invoice co ma hoa don va chi tiet mon.
   - [ ] Activity log ghi nhan thanh toan.

### Luong bao cao

1. Tao va thanh toan it nhat 1 order.
2. Goi cac API statistics.
3. Kiem tra:
   - [ ] Tong doanh thu khop payment.
   - [ ] Popular items khop so luong da ban.
   - [ ] Revenue by day/by staff khop du lieu order.

## 21. Lenh test tu dong tham chieu

Chay toan bo unit test:

```powershell
python -m unittest discover -s tests/unittest -v
```

Chay rieng test all API neu can kiem tra luong tong hop voi database that:

```powershell
$env:RUN_REAL_DB_TESTS='1'
python -m unittest tests.test_all_api -v
```

Neu muon doi chieu nhanh voi Postman, import collection:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

Thu tu folder Postman nen chay:

1. `00 - Public`
2. `01 - Admin Scenario`
3. `02 - Staff Scenario`
4. `03 - Cashier Scenario`
5. `04 - Admin Reports And Cleanup`
