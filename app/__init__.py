from flask import Flask
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.category_controller import category_bp
    from app.controllers.menu_item_controller import menu_item_bp
    from app.controllers.table_controller import table_bp
    from app.controllers.customer_controller import customer_bp
    from app.controllers.order_controller import order_bp
    from payment_app.controllers.payment_controller import payment_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.statistic_controller import statistic_bp
    from app.controllers.invoice_controller import invoice_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(menu_item_bp)
    app.register_blueprint(table_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(statistic_bp)
    app.register_blueprint(invoice_bp)

    @app.get('/api/health')
    def health():
        return {'message': 'Sushi Restaurant API is running'}

    return app
