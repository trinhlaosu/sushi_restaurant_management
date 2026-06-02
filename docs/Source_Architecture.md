# Source Architecture

Tai lieu nay tom tat cach source code dap ung cac yeu cau: OOP, MVC, service
layer, module rieng va module goi lai module khac.

## 1. MVC trong project

Project dung Flask REST API nen phan "View" duoc the hien bang JSON response tu
controller.

- Model: `app/models/`
  - Dinh nghia cac entity va quan he CSDL bang SQLAlchemy.
  - Vi du: `User`, `Role`, `Order`, `Payment`, `Reservation`, `Discount`,
    `Ingredient`, `Shift`.
- Controller: `app/controllers/`, `payment_app/controllers/`
  - Nhan request, lay JSON/query params, goi service, tra response.
  - Controller khong xu ly nghiep vu truc tiep.
- Service: `app/services/`, `payment_app/services/`
  - Xu ly nghiep vu chinh: tao don, thanh toan, dat ban, voucher, ton kho,
    hoa don, thong ke, ca lam viec.
- View/Response: `app/utils/response.py`
  - Gom cac helper tra JSON response chung: `success_response`,
    `error_response`, `list_response`, `data_response`.

## 2. OOP

Source dung class cho cac thanh phan chinh:

- Model class ke thua `db.Model`.
- Service class dong goi nghiep vu theo module.
- Base service abstract class trong `app/services/base_service.py`:
  - `ABCBaseService`
  - `ABCWritableService`

Vi du service:

- `OrderService`
- `PaymentService`
- `ReservationService`
- `DiscountService`
- `IngredientService`
- `ShiftService`
- `InvoiceService`
- `ActivityLogService`

## 3. Service layer

Controller chi lam nhiem vu dieu phoi:

1. Nhan request.
2. Goi service.
3. Bat loi nghiep vu neu co.
4. Tra JSON response.

Nghiep vu nam trong service layer. Vi du:

- `OrderService.create()` tinh tong tien, ap dung voucher, tru ton kho.
- `PaymentService.thanh_toan()` tao thanh toan va cap nhat trang thai don.
- `ReservationService.create()` kiem tra ban co bi trung khung gio khong.
- `DiscountService` validate ma giam gia, tinh so tien giam.
- `RecipeService` kiem tra va tru nguyen lieu.
- `InvoiceService` tao hoa don chi tiet tu don da thanh toan.

## 4. Module/app rieng

Module thanh toan da duoc tach thanh app rieng:

- `payment_app/controllers/payment_controller.py`
- `payment_app/services/payment_service.py`

Flask app chinh register blueprint cua payment app trong `app/__init__.py`.
Hai file wrapper duoc giu lai de import cu khong bi vo:

- `app/controllers/payment_controller.py`
- `app/services/payment_service.py`

## 5. Module goi lai module khac

Project co nhieu vi du module goi lai module khac:

- `payment_app.services.PaymentService` goi `app.services.order_service.OrderService`
  de lay don hang va cap nhat trang thai don sau khi thanh toan.
- `payment_app.controllers.payment_controller` goi `ActivityLogService`
  de ghi log thanh toan.
- `OrderService` goi:
  - `DiscountService` de ap dung voucher.
  - `RecipeService` de kiem tra/tru ton kho nguyen lieu.
- `InvoiceService` goi `OrderService` de lay don va tao hoa don chi tiet.

Day la cac diem the hien su tach module va kha nang tai su dung nghiep vu giua
cac module.

## 6. Cac nhom chuc nang hien co

- Auth: dang ky, dang nhap, dang xuat, token auth.
- User: xem user, cap nhat role.
- Category/Menu: quan ly danh muc va mon an.
- Table: quan ly ban.
- Customer: quan ly khach hang.
- Order: tao don, chi tiet don, cap nhat trang thai.
- Payment app: thanh toan, lich su thanh toan.
- Reservation: dat ban va huy dat ban.
- Discount: ma giam gia.
- Inventory/Recipe: nguyen lieu va dinh luong mon.
- Invoice: hoa don chi tiet.
- Activity log: lich su thao tac.
- Shift: ca lam viec.
- Statistic: doanh thu, top mon, doanh thu theo ngay/nhan vien.

## 7. Unit test

Folder `tests/unittest/` cover cac nhom API chinh:

- Auth va phan quyen.
- CRUD cac module quan ly.
- Order + Payment app.
- Voucher + ton kho + hoa don.
- Dat ban + ca lam viec + activity log.
- Bao cao thong ke.
