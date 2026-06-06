-- Lược đồ CSDL tóm tắt cho đề tài Web API quản lý nhà hàng sushi
-- Khi chạy seed.py, Flask-SQLAlchemy sẽ tự tạo đầy đủ bảng theo models.
-- Cơ sở dữ liệu được tối ưu hóa với 10 bảng chính

roles(id, name, description)
users(id, full_name, username, password_hash, role_id, is_active, created_at)
access_tokens(id, token, user_id, created_at, is_revoked)
categories(id, name, description)
menu_items(id, name, description, price, category_id, is_available, status)
dining_tables(id, table_number, seats, status, reserved_at, reserved_until)
customers(id, full_name, phone, note, customer_type, member_tier, birth_date)
orders(id, table_id, customer_id, created_by_user_id, status, total_amount, discount_percent, discount_amount, final_amount, promotion_note, gift_item, created_at)
order_details(id, order_id, menu_item_id, quantity, unit_price, subtotal)
payments(id, order_id, payment_method, amount, paid_at)
