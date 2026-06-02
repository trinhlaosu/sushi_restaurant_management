# API Detailed Specification

Tai lieu nay mo ta chi tiet tung API cua Sushi Restaurant Management: muc dich, quyen truy cap, payload, luong xu ly controller -> service -> database, business rule va side effect.

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
| `staff` | Nhan vien phuc vu, tao order, dat ban, quan ly khach |
| `cashier` | Thu ngan, thanh toan, xem hoa don/thanh toan |

Response pattern:

- API tao moi thuong tra `201` va object vua tao.
- API cap nhat/xoa/thao tac thuong tra `200` va message.
- Loi nghiep vu trong service thuong tra qua `service_error_response`.
- API dung `get_or_404` se tra `404` khi ID khong ton tai.

## 2. Health

### GET `/api/health`

- Quyen: public.
- Controller: route khai bao truc tiep trong `app/__init__.py`.
- Muc dich: kiem tra Flask app dang chay.
- Request body: khong co.
- Response thanh cong:

```json
{
  "message": "Sushi Restaurant API is running"
}
```

- Luong chay:
  1. Client goi endpoint.
  2. Flask tra JSON tinh.
  3. Khong truy cap database.
- Business rule: khong co.
- Side effect: khong co.

## 3. Auth

### POST `/api/auth/register`

- Quyen: public.
- Controller: `auth_controller.register`.
- Service: `AuthService.register`.
- Muc dich: tao tai khoan moi.
- Body:

```json
{
  "full_name": "New Staff",
  "username": "new_staff",
  "password": "new123"
}
```

- Response chinh: `201`, tra `user`.
- Luong chay:
  1. Controller lay JSON body.
  2. Service bat buoc co `full_name`, `username`, `password`.
  3. Service kiem tra `username` chua ton tai.
  4. Service tim role `staff`.
  5. Tao `User`, hash password qua `set_password`.
  6. Commit database.
- Business rule:
  - Tai khoan dang ky moi mac dinh la `staff`.
  - Neu chua seed role `staff`, API loi runtime.
  - Username khong duoc trung.
- Side effect:
  - Them record `User`.

### POST `/api/auth/login`

- Quyen: public.
- Controller: `auth_controller.login`.
- Service: `AuthService.login`.
- Muc dich: dang nhap va cap access token.
- Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

- Response chinh: `200`, tra `token` va `user`.
- Luong chay:
  1. Tim `User` theo username.
  2. Kiem tra password bang `check_password`.
  3. Tao chuoi token random bang `secrets.token_urlsafe(32)`.
  4. Luu token vao bang `AccessToken`.
  5. Tra token cho client.
- Business rule:
  - Sai username/password tra loi dang nhap that bai.
  - Moi lan login tao token moi.
- Side effect:
  - Them record `AccessToken`.

### POST `/api/auth/logout`

- Quyen: `admin`, `staff`, `cashier`.
- Controller: `auth_controller.logout`.
- Service: `AuthService.logout`.
- Muc dich: vo hieu hoa token hien tai.
- Body: khong bat buoc.
- Response chinh: `200`.
- Luong chay:
  1. `auth_required` doc bearer token.
  2. Controller lay `g.access_token`.
  3. Service set `is_revoked = True`.
  4. Commit database.
- Business rule:
  - Token da logout khong dung duoc cho API protected.
  - Admin, staff va cashier deu co the logout token cua chinh minh.
- Side effect:
  - Cap nhat record `AccessToken`.

## 4. User

### GET `/api/users`

- Quyen: `admin`.
- Controller: `user_controller.get_users`.
- Service: `UserService.get_all`.
- Muc dich: xem danh sach tai khoan.
- Body: khong co.
- Response chinh: `200`, list user theo `id` tang dan.
- Luong chay:
  1. Auth guard xac nhan role admin.
  2. Service query `User.query.order_by(User.id)`.
  3. Controller serialize bang `to_dict`.
- Business rule:
  - Staff/cashier bi chan boi role guard.
- Side effect: khong co.

### PUT `/api/users/<user_id>/role`

- Quyen: `admin`.
- Controller: `user_controller.update_user_role`.
- Service: `UserService.update_role`.
- Muc dich: doi role cua user.
- Body:

```json
{
  "role": "admin"
}
```

- Response chinh: `200`, tra `user`.
- Luong chay:
  1. Tim `Role` theo `name`.
  2. Tim `User` theo `user_id`.
  3. Gan `user.role_id = role.id`.
  4. Commit database.
- Business rule:
  - Role phai ton tai trong bang `Role`.
  - User khong ton tai tra `404`.
- Side effect:
  - Cap nhat role user.

## 5. Category

### GET `/api/categories`

