# Postman Demo Scenario

Tai lieu nay mo ta cach chay collection Postman chinh:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

## 1. Chuan bi

Tai terminal project:

```powershell
python seed.py
python run.py
```

Server mac dinh:

```text
http://127.0.0.1:5000
```

Tai khoan seed:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Staff | `staff` | `staff123` |
| Cashier | `cashier` | `cashier123` |

## 2. Thu tu folder trong collection

Chay folder theo thu tu tu tren xuong duoi.

### 00 - Public And Login

- Kiem tra server bang `GET /api/health`.
- Dang ky mot user demo.
- Dang nhap `admin`, `staff`, `cashier`.
- Token duoc Postman script luu vao collection variables:
  - `admin_token`
  - `staff_token`
  - `cashier_token`

### 01 - Admin Master Data

- Admin xem danh sach user va cap nhat role user demo.
- Admin tao category demo `Set đặc biệt`.
- Staff xem danh sach/chi tiet category.
- Admin cap nhat category demo.
- Admin tao menu item demo `Set Nigiri cá hồi`.
- Public xem danh sach/chi tiet menu item.
- Admin cap nhat menu item demo.
- Admin tao ban demo `VIP-<timestamp>`.
- Staff xem va cap nhat ban demo sang `da_dat`.

### 02 - Staff Customer And Order

- Staff tao customer demo `Nguyễn Minh Anh <timestamp>`.
- Staff xem/cap nhat customer.
- Staff tao order bang chinh du lieu vua tao:
  - `created_table_id`
  - `created_customer_id`
  - `created_menu_item_id`
- Staff xem danh sach order, chi tiet order.
- Staff cap nhat trang thai order sang `da_phuc_vu`.

### 03 - Cashier Payment And Invoice

- Cashier thanh toan order vua tao.
- Cashier xem lich su thanh toan.
- Cashier xem hoa don chi tiet.

### 04 - Admin Reports And Auth Guards

- Admin xem cac API thong ke:
  - tong quan
  - doanh thu
  - mon ban chay
  - doanh thu theo ngay
  - doanh thu theo nhan vien
- Kiem tra phan quyen:
  - thieu token goi `/api/users` phai bi `401`
  - staff goi `/api/users` phai bi `403`

### 05 - Cleanup

- Admin an menu item demo.
- Staff dua ban demo ve `trong`.
- Logout admin va cashier.

## 3. Luu y khi demo

- Nen chay `python seed.py` truoc moi lan demo de DB ve trang thai sach.
- Collection dung `{{$timestamp}}` khi tao category, menu item, table, customer de tranh trung du lieu.
- Order/payment dung chinh du lieu demo vua tao de luong thuyet trinh tu nhien hon.
- Neu chay rieng tung request, can chay cac request login truoc de co token.
- Cleanup khong xoa order/payment, category, customer, table va user dang ky demo vi cac du lieu nay da nam trong lich su order; chay lai `python seed.py` neu can dua DB ve trang thai sach hoan toan.
