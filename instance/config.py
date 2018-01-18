import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/test?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}
SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True
SECURITY_PASSWORD_SALT = "eco"
SECURITY_PASSWORD_HASH = "bcrypt"
# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"
# Secret key for signing cookies
SECRET_KEY = "secret"