- Quyen: `admin`, `staff`.
- Controller: `category_controller.get_all`.
- Service: `CategoryService.get_all`.
- Muc dich: xem danh sach danh muc mon.
- Response chinh: `200`, list category.
- Luong chay:
  1. Auth guard kiem role.
  2. Service lay danh sach category.
  3. Controller tra list JSON.
- Business rule: day la master data de menu item tham chieu.
- Side effect: khong co.

### GET `/api/categories/<id>`

- Quyen: `admin`, `staff`.
- Muc dich: xem chi tiet mot danh muc.
- Response chinh: `200`, category object.
- Luong chay:
  1. Service tim category theo ID.
  2. Tra `to_dict`.
- Business rule:
  - ID khong ton tai tra `404`.
- Side effect: khong co.

### POST `/api/categories`

- Quyen: `admin`.
- Muc dich: tao danh muc mon.
- Body:

```json
{
  "name": "Sashimi",
  "description": "Raw fish"
}
```

- Response chinh: `201`, tra `category`.
- Luong chay:
  1. Controller lay JSON.
  2. Service validate va tao category.
  3. Commit DB.
- Business rule:
  - `name` la thong tin quan trong de phan loai menu item.
  - Thuong chi admin duoc tao/sua/xoa master data.
- Side effect:
  - Them record `Category`.

### PUT `/api/categories/<id>`

- Quyen: `admin`.
- Muc dich: cap nhat danh muc.
- Body vi du:

```json
{
  "name": "Updated Category",
  "description": "Updated description"
}
```

- Response chinh: `200`, tra `category`.
- Luong chay:
  1. Tim category theo ID.
  2. Apply field trong body.
  3. Commit DB.
- Business rule:
  - Chi cap nhat danh muc, khong tu dong sua menu item ngoai foreign key hien co.
- Side effect:
  - Cap nhat record `Category`.

### DELETE `/api/categories/<id>`

- Quyen: `admin`.
- Muc dich: xoa danh muc.
- Response chinh: `200`.
- Luong chay:
  1. Tim category.
  2. Service xoa.
  3. Commit DB.
- Business rule:
  - Neu category dang duoc menu item tham chieu, database/service co the chan tuy constraint.
- Side effect:
  - Xoa record `Category`.

## 6. Menu Item va Recipe

### GET `/api/menu-items`

- Quyen: public.
- Controller: `menu_item_controller.get_all`.
- Service: `MenuItemService.get_all`.
- Muc dich: xem menu ban hang.
- Response chinh: `200`, list menu item.
- Luong chay:
  1. Client goi public endpoint.
  2. Service lay danh sach mon.
  3. Controller tra JSON.
- Business rule:
  - Public co the xem menu khong can login.
  - Mon co `is_available`/`status` la du lieu quyet dinh co ban duoc hay khong khi tao order.
- Side effect: khong co.

### GET `/api/menu-items/<id>`

- Quyen: public.
- Muc dich: xem chi tiet mon.
- Response chinh: `200`, menu item object.
- Business rule:
  - ID khong ton tai tra `404`.
- Side effect: khong co.

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

- Response chinh: `201`, tra `menu_item`.
- Luong chay:
  1. Controller lay JSON.
  2. Service tao `MenuItem`.
  3. Gan category, gia, mo ta, trang thai mac dinh.
  4. Commit DB.
- Business rule:
  - Chi admin duoc quan ly menu.
  - `category_id` nen ton tai.
  - Gia mon duoc dung ve sau de tinh `subtotal`, `total_amount`.
- Side effect:
  - Them record `MenuItem`.

### PUT `/api/menu-items/<id>`

- Quyen: `admin`.
- Muc dich: cap nhat thong tin mon.
- Body vi du:

```json
{
  "price": 50000,
  "is_available": true,
  "status": "con_mon"
}
```

- Response chinh: `200`, tra `menu_item`.
- Luong chay:
  1. Tim menu item.
  2. Cap nhat field co trong body.
  3. Commit DB.
- Business rule:
  - Gia moi chi anh huong order tao sau; order da tao co `unit_price` rieng trong `OrderDetail`.
- Side effect:
  - Cap nhat record `MenuItem`.

### DELETE `/api/menu-items/<id>`

- Quyen: `admin`.
- Muc dich: an mon khoi menu.
- Response chinh: `200`.
- Luong chay:
  1. Tim menu item.
  2. Service thuc hien xoa/an mon.
  3. Commit DB.
- Business rule:
  - Theo test hien co, delete menu item la xoa mem: `is_available = false`.
  - Mon bi an khong duoc phep tao order moi.
- Side effect:
  - Cap nhat trang thai mon thay vi bat buoc xoa cung.

### GET `/api/menu-items/<menu_item_id>/ingredients`

- Quyen: `admin`, `staff`.
- Controller: `inventory_controller.get_recipe`.
- Service: `RecipeService.get_by_menu_item`.
- Muc dich: xem cong thuc/dinh luong nguyen lieu cua mon.
- Response chinh: `200`, list recipe item.
- Luong chay:
  1. Kiem tra menu item ton tai.
  2. Query `MenuItemIngredient` theo `menu_item_id`.
  3. Tra list.
- Business rule:
  - Recipe duoc dung khi tao order de tru ton kho.
- Side effect: khong co.

### POST `/api/menu-items/<menu_item_id>/ingredients`

- Quyen: `admin`.
- Muc dich: gan/cap nhat cong thuc mon.
- Body:

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

- Response chinh: `200`, tra `recipe`.
- Luong chay:
  1. Kiem tra menu item ton tai.
  2. Xoa recipe cu cua mon.
  3. Voi tung ingredient trong body:
     - Kiem tra ingredient ton tai.
     - Kiem tra `quantity > 0`.
     - Tao `MenuItemIngredient`.
  4. Commit DB.
- Business rule:
  - Moi lan set recipe la thay the toan bo recipe cu.
  - `quantity` la dinh luong tieu hao cho 1 don vi mon.
- Side effect:
  - Xoa recipe cu, them recipe moi.

## 7. Table

### GET `/api/tables`

- Quyen: `admin`, `staff`.
- Controller: `table_controller.get_tables`.
- Service: `TableService.get_all`.
- Muc dich: xem danh sach ban va trang thai.
- Response chinh: `200`, list table.
- Luong chay:
  1. Service goi `release_expired_reservations`.
  2. Cac ban `da_dat` qua `reserved_until` duoc chuyen ve `trong`.
  3. Tra danh sach table theo ID.
- Business rule:
  - Ban dat tam thoi het han sau 15 phut.
- Side effect:
  - Co the cap nhat cac ban dat qua han ve `trong`.

### POST `/api/tables`

- Quyen: `admin`.
- Muc dich: tao ban moi.
- Body:

```json
{
  "table_number": "B02",
  "seats": 6,
  "status": "trong"
}
```

- Response chinh: `201`, tra `table`.
- Luong chay:
  1. Tao `DiningTable`.
  2. Seats mac dinh la 4 neu khong truyen.
  3. Ap dung status bang `apply_table_status`.
  4. Commit DB.
- Business rule:
  - Status hop le nam trong `TABLE_STATUSES`.
  - Neu tao voi `status = da_dat`, set `reserved_at` va `reserved_until = reserved_at + 15 phut`.
- Side effect:
  - Them record `DiningTable`.

### PUT `/api/tables/<table_id>`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat ban, dac biet la trang thai ban.
- Body vi du:

```json
{
  "status": "da_dat"
}
```

- Response chinh: `200`, tra `table`.
- Luong chay:
  1. Tim table.
  2. Cap nhat `table_number`, `seats` neu co.
  3. Neu co `status`, goi `apply_table_status`.
  4. Commit DB.
- Business rule:
  - `da_dat`: set thoi gian giu ban 15 phut.
  - `trong` hoac `dang_phuc_vu`: xoa `reserved_at`, `reserved_until`.
  - Status khong hop le bi bao loi.
- Side effect:
  - Cap nhat record `DiningTable`.

### DELETE `/api/tables/<table_id>`

- Quyen: `admin`.
- Muc dich: xoa ban.
- Response chinh: `200`.
- Luong chay:
  1. Tim table.
  2. Xoa record.
  3. Commit DB.
- Business rule:
  - Nen chi xoa ban khong con rang buoc order/reservation.
- Side effect:
  - Xoa record `DiningTable`.

## 8. Customer

### GET `/api/customers`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach khach hang.
- Response chinh: `200`, list customer theo ID.
- Business rule:
  - Khach hang co the la `khach_le` hoac `thanh_vien`.
- Side effect: khong co.

### POST `/api/customers`

- Quyen: `admin`, `staff`.
- Muc dich: tao khach hang.
- Body:

```json
{
  "full_name": "Nguyen Van A",
  "phone": "0900000001",
  "customer_type": "thanh_vien",
  "member_tier": "vip",
  "birth_date": "1998-06-12",
  "note": "VIP"
}
```

- Response chinh: `201`, tra `customer`.
- Luong chay:
  1. Tao `Customer` voi `full_name`.
  2. Apply phone, note, customer_type, member_tier, birth_date.
  3. Parse `birth_date` bang `date.fromisoformat`.
  4. Commit DB.
- Business rule:
  - `customer_type` phai thuoc `CUSTOMER_TYPES`.
  - `member_tier` phai thuoc `MEMBER_TIERS`.
  - Neu `customer_type = khach_le`, service reset `member_tier = thuong` va `birth_date = None`.
  - Thong tin thanh vien duoc OrderService dung de tinh uu dai neu khong dung voucher code.
