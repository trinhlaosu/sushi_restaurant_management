# Kịch Bản Kiểm Thử API Bằng Postman

Tài liệu này hướng dẫn chạy collection:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

Kịch bản mô phỏng một lượt kiểm thử đầy đủ các chức năng chính của hệ thống
quản lý nhà hàng sushi. Dữ liệu nền được tạo từ `seed.py`; trong lúc chạy
collection, người kiểm thử tạo thêm danh mục, món ăn, bàn, khách hàng, đơn gọi
món, thanh toán và hóa đơn.

## 1. Chuẩn Bị Trước Khi Chạy

Tại thư mục project:

```powershell
python seed.py
python run.py
```

Server mặc định:

```text
http://127.0.0.1:5000
```

Tài khoản mẫu sau khi chạy `seed.py`:

| Vai trò | Username | Password | Mục đích |
|---|---|---|---|
| Admin | `admin` | `admin123` | Quản lý user, danh mục, món ăn, bàn, voucher, thống kê |
| Staff | `staff` | `staff123` | Quản lý khách hàng, tạo đơn gọi món |
| Cashier | `cashier` | `cashier123` | Thanh toán, xem lịch sử thanh toán và hóa đơn |

Dữ liệu nền có sẵn:

| Nhóm dữ liệu | Ví dụ |
|---|---|
| Danh mục | Sushi, Sashimi, Maki / Cuon, Set / Combo, Mon nuong / chien, Com / Mi, Do uong |
| Món ăn | Ca hoi Nigiri, Ca ngu Nigiri, California Roll, Tempura tom, Matcha Latte |
| Bàn | `B01` đến `B10` |
| Khách hàng | Khach le, Nguyen Minh Anh |

## 2. Cách Import Và Chạy Collection

1. Mở Postman.
2. Chọn **Import**.
3. Chọn file:

```text
postman/Nhom07_Sushi_API.postman_collection.json
```

4. Kiểm tra collection variable `base_url`:

```text
http://127.0.0.1:5000
```

5. Chạy các folder theo đúng thứ tự từ `00` đến `05`.

## 3. Biến Postman Được Tự Động Lưu

Collection có script tự lưu dữ liệu tạo mới vào collection variables:

| Biến | Ý nghĩa |
|---|---|
| `admin_token` | Token đăng nhập admin |
| `staff_token` | Token đăng nhập staff |
| `cashier_token` | Token đăng nhập cashier |
| `registered_user_id` | ID nhân viên mới đăng ký |
| `created_category_id` | ID danh mục tạo bằng admin |
| `created_menu_item_id` | ID món ăn tạo bằng admin |
| `created_table_id` | ID bàn tạo bằng admin |
| `created_customer_id` | ID khách hàng tạo bằng staff |
| `order_id` | ID đơn gọi món |
| `payment_id` | ID thanh toán |

Nhờ các biến này, request sau dùng đúng dữ liệu được tạo ở request trước.

## 4. Thứ Tự Chạy Folder

### 00 - Public And Login

Mục tiêu: kiểm tra server, đăng ký một nhân viên mới và đăng nhập 3 vai trò.

Các request chính:

| Request | Dữ liệu sử dụng | Kết quả mong đợi |
|---|---|---|
| Health Check | Không cần token | API trả `200` |
| Đăng ký nhân viên Trần Quốc Bảo | `Trần Quốc Bảo` | Tạo user mới, lưu `registered_user_id` |
| Login Admin | `admin/admin123` | Lưu `admin_token` |
| Login Staff | `staff/staff123` | Lưu `staff_token` |
| Login Cashier | `cashier/cashier123` | Lưu `cashier_token` |

Body đăng ký nhân viên mới:

```json
{
  "full_name": "Trần Quốc Bảo",
  "username": "bao.phucvu",
  "password": "bao123"
}
```

### 01 - Admin Master Data

Mục tiêu: admin tạo dữ liệu vận hành cho nhà hàng.

Luồng dữ liệu:

1. Admin xem danh sách user.
2. Admin xác nhận role của nhân viên mới là `staff`.
3. Admin tạo danh mục mới.
4. Admin tạo món mới thuộc danh mục vừa tạo.
5. Admin tạo bàn mới.
6. Admin cập nhật trạng thái bàn sang `da_dat`.

Dữ liệu tạo mới trong quá trình kiểm thử:

| Chức năng | Dữ liệu nhập |
|---|---|
| Category | `Set gia đình` |
| Menu item | `Set cá hồi gia đình` |
| Giá món | `180000`, sau đó cập nhật thành `195000` VND |
| Table | `B11`, 4 ghế |
| Table status | `da_dat` |

