from app import db
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    def get_tablename(self):
        cn = self.__tablename__
        _i = cn.rfind('_')
        if _i > 0:
            return cn[:_i]
        else:
            return cn


class WithIdModel(BaseModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated = db.Column(db.TIMESTAMP, server_default=db.func.now(
    ), onupdate=db.func.current_timestamp())


class user_model(WithIdModel):
    def __init__(self):
        super(user_model, self).__init__()


u = user_model()
print(str(u.get_tablename()))
