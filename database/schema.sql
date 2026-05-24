-- Lược đồ CSDL tóm tắt cho đề tài Web API quản lý nhà hàng sushi
-- Khi chạy seed.py, Flask-SQLAlchemy sẽ tự tạo đầy đủ bảng theo models.

roles(id, name, description)
users(id, full_name, username, password_hash, role_id, is_active, created_at)
access_tokens(id, token, user_id, created_at, is_revoked)
categories(id, name, description)
menu_items(id, name, description, price, category_id, is_available)
tables(id, table_number, seats, status)
customers(id, full_name, phone, note)
orders(id, table_id, customer_id, created_by_user_id, status, total_amount, created_at)
order_details(id, order_id, menu_item_id, quantity, unit_price, subtotal)
payments(id, order_id, payment_method, amount, paid_at)
