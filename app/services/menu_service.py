from app.extensions import db
from app.models import Category, MenuItem
from app.models.menu_item import MENU_ITEM_STATUSES
from app.services.base_service import ABCWritableService


class CategoryService(ABCWritableService):
    """Xu ly danh muc mon an."""

    def get_all(self):
        return Category.query.order_by(Category.name).all()

    def get_by_id(self, record_id):
        return db.get_or_404(Category, record_id)

    def create(self, data):
        ten = data.get('name', '').strip()
        if not ten:
            raise ValueError('Ten danh muc khong duoc de trong')

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
        if data.get('name'):
            ten = data['name'].strip()
            self.__kiem_tra_ten_trung(ten, exclude_id=danh_muc.id)
            danh_muc.name = ten
        danh_muc.description = data.get('description', danh_muc.description)
        db.session.commit()
        return danh_muc

    def delete(self, record_id):
        danh_muc = self.get_by_id(record_id)
        db.session.delete(danh_muc)
        db.session.commit()

    def __kiem_tra_ten_trung(self, ten, exclude_id=None):
        query = Category.query.filter_by(name=ten)
        if exclude_id:
            query = query.filter(Category.id != exclude_id)
        if query.first():
            raise ValueError(f'Danh muc "{ten}" da ton tai')

    def __str__(self):
        return 'CategoryService()'


class MenuItemService(ABCWritableService):
    """Xu ly mon an trong menu."""

    def get_all(self):
        return MenuItem.query.order_by(MenuItem.name).all()

    def get_by_id(self, record_id):
        return db.get_or_404(MenuItem, record_id)

    def create(self, data):
        ten = data.get('name', '').strip()
        gia = data.get('price')
        dm_id = data.get('category_id')
        trang_thai = data.get('status', 'con_mon')

        if not all([ten, gia, dm_id]):
            raise ValueError('Thieu name, price hoac category_id')
        if int(gia) <= 0:
            raise ValueError('Gia mon phai lon hon 0')
        self.__kiem_tra_danh_muc(dm_id)

        self.__kiem_tra_trang_thai(trang_thai)

        mon = MenuItem(
            name=ten,
            description=data.get('description', ''),
            price=int(gia),
            category_id=dm_id,
            status=trang_thai,
            is_available=trang_thai == 'con_mon'
        )
        db.session.add(mon)
        db.session.commit()
        return mon

    def update(self, record_id, data):
        mon = self.get_by_id(record_id)
        mon.name = data.get('name', mon.name)
        mon.description = data.get('description', mon.description)

        if data.get('status'):
            self.__kiem_tra_trang_thai(data['status'])
            mon.status = data['status']
            mon.is_available = mon.status == 'con_mon'
        elif 'is_available' in data:
            mon.is_available = data['is_available']
            mon.status = 'con_mon' if mon.is_available else 'ngung_ban'

        if data.get('price'):
            if int(data['price']) <= 0:
                raise ValueError('Gia mon phai lon hon 0')
            mon.price = int(data['price'])
        if data.get('category_id'):
            self.__kiem_tra_danh_muc(data['category_id'])
            mon.category_id = data['category_id']
        db.session.commit()
        return mon

    def delete(self, record_id):
        # Khong xoa han de khong anh huong cac don hang cu.
        mon = self.get_by_id(record_id)
        mon.is_available = False
        mon.status = 'ngung_ban'
        db.session.commit()

    def __kiem_tra_trang_thai(self, trang_thai):
        if trang_thai not in MENU_ITEM_STATUSES:
            raise ValueError(f'Trang thai mon khong hop le. Chon mot trong: {MENU_ITEM_STATUSES}')

    def __kiem_tra_danh_muc(self, category_id):
        if not db.session.get(Category, category_id):
            raise ValueError('Danh muc khong ton tai')

    def __str__(self):
        return 'MenuItemService()'