- Side effect:
  - Them record `Customer`.

### PUT `/api/customers/<customer_id>`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat khach hang.
- Body vi du:

```json
{
  "note": "VIP",
  "member_tier": "gold"
}
```

- Response chinh: `200`, tra `customer`.
- Luong chay:
  1. Tim customer.
  2. Apply field co trong body.
  3. Commit DB.
- Business rule:
  - Chuyen ve `khach_le` se xoa birth date va dua tier ve `thuong`.
- Side effect:
  - Cap nhat record `Customer`.

### DELETE `/api/customers/<customer_id>`

- Quyen: `admin`.
- Muc dich: xoa khach hang.
- Response chinh: `200`.
- Business rule:
  - Nen tranh xoa customer dang co order/reservation neu DB co rang buoc.
- Side effect:
  - Xoa record `Customer`.

## 9. Reservation

### GET `/api/reservations`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach dat ban.
- Response chinh: `200`, list reservation.
- Side effect: khong co.

### POST `/api/reservations`

- Quyen: `admin`, `staff`.
- Service: `ReservationService.create`.
- Muc dich: tao lich dat ban.
- Body:

```json
{
  "table_id": 1,
  "customer_id": 1,
  "reservation_time": "2030-01-01T18:00:00",
  "guest_count": 2,
  "note": "Dat ban buoi toi"
}
```

- Response chinh: `201`, tra `reservation`.
- Luong chay:
  1. Kiem tra table/customer theo ID.
  2. Parse `reservation_time`.
  3. Tao `Reservation`.
  4. Commit DB.
- Business rule:
  - Dung de quan ly dat ban theo customer va table.
  - Status mac dinh trong test la `cho_xac_nhan`.
  - Service chan so khach <= 0, so khach vuot so ghe, customer/table khong ton tai va ban trung lich trong khoang 2 gio truoc/sau.
- Side effect:
  - Them record `Reservation`.

### PUT `/api/reservations/<reservation_id>`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat lich dat ban.
- Body vi du:

```json
{
  "status": "da_xac_nhan"
}
```

- Response chinh: `200`, tra `reservation`.
- Luong chay:
  1. Tim reservation.
  2. Apply cac field cap nhat.
  3. Commit DB.
- Business rule:
  - Thuong dung de xac nhan/huy/cap nhat thoi gian dat ban.
- Side effect:
  - Cap nhat record `Reservation`.

### DELETE `/api/reservations/<reservation_id>`

- Quyen: `admin`, `staff`.
- Muc dich: huy dat ban.
- Response chinh: `200`.
- Luong chay:
  1. Tim reservation.
  2. Service delete/cancel.
  3. Commit DB.
- Business rule:
  - Ten controller la `cancel_reservation`, nghia nghiep vu la huy dat ban.
- Side effect:
  - Cap nhat reservation sang status `da_huy`, khong xoa record khoi database.

## 10. Discount

### GET `/api/discounts`

- Quyen: `admin`, `staff`.
- Muc dich: xem danh sach voucher/ma giam gia.
- Response chinh: `200`, list discount theo ID giam dan.
- Side effect: khong co.

### POST `/api/discounts`

- Quyen: `admin`.
- Service: `DiscountService.create`.
- Muc dich: tao ma giam gia.
- Body:

```json
{
  "code": "SALE10",
  "discount_type": "percent",
  "value": 10,
  "usage_limit": 5,
  "expires_at": "2030-01-01T00:00:00",
  "is_active": true
}
```

- Response chinh: `201`, tra `discount`.
- Luong chay:
  1. Chuan hoa `code`: strip va upper.
  2. Kiem tra code khong rong, khong trung.
  3. Kiem tra `discount_type` la `percent` hoac `amount`.
  4. Kiem tra `value > 0`.
  5. Parse `expires_at` neu co.
  6. Tao `Discount`, commit DB.
- Business rule:
  - `percent`: so tien giam = `total * value / 100`, toi da bang total.
  - `amount`: giam truc tiep so tien, toi da bang total.
  - `usage_limit` gioi han so lan su dung.
- Side effect:
  - Them record `Discount`.

### PUT `/api/discounts/<discount_id>`

- Quyen: `admin`.
- Muc dich: cap nhat ma giam gia.
- Body vi du:

```json
{
  "value": 15,
  "is_active": true
}
```

- Response chinh: `200`, tra `discount`.
- Business rule:
  - `discount_type` van chi nhan `percent` hoac `amount`.
  - `value` phai lon hon 0.
  - `expires_at` co the set null neu truyen rong.
