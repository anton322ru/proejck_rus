from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nikname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    mistakes_4 = Column(String, nullable=True)
    mistakes_9 = Column(String, nullable=True)
    mistakes_10 = Column(String, nullable=True)
    mistakes_22 = Column(String, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)