from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#init databse
db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_database():
    db.create_all()
    print('DB CRATED')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "my secret key"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(admin,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    #with app.app_context():
    #    create_database()
    
    return app