- Side effect:
  - Cap nhat record `Discount`.

### DELETE `/api/discounts/<discount_id>`

- Quyen: `admin`.
- Muc dich: tat ma giam gia.
- Response chinh: `200`.
- Luong chay:
  1. Tim discount.
  2. Set `is_active = False`.
  3. Commit DB.
- Business rule:
  - Day la xoa mem/tat voucher, khong xoa record.
  - Voucher bi tat khong duoc ap dung cho order moi.
- Side effect:
  - Cap nhat `Discount.is_active`.

## 11. Inventory

### GET `/api/ingredients`

- Quyen: `admin`, `staff`.
- Muc dich: xem ton kho nguyen lieu.
- Response chinh: `200`, list ingredient sap xep theo name.
- Side effect: khong co.

### POST `/api/ingredients`

- Quyen: `admin`.
- Muc dich: tao nguyen lieu.
- Body:

```json
{
  "name": "Salmon",
  "unit": "gram",
  "stock_quantity": 100,
  "min_quantity": 10
}
```

- Response chinh: `201`, tra `ingredient`.
- Luong chay:
  1. Strip name.
  2. Kiem tra name khong rong va khong trung.
  3. Tao ingredient voi unit mac dinh `gram`, stock/min quantity dang float.
  4. Commit DB.
- Business rule:
  - Ingredient duoc recipe tham chieu.
  - Stock bi tru khi tao order co menu item dung ingredient do.
- Side effect:
  - Them record `Ingredient`.

### PUT `/api/ingredients/<ingredient_id>`

- Quyen: `admin`.
- Muc dich: cap nhat nguyen lieu/ton kho.
- Body vi du:

```json
{
  "stock_quantity": 500,
  "min_quantity": 50
}
```

- Response chinh: `200`, tra `ingredient`.
- Business rule:
  - `stock_quantity` va `min_quantity` duoc parse sang float.
- Side effect:
  - Cap nhat record `Ingredient`.

### DELETE `/api/ingredients/<ingredient_id>`

- Quyen: `admin`.
- Muc dich: xoa nguyen lieu.
- Response chinh: `200`.
- Business rule:
  - Neu ingredient dang nam trong recipe, DB/service co the chan xoa tuy rang buoc.
- Side effect:
  - Xoa record `Ingredient`.

## 12. Order

### GET `/api/orders`

- Quyen: `admin`, `staff`.
- Controller: `order_controller.get_orders`.
- Service: `OrderService.get_all`.
- Muc dich: xem danh sach order.
- Response chinh: `200`, list order khong kem details day du.
- Luong chay:
  1. Service giai phong ban dat qua han.
  2. Query order theo ID giam dan.
  3. Serialize voi `include_details=False`.
- Business rule:
  - List order nhe hon detail, phu hop man hinh tong quan.
- Side effect:
  - Co the cap nhat ban `da_dat` qua han ve `trong`.

### GET `/api/orders/<order_id>`

- Quyen: `admin`, `staff`.
- Muc dich: xem chi tiet order.
- Response chinh: `200`, order kem details.
- Luong chay:
  1. Service giai phong ban dat qua han.
  2. Tim order theo ID.
  3. Serialize order day du.
- Business rule:
  - Dung cho man hinh chi tiet don/hang da goi.
- Side effect:
  - Co the cap nhat ban dat qua han.

### POST `/api/orders`

- Quyen: `admin`, `staff`.
- Controller: `order_controller.create_order`.
- Service: `OrderService.create`.
- Muc dich: tao don goi mon.
- Body:

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

- Response chinh: `201`, tra `order`.
- Luong chay:
  1. Controller lay JSON va gan `user_id = g.current_user.id`.
  2. Service bat buoc `items` khong rong.
  3. Giai phong ban dat qua han.
  4. Kiem tra table ton tai va table khong phai `dang_phuc_vu`.
  5. Tao `Order` status `dang_xu_ly`, flush de lay ID.
  6. Voi tung item:
     - Parse `quantity`.
     - Kiem tra `quantity > 0`.
     - Tim menu item.
     - Kiem tra mon ton tai, `is_available = true`, `status = con_mon`.
     - Goi `RecipeService.ensure_stock_and_deduct`.
     - Tao `OrderDetail` voi `unit_price`, `subtotal`.
  7. Tinh khuyen mai:
     - Neu co `discount_code`, lay voucher active, tinh amount, tang `used_count`.
     - Neu khong co voucher, kiem tra customer thanh vien.
     - Thanh vien sinh nhat duoc giam 10%, khong kem qua tang.
     - Thanh vien khong sinh nhat duoc giam theo tier va co the co `gift_item`.
  8. Gan `total_amount`, `discount_amount`, `final_amount`, note khuyen mai.
  9. Chuyen table sang `dang_phuc_vu`, xoa thong tin dat ban tam.
  10. Commit DB.
- Business rule:
  - Don phai co it nhat 1 mon.
  - Ban dang phuc vu khong tao don moi.
  - Mon het hang/khong du nguyen lieu bi chan.
  - Voucher uu tien hon uu dai thanh vien neu co `discount_code`.
  - Voucher het han/tat/het luot bi chan.
  - Stock ingredient bi tru ngay khi tao order.
- Side effect:
  - Them `Order`, `OrderDetail`.
  - Tru `Ingredient.stock_quantity`.
  - Tang `Discount.used_count` neu dung voucher.
  - Cap nhat table sang `dang_phuc_vu`.

### PUT `/api/orders/<order_id>/status`

- Quyen: `admin`, `staff`.
- Muc dich: cap nhat trang thai don.
- Body:

```json
{
  "status": "da_phuc_vu"
}
```

- Response chinh: `200`, tra `order`.
- Luong chay:
  1. Tim order.
  2. Validate status thuoc `dang_xu_ly`, `da_phuc_vu`, `da_thanh_toan`, `da_huy`.
  3. Gan status.
  4. Neu status la `da_thanh_toan` hoac `da_huy`, ban ve `trong`.
  5. Commit DB.
- Business rule:
  - Status khong hop le bi bao loi.
  - Ket thuc don/huy don giai phong ban.
- Side effect:
  - Cap nhat `Order.status`.
  - Co the cap nhat `DiningTable.status`.

## 13. Payment

### POST `/api/payments`

- Quyen: `admin`, `staff`, `cashier`.
- Controller: `payment_app.controllers.payment_controller.create_payment`.
- Service: `payment_app.services.PaymentService.thanh_toan`.
- Muc dich: thanh toan order.
- Body:

```json
{
  "order_id": 1,
  "payment_method": "tien_mat"
}
```

- Response chinh: `201`, tra `payment`.
- Luong chay:
  1. Controller lay JSON.
  2. PaymentService lay order qua `OrderService.get_by_id`.
  3. Kiem tra order chua co payment.
  4. Tao `Payment` voi amount = `order.final_amount` neu co, nguoc lai `order.total_amount`.
  5. Goi `OrderService.cap_nhat_trang_thai(order, 'da_thanh_toan')`.
  6. Commit DB.
  7. Controller ghi `ActivityLog` action `create_payment`.
  8. Tra payment.
- Business rule:
  - Mot order chi thanh toan mot lan.
  - Order da huy khong duoc thanh toan.
  - Thanh toan xong order sang `da_thanh_toan`.
  - Thanh toan xong ban ve `trong`.
  - Payment method mac dinh la `tien_mat`.
- Side effect:
  - Them `Payment`.
  - Cap nhat `Order.status`.
  - Cap nhat `DiningTable.status`.
  - Them `ActivityLog`.

### GET `/api/payments`

- Quyen: `admin`, `cashier`.
- Muc dich: xem lich su thanh toan.
- Response chinh: `200`, list payment theo ID giam dan.
- Business rule:
  - Staff co the tao payment theo decorator POST, nhung khong duoc xem danh sach payment theo decorator GET.
- Side effect: khong co.

## 14. Invoice

### GET `/api/invoices/<order_id>`

- Quyen: `admin`, `staff`, `cashier`.
- Controller: `invoice_controller.get_invoice`.
- Service: `InvoiceService.get_invoice`.
- Muc dich: lay hoa don chi tiet cho order da thanh toan.
- Response chinh: `200`, invoice object:

```json
{
  "invoice_code": "HD000001",
  "order_id": 1,
  "items": [],
  "subtotal": 90000,
  "discount_code": "SALE10",
  "discount_amount": 9000,
  "total_amount": 81000,
  "payment": {}
}
```

- Luong chay:
  1. Lay order qua `OrderService.get_by_id`.
  2. Neu order chua co payment, raise loi.
  3. Tao `invoice_code = HD{order.id:06d}`.
  4. Lay table, customer, details, subtotal, discount, payment.
  5. Tra dict invoice.
- Business rule:
  - Chi order da thanh toan moi co hoa don.
  - `total_amount` trong invoice la `final_amount` neu co, nguoc lai `total_amount`.
- Side effect: khong co.

## 15. Shift

### GET `/api/shifts`

- Quyen: `admin`.
- Muc dich: xem danh sach ca lam.
- Response chinh: `200`, list shift theo ID giam dan.
- Business rule:
  - Chi admin xem toan bo ca lam.
- Side effect: khong co.

### POST `/api/shifts/check-in`

- Quyen: `admin`, `staff`, `cashier`.
- Service: `ShiftService.check_in`.
- Muc dich: bat dau ca lam.
- Body:

