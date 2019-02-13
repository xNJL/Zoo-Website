from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# import database_project.App.config as config
import config
from .utils import DB

Config = config.Config
DB = DB.DB
db = DB()

app = Flask(__name__)
Bootstrap(app)

login = LoginManager(app)
login.login_view = 'auth.login'

app.config.from_object(Config)

from .auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/')

from .main import bp as main_bp
app.register_blueprint(main_bp, url_prefix='/')

from .admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from .staff import bp as staff_bp
app.register_blueprint(staff_bp, url_prefix='/staff')

from .visitor import bp as visitor_bp
app.register_blueprint(visitor_bp, url_prefix='/visitor')

if __name__ == '__main__':
    app.run()
