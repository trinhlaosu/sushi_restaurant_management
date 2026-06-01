from app import create_app
from app.extensions import db
from app.models import (
    Category,
    Customer,
    DiningTable,
    Ingredient,
    MenuItem,
    MenuItemIngredient,
    Role,
    User,
)

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_role = Role(name='admin', description='Quản trị viên hệ thống')
    staff_role = Role(name='staff', description='Nhân viên nhà hàng')
    cashier_role = Role(name='cashier', description='Thu ngân')
    db.session.add_all([admin_role, staff_role, cashier_role])
    db.session.flush()

    admin = User(full_name='Quản trị viên', username='admin', role_id=admin_role.id)
    admin.set_password('admin123')
    staff = User(full_name='Nhân viên bán hàng', username='staff', role_id=staff_role.id)
    staff.set_password('staff123')
    cashier = User(full_name='Thu ngân', username='cashier', role_id=cashier_role.id)
    cashier.set_password('cashier123')
    db.session.add_all([admin, staff, cashier])

    category_names = [
        ('Sushi', 'Các món sushi/nigiri'),
        ('Sashimi', 'Các món sashimi cá sống'),
        ('Maki / Cuộn', 'Các món cuộn kiểu Nhật'),
        ('Set / Combo', 'Combo dùng theo nhóm'),
        ('Món nướng / chiên', 'Món ăn nóng'),
        ('Cơm / Mì', 'Món chính dùng no'),
        ('Đồ uống', 'Nước uống dùng kèm'),
    ]
    categories = []
    for name, description in category_names:
        category = Category(name=name, description=description)
        db.session.add(category)
        categories.append(category)
    db.session.flush()

    def c(name):
        return next(category for category in categories if category.name == name).id

    menu_items = [
        ('Cá hồi Nigiri', 'Sushi cá hồi', 45000, 'Sushi'),
        ('Cá ngừ Nigiri', 'Sushi cá ngừ', 42000, 'Sushi'),
        ('Lươn Nhật Nigiri', 'Sushi lươn Nhật sốt kabayaki', 65000, 'Sushi'),
        ('Sashimi cá hồi', 'Cá hồi tươi cắt lát', 129000, 'Sashimi'),
        ('Sashimi cá ngừ', 'Cá ngừ tươi cắt lát', 119000, 'Sashimi'),
        ('Set Sashimi Tổng Hợp', 'Set sashimi dùng cho 2 người', 399000, 'Set / Combo'),
        ('California Roll', 'Cuộn thanh cua, bơ và trứng cá', 89000, 'Maki / Cuộn'),
        ('Cuốn cá hồi phủ cheese', 'Cuộn cá hồi phủ phô mai đút lò', 139000, 'Maki / Cuộn'),
        ('Cuốn hải sản chiên xù sốt spicy', 'Cuộn hải sản chiên xù dùng sốt cay', 129000, 'Maki / Cuộn'),
        ('Hàu nướng Misoyaki', 'Hàu nướng sốt miso', 99000, 'Món nướng / chiên'),
        ('Tempura tôm', 'Tôm chiên tempura', 89000, 'Món nướng / chiên'),
        ('Cơm lươn Nhật', 'Cơm lươn sốt kabayaki', 169000, 'Cơm / Mì'),
        ('Mì Udon bò', 'Mì udon dùng với thịt bò', 119000, 'Cơm / Mì'),
        ('Trà đào', 'Trà đào lạnh', 35000, 'Đồ uống'),
        ('Matcha Latte', 'Matcha latte đá', 45000, 'Đồ uống'),
        ('Nước suối', 'Nước suối đóng chai', 12000, 'Đồ uống'),
    ]

    first_menu_item = None
    for name, description, price, category_name in menu_items:
        menu_item = MenuItem(
            name=name,
            description=description,
            price=price,
            category_id=c(category_name),
        )
        db.session.add(menu_item)
        if first_menu_item is None:
            first_menu_item = menu_item

    for i in range(1, 11):
        db.session.add(DiningTable(table_number=f'B{i:02d}', seats=4 if i <= 8 else 6))

    db.session.add_all([
        Customer(full_name='Khách lẻ', phone=None, note='Khách không đăng ký thành viên'),
        Customer(full_name='Nguyễn Minh Anh', phone='0901000001', note='Khách thành viên'),
        Customer(full_name='Trần Quốc Bảo', phone='0901000002', note='Thường gọi sashimi'),
    ])

    db.session.flush()

    salmon = Ingredient(name='Cá hồi', unit='gram', stock_quantity=5000, min_quantity=500)
    rice = Ingredient(name='Cơm sushi', unit='gram', stock_quantity=10000, min_quantity=1000)
    db.session.add_all([salmon, rice])
    db.session.flush()

    db.session.add_all([
        MenuItemIngredient(menu_item_id=first_menu_item.id, ingredient_id=salmon.id, quantity=30),
        MenuItemIngredient(menu_item_id=first_menu_item.id, ingredient_id=rice.id, quantity=40),
    ])

    db.session.commit()
    print('Đã tạo CSDL mẫu thành công.')
    print('Tài khoản admin: admin / admin123')
    print('Tài khoản nhân viên: staff / staff123')
    print('Tài khoản thu ngân: cashier / cashier123')