```json
{
  "user_id": 2,
  "note": "Morning shift"
}
```

- Response chinh: `201`, tra `shift`.
- Luong chay:
  1. Kiem tra user ton tai.
  2. Tim shift active cua user: `end_time = None`.
  3. Neu da co shift active, bao loi.
  4. Tao `Shift` moi.
  5. Commit DB.
- Business rule:
  - Moi user chi co mot ca active tai mot thoi diem.
- Side effect:
  - Them record `Shift`.

### POST `/api/shifts/<shift_id>/check-out`

- Quyen: `admin`, `staff`, `cashier`.
- Muc dich: ket thuc ca lam.
- Response chinh: `200`, tra `shift`.
- Luong chay:
  1. Tim shift.
  2. Neu da co `end_time`, bao loi.
  3. Set `end_time = datetime.utcnow()`.
  4. Commit DB.
- Business rule:
  - Ca da ket thuc khong checkout lai.
- Side effect:
  - Cap nhat `Shift.end_time`.

## 16. Activity Log

### GET `/api/activity-logs`

- Quyen: `admin`.
- Muc dich: xem lich su thao tac.
- Response chinh: `200`, list log theo ID giam dan.
- Luong chay:
  1. Auth guard admin.
  2. Service query `ActivityLog`.
  3. Tra list.
- Business rule:
  - Hien tai payment controller ghi log khi tao payment.
  - Log gom `user_id`, `action`, `target_type`, `target_id`, `description`.
- Side effect: khong co khi GET.

## 17. Statistics

### GET `/api/statistics`

- Quyen: `admin`.
- Service: `StatisticService.get_all`.
- Muc dich: thong ke tong quan.
- Response chinh:

```json
{
  "tong_don_da_thanh_toan": 1,
  "tong_doanh_thu": 90000,
  "top_5_mon_ban_chay": [],
  "currency": "VND"
}
```

- Luong chay:
  1. Query order co `status = da_thanh_toan`.
  2. Dem so don da thanh toan.
  3. Sum `Order.final_amount`.
  4. Query top 5 mon ban chay tu `OrderDetail`.
- Business rule:
  - Chi tinh doanh thu tu order da thanh toan.
  - Don vi tien te la VND.
- Side effect: khong co.

### GET `/api/statistics/revenue`

- Quyen: `admin`.
- Query params:

```text
?tu_ngay=2026-06-01&den_ngay=2026-06-30
```

- Muc dich: thong ke doanh thu theo khoang ngay.
- Response chinh: `so_don`, `tong_doanh_thu`, `currency`.
- Luong chay:
  1. Lay `tu_ngay`, `den_ngay` tu query string.
  2. Filter order da thanh toan theo khoang ngay neu co.
  3. Tra so don va tong doanh thu.
- Business rule:
  - Chi admin xem duoc.
  - Chi order `da_thanh_toan` duoc tinh.
- Luu y code hien tai:
  - Phan dem `so_don` va `tong_doanh_thu` deu ap dung filter ngay neu co.
- Side effect: khong co.

### GET `/api/statistics/popular-items`

- Quyen: `admin`.
- Query params:

```text
?top=5
```

- Muc dich: xem mon ban chay.
- Response chinh: list mon voi `ten_mon`, `tong_so_luong`, `tong_tien`.
- Luong chay:
  1. Parse `top`, mac dinh 5.
  2. Join `MenuItem` voi `OrderDetail`.
  3. Group theo mon.
  4. Sap xep theo tong so luong giam dan.
  5. Limit theo top.
- Business rule:
  - Thong ke dua tren order detail da phat sinh.
  - Chi tinh order co status `da_thanh_toan`.
- Side effect: khong co.

### GET `/api/statistics/by-day`

- Quyen: `admin`.
- Muc dich: doanh thu theo ngay.
- Response chinh: list ngay voi `so_don`, `tong_doanh_thu`, `currency`.
- Luong chay:
  1. Filter order `da_thanh_toan`.
  2. Group theo `date(Order.created_at)`.
  3. Sum `Order.final_amount`.
  4. Sap xep ngay giam dan.
- Business rule:
  - Chi tinh order da thanh toan.
- Side effect: khong co.

### GET `/api/statistics/by-staff`

- Quyen: `admin`.
- Muc dich: doanh thu theo nhan vien tao order.
- Response chinh: list user voi `so_don`, `tong_doanh_thu`.
- Luong chay:
  1. Join `User` voi `Order.created_by_user_id`.
  2. Filter order `da_thanh_toan`.
  3. Group theo user.
  4. Sum `Order.final_amount`.
  5. Sap xep doanh thu giam dan.
- Business rule:
  - Ghi nhan theo nhan vien tao order, khong phai nguoi thanh toan.
