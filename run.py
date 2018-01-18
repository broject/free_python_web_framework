import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
print(config_name)
app = create_app('development')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
if __name__ == '__main__':
    app.run()