Body tạo món ăn:

```json
{
  "name": "Set cá hồi gia đình",
  "description": "6 miếng nigiri cá hồi, 1 phần maki cá hồi, kèm súp miso",
  "price": 180000,
  "category_id": {{created_category_id}}
}
```

Body tạo bàn:

```json
{
  "table_number": "B11",
  "seats": 4,
  "status": "trong"
}
```

### 02 - Staff Customer And Order

Mục tiêu: staff tạo khách hàng và tạo đơn gọi món bằng dữ liệu vừa tạo.

Luồng dữ liệu:

1. Staff tạo khách hàng thành viên.
2. Staff cập nhật ghi chú khách hàng.
3. Staff tạo order cho bàn `B11`.
4. Staff xem danh sách order.
5. Staff xem chi tiết order.
6. Staff cập nhật trạng thái order sang `da_phuc_vu`.

Dữ liệu khách hàng:

```json
{
  "full_name": "Nguyễn Thị Anh",
  "phone": "0902000011",
  "customer_type": "thanh_vien",
  "member_tier": "vang",
  "birth_date": "1998-05-12",
  "note": "Khách đi 4 người, ưu tiên bàn yên tĩnh"
}
```

Body tạo order:

```json
{
  "table_id": {{created_table_id}},
  "customer_id": {{created_customer_id}},
  "items": [
    {
      "menu_item_id": {{created_menu_item_id}},
      "quantity": 2
    }
  ]
}
```

Kết quả mong đợi:

- Tạo record trong `orders`.
- Tạo chi tiết món trong `order_details`.
- Tổng tiền = giá món sau cập nhật `195000` x số lượng `2` = `390000` VND.
- Bàn chuyển sang trạng thái `dang_phuc_vu`.
- `order_id` được lưu để cashier thanh toán.

### 03 - Cashier Payment And Invoice

Mục tiêu: cashier thanh toán đơn và xem hóa đơn.

Luồng dữ liệu:

1. Cashier tạo payment cho `order_id`.
2. Cashier xem lịch sử thanh toán.
3. Cashier xem hóa đơn chi tiết.

Body thanh toán:

```json
{
  "order_id": {{order_id}},
  "payment_method": "tien_mat"
}
```

Kết quả mong đợi:

- Tạo record trong `payments`.
- Order chuyển sang `da_thanh_toan`.
- Bàn được trả về `trong`.
- API hóa đơn trả mã hóa đơn dạng `HD000001`, danh sách món, tổng tiền và thông tin thanh toán.

### 04 - Admin Reports And Auth Guards

Mục tiêu: admin xem báo cáo và kiểm tra phân quyền.

Các API thống kê:

| Request | Ý nghĩa |
|---|---|
| Statistics Overview | Tổng số đơn đã thanh toán, tổng doanh thu, top món |
| Revenue | Doanh thu |
| Popular Items | Món bán chạy |
| Revenue By Day | Doanh thu theo ngày |
| Revenue By Staff | Doanh thu theo nhân viên tạo order |

Kiểm tra phân quyền:

| Request | Kết quả mong đợi |
|---|---|
| Missing Token gọi `/api/users` | `401` |
| Staff gọi `/api/users` | `403` |

### 05 - Cleanup

Mục tiêu: dọn trạng thái sau khi kiểm thử.

Các request:

| Request | Ý nghĩa |
|---|---|
| Ẩn món vừa tạo | Ẩn món vừa tạo khỏi menu |
| Trả bàn B11 về trạng thái trống | Chuyển bàn `B11` về `trong` |
| Logout Admin | Thu hồi token admin |
| Logout Cashier | Thu hồi token cashier |

Lưu ý: dữ liệu order/payment không xóa để giữ lịch sử bán hàng. Nếu muốn đưa
database về trạng thái sạch hoàn toàn, chạy lại:

```powershell
python seed.py
```

## 5. Lưu Ý Khi Demo

- Luôn chạy `python seed.py` trước buổi kiểm thử để tránh dữ liệu cũ gây trùng.
- Collection dùng dữ liệu cố định để nội dung trả về dễ đọc khi chụp màn hình báo cáo.
- Không chạy folder giữa chừng nếu chưa có token hoặc chưa có biến ID cần thiết.
- Nếu DBeaver đang mở database, hãy refresh lại sau khi chạy `python seed.py`.
- Tất cả giá tiền trong request/response dùng đơn vị **VND**.
