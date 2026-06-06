from datetime import date, timedelta

from app import create_app
from app.extensions import db
from app.models import Category, Customer, DiningTable, MenuItem, Role, User
from app.models.dining_table import now_utc


app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_role = Role(name='admin', description='Quan tri vien he thong')
    staff_role = Role(name='staff', description='Nhan vien nha hang')
    cashier_role = Role(name='cashier', description='Nhan vien thu ngan')
    db.session.add_all([admin_role, staff_role, cashier_role])
    db.session.flush()

    admin = User(full_name='Quan tri vien', username='admin', role_id=admin_role.id)
    admin.set_password('admin123')
    staff = User(full_name='Nhan vien ban hang', username='staff', role_id=staff_role.id)
    staff.set_password('staff123')
    cashier = User(full_name='Nhan vien thu ngan', username='cashier', role_id=cashier_role.id)
    cashier.set_password('cashier123')
    db.session.add_all([admin, staff, cashier])

    category_names = [
        ('Sushi', 'Cac mon sushi/nigiri'),
        ('Sashimi', 'Cac mon sashimi ca song'),
        ('Maki / Cuon', 'Cac mon cuon kieu Nhat'),
        ('Set / Combo', 'Combo dung theo nhom'),
        ('Mon nuong / chien', 'Mon an nong'),
        ('Com / Mi', 'Mon chinh dung no'),
        ('Do uong', 'Nuoc uong dung kem'),
    ]
    categories = []
    for name, description in category_names:
        category = Category(name=name, description=description)
        db.session.add(category)
        categories.append(category)
    db.session.flush()

    def category_id(name):
        return next(category for category in categories if category.name == name).id

    menu_items = [
        ('Ca hoi Nigiri', 'Sushi ca hoi', 45000, 'Sushi'),
        ('Ca ngu Nigiri', 'Sushi ca ngu', 42000, 'Sushi'),
        ('Luon Nhat Nigiri', 'Sushi luon Nhat sot kabayaki', 65000, 'Sushi'),
        ('Sashimi ca hoi', 'Ca hoi tuoi cat lat', 129000, 'Sashimi'),
        ('Sashimi ca ngu', 'Ca ngu tuoi cat lat', 119000, 'Sashimi'),
        ('Set Sashimi Tong Hop', 'Set sashimi dung cho 2 nguoi', 399000, 'Set / Combo'),
        ('California Roll', 'Cuon thanh cua, bo va trung ca', 89000, 'Maki / Cuon'),
        ('Cuon ca hoi phu cheese', 'Cuon ca hoi phu pho mai dut lo', 139000, 'Maki / Cuon'),
        ('Cuon hai san chien xu sot spicy', 'Cuon hai san chien xu dung sot cay', 129000, 'Maki / Cuon'),
        ('Hau nuong Misoyaki', 'Hau nuong sot miso', 99000, 'Mon nuong / chien'),
        ('Tempura tom', 'Tom chien tempura', 89000, 'Mon nuong / chien'),
        ('Com luon Nhat', 'Com luon sot kabayaki', 169000, 'Com / Mi'),
        ('Mi Udon bo', 'Mi udon dung voi thit bo', 119000, 'Com / Mi'),
        ('Tra dao', 'Tra dao lanh', 35000, 'Do uong'),
        ('Matcha Latte', 'Matcha latte da', 45000, 'Do uong'),
        ('Nuoc suoi', 'Nuoc suoi dong chai', 12000, 'Do uong'),
    ]
    for name, description, price, category_name in menu_items:
        status = 'het_mon' if name == 'Hau nuong Misoyaki' else 'con_mon'
        db.session.add(MenuItem(
            name=name,
            description=description,
            price=price,
            category_id=category_id(category_name),
            status=status,
            is_available=status == 'con_mon',
        ))

    for i in range(1, 11):
        reserved_at = None
        reserved_until = None
        status = 'trong'
        if i == 2:
            status = 'da_dat'
            reserved_at = now_utc()
            reserved_until = reserved_at + timedelta(minutes=15)
        elif i == 3:
            status = 'dang_phuc_vu'

        db.session.add(DiningTable(
            table_number=f'B{i:02d}',
            seats=4 if i <= 8 else 6,
            status=status,
            reserved_at=reserved_at,
            reserved_until=reserved_until,
        ))

    db.session.add_all([
        Customer(
            full_name='Khach le',
            phone=None,
            note='Khach khong dang ky thanh vien',
            customer_type='khach_le',
            member_tier='thuong',
        ),
        Customer(
            full_name='Nguyen Minh Anh',
            phone='0901000001',
            note='Khach thanh vien hang vang',
            customer_type='thanh_vien',
            member_tier='vang',
            birth_date=date(1998, 5, 12),
        ),
    ])

    db.session.commit()
    print('Da tao CSDL mau thanh cong.')
    print('Tai khoan admin: admin / admin123')
    print('Tai khoan nhan vien: staff / staff123')
    print('Tai khoan thu ngan: cashier / cashier123')
