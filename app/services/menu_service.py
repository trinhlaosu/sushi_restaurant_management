from app.extensions import db
from app.models import Category, MenuItem
from app.services.base_service import ABCWritableService


class CategoryService(ABCWritableService):
    """Xử lý danh mục món ăn."""

    def get_all(self):
        return Category.query.order_by(Category.name).all()

    def get_by_id(self, record_id):
        return Category.query.get_or_404(record_id)

    def create(self, data):
        ten = data.get('name', '').strip()
        if not ten:
            raise ValueError('Tên danh mục không được để trống')

        self.__kiem_tra_ten_trung(ten)

        danh_muc = Category(
            name=ten,
            description=data.get('description', '')
        )
        db.session.add(danh_muc)
        db.session.commit()
        return danh_muc

    def update(self, record_id, data):
        danh_muc = self.get_by_id(record_id)
        danh_muc.name        = data.get('name',        danh_muc.name)
        danh_muc.description = data.get('description', danh_muc.description)
        db.session.commit()
        return danh_muc

    def delete(self, record_id):
        danh_muc = self.get_by_id(record_id)
        db.session.delete(danh_muc)
        db.session.commit()

    def __kiem_tra_ten_trung(self, ten):
        if Category.query.filter_by(name=ten).first():
            raise ValueError(f'Danh mục "{ten}" đã tồn tại')

    def __str__(self):
        return 'CategoryService()'


class MenuItemService(ABCWritableService):
    """Xử lý món ăn trong menu."""

    def get_all(self):
        return MenuItem.query.order_by(MenuItem.name).all()

    def get_by_id(self, record_id):
        return MenuItem.query.get_or_404(record_id)

    def create(self, data):
        ten      = data.get('name', '').strip()
        gia      = data.get('price')
        dm_id    = data.get('category_id')

        if not all([ten, gia, dm_id]):
            raise ValueError('Thiếu name, price hoặc category_id')
        if int(gia) <= 0:
            raise ValueError('Giá món phải lớn hơn 0')

        mon = MenuItem(
            name=ten,
            description=data.get('description', ''),
            price=int(gia),
            category_id=dm_id,
            is_available=data.get('is_available', True)
        )
        db.session.add(mon)
        db.session.commit()
        return mon

    def update(self, record_id, data):
        mon = self.get_by_id(record_id)
        mon.name         = data.get('name',         mon.name)
        mon.description  = data.get('description',  mon.description)
        mon.is_available = data.get('is_available',  mon.is_available)
        if data.get('price'):
            if int(data['price']) <= 0:
                raise ValueError('Giá món phải lớn hơn 0')
            mon.price = int(data['price'])
        if data.get('category_id'):
            mon.category_id = data['category_id']
        db.session.commit()
        return mon

    def delete(self, record_id):
        # Không xóa hẳn để không ảnh hưởng các đơn hàng cũ
        mon = self.get_by_id(record_id)
        mon.is_available = False
        db.session.commit()

    def __str__(self):
        return 'MenuItemService()'
