from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTestDatabase(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    access = Column(Integer, nullable=True)
    active = Column(Integer, nullable=True)
    start_active_time = Column(Date, nullable=True)