- Side effect: khong co.

## 18. Luong nghiep vu lon

### 18.1 Luong order -> payment -> invoice

1. Staff/admin login.
2. Tao order qua `POST /api/orders`.
3. Order service:
   - Validate ban, mon, so luong.
   - Tru kho theo recipe.
   - Tinh voucher/member promotion.
   - Set ban sang `dang_phuc_vu`.
4. Cashier/admin/staff thanh toan qua `POST /api/payments`.
5. Payment service:
   - Tao payment.
   - Set order `da_thanh_toan`.
   - Giai phong ban ve `trong`.
   - Ghi activity log.
6. Lay invoice qua `GET /api/invoices/<order_id>`.

Ket qua business can dat:

- Order co details va tong tien dung.
- Ingredient stock giam dung.
- Voucher used_count tang neu ap dung voucher.
- Payment amount bang final amount.
- Invoice chi co khi order da thanh toan.

### 18.2 Luong dat ban tam 15 phut

1. Staff/admin set table status `da_dat`.
2. Table service set `reserved_at` va `reserved_until = reserved_at + 15 phut`.
3. Khi goi `GET /api/tables` hoac order service chay, cac ban het han duoc release ve `trong`.

Ket qua business can dat:

- Ban dat chua het han giu status `da_dat`.
- Ban qua han tu dong ve `trong`.

### 18.3 Luong thanh vien va khuyen mai

1. Customer co `customer_type = thanh_vien`.
2. Tao order khong truyen `discount_code`.
3. Neu thang hien tai trung thang sinh nhat: giam 10%, khong kem qua.
4. Neu khong sinh nhat: giam theo `member_tier`, co the co `gift_item`.
5. Neu order co `discount_code`: voucher duoc uu tien, khong ap dung dong thoi uu dai thanh vien.

### 18.4 Luong ca lam

1. User check-in qua `POST /api/shifts/check-in`.
2. Service chan neu user dang co shift chua checkout.
3. Staff/cashier chi tu check-in/check-out cho chinh minh; admin co the thao tac ho.
4. User check-out qua `POST /api/shifts/<id>/check-out`.
5. Service set `end_time`.

## 19. Danh sach API nhanh

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
| GET | `/api/menu-items/<id>/ingredients` | admin, staff | Recipe |
| POST | `/api/menu-items/<id>/ingredients` | admin | Recipe |
| GET | `/api/tables` | admin, staff | Table |
| POST | `/api/tables` | admin | Table |
| PUT | `/api/tables/<id>` | admin, staff | Table |
| DELETE | `/api/tables/<id>` | admin | Table |
| GET | `/api/customers` | admin, staff | Customer |
| POST | `/api/customers` | admin, staff | Customer |
| PUT | `/api/customers/<id>` | admin, staff | Customer |
| DELETE | `/api/customers/<id>` | admin | Customer |
| GET | `/api/reservations` | admin, staff | Reservation |
| POST | `/api/reservations` | admin, staff | Reservation |
| PUT | `/api/reservations/<id>` | admin, staff | Reservation |
| DELETE | `/api/reservations/<id>` | admin, staff | Reservation |
| GET | `/api/discounts` | admin, staff | Discount |
| POST | `/api/discounts` | admin | Discount |
| PUT | `/api/discounts/<id>` | admin | Discount |
| DELETE | `/api/discounts/<id>` | admin | Discount |
| GET | `/api/ingredients` | admin, staff | Inventory |
| POST | `/api/ingredients` | admin | Inventory |
| PUT | `/api/ingredients/<id>` | admin | Inventory |
| DELETE | `/api/ingredients/<id>` | admin | Inventory |
| GET | `/api/orders` | admin, staff | Order |
| GET | `/api/orders/<id>` | admin, staff | Order |
| POST | `/api/orders` | admin, staff | Order |
| PUT | `/api/orders/<id>/status` | admin, staff | Order |
| POST | `/api/payments` | admin, staff, cashier | Payment |
| GET | `/api/payments` | admin, cashier | Payment |
| GET | `/api/invoices/<order_id>` | admin, staff, cashier | Invoice |
| GET | `/api/shifts` | admin | Shift |
| POST | `/api/shifts/check-in` | admin, staff, cashier | Shift |
| POST | `/api/shifts/<id>/check-out` | admin, staff, cashier | Shift |
| GET | `/api/activity-logs` | admin | Activity Log |
| GET | `/api/statistics` | admin | Statistics |
| GET | `/api/statistics/revenue` | admin | Statistics |
| GET | `/api/statistics/popular-items` | admin | Statistics |
| GET | `/api/statistics/by-day` | admin | Statistics |
| GET | `/api/statistics/by-staff` | admin | Statistics |
