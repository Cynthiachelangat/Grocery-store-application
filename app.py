from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)