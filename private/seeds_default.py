import sys
import os
base_alembic_dir = os.path.abspath(os.path.dirname(__file__))
base_project_dir = os.path.dirname(base_alembic_dir)
sys.path.append(base_project_dir)

from app.models.auth_models import Client, Grant, Token, User, Role, Permission, RolePermission
from datetime import datetime, timedelta
from app import db, create_app

app = create_app('development')
app.app_context().push()

clients = [
    Client(
        name='dev', client_id='dev', client_secret='dev',
        redirect_uris=(
            'http://localhost:5000/authorized '
            'http://localhost/authorized'
        ),
    ),
    Client(
        name='dev2', client_id='dev2', client_secret='dev2',
        redirect_uris=(
            'http://localhost:8001/authorized '
            'http://localhost/authorized'
        ),
    )
]

roles = [
    Role(code=-100, name='deactived', title='Идэвхигүй'),
    Role(code=-10, name='banned', title='Хориглосон'),
    Role(code=-1, name='pending', title='Хүлээгдэж байгаа'),
    Role(code=0, name='guest', title='Зочин'),
    Role(code=1, name='root', title='Систем'),
    Role(code=10, name='admin', title='Админ'),
    Role(code=100, name='user', title='Хэрэглэгч'),
    Role(code=1000, name='director', title='Захирал'),
    Role(code=2000, name='accountant', title='Нягтлан'),
    Role(code=3000, name='chairman', title='Дарга'),
    Role(code=4000, name='stockkeeper', title='Нярав'),
    Role(code=5000, name='manager', title='Ажилтан')
]

permissions = [
    Permission(name='*'),
    Permission(name='all'),
    Permission(name='view_profile')
]

db.session.bulk_save_objects(clients)
db.session.bulk_save_objects(roles)
db.session.bulk_save_objects(permissions)
db.session.commit()

role_permissions = [RolePermission(role_id=5, permission_id=1)]

users = [
    User(username='root',
         email='root@odo.mn',
         password='p@ssw0rd',
         role_id=5),
    User(username='admin',
         email='admin@odo.mn',
         password='p@ssw0rd',
         role_id=6)
]

access_tokens = [
    Token(
        user_id=1, client_id='dev', access_token='expired', expires_in=0
    ),
    Token(
        user_id=1, client_id='dev', access_token='never_expire'
    )
]

db.session.bulk_save_objects(role_permissions)
db.session.bulk_save_objects(users)
db.session.commit()

db.session.bulk_save_objects(access_tokens)
db.session.commit()

from app.models.media_models import Gender, Unit, Quality, Business

genders = [
    Gender('male', 'Эрэгтэй'),
    Gender('female', 'Эмэгтэй'),
]

units = [
    Unit('piece', 'Ширхэг'),
    Unit('cask', 'Хайрцаг'),
    Unit('gramm', 'Грамм'),
    Unit('kilogramm', 'Килограмм'),
    Unit('tonn', 'Тонн'),
    Unit('millimeter', 'Миллиметр'),
    Unit('centimeter', 'Сантиметр'),
    Unit('meter', 'Метр'),
    Unit('kilometer', 'Километр'),
    Unit('millilitre', 'Миллилитр'),
    Unit('litre', 'Литр'),
    Unit('meterkb', 'Метр кв'),
    Unit('metercube', 'Метр куб'),
]

qualities = [
    Quality('Шинэ'),
    Quality('Хуучирсан'),
    Quality('Засвартай'),
    Quality('Ашиглах боломжгүй'),
    Quality('Хугацаа хэтэрсэн')
]

businesses = [
    Business('Дэлгүүр'),
    Business('Супермаркет'),
    Business('Их дэлгүүр'),
    Business('Баар паб'),
    Business('Рестран'),
]

db.session.bulk_save_objects(genders)
db.session.bulk_save_objects(units)
db.session.bulk_save_objects(qualities)
db.session.bulk_save_objects(businesses)
db.session.commit()

from app.models.company_models import Company, CompanyCustomer, Branch, BranchCustomer

companies = [
    Company(1, 1, 'Компани 1', 'AE998877'),
    Company(1, 1, 'Компани 2', 'BE001122'),
    Company(1, 1, 'Компани 3', 'CE001122'),
    Company(1, 1, 'Компани 4', 'DE001122'),
]
db.session.bulk_save_objects(companies)
db.session.commit()

company_customers = [
    CompanyCustomer(1, 2),
    CompanyCustomer(1, 3)
]
db.session.bulk_save_objects(company_customers)

branchs = [
    Branch(1, 'Салбар 1'),
    Branch(1, 'Салбар 2')
]
db.session.bulk_save_objects(branchs)
db.session.commit()

branch_customers = [
    BranchCustomer(1, 2),
    BranchCustomer(1, 3),
    BranchCustomer(1, 4),
]
db.session.bulk_save_objects(branch_customers)

db.session.commit()
