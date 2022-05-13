from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class AllRequests(Base):
    __tablename__ = 'all_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)


class RequestsByType(Base):
    __tablename__ = 'requests_by_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(4), nullable=False)
    quantity = Column(Integer, nullable=False)


class TheMostFrequentRequests(Base):
    __tablename__ = 'the_most_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)


class ClientBasedErrors(Base):
    __tablename__ = 'client_based_errors'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    size = Column(Integer, nullable=False)
    ip_address = Column(String(15), nullable=False)
    status_code = Column(Integer, nullable=False)


class ServerBasedErrors(Base):
    __tablename__ = 'server_based_errors'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(15), nullable=False)
    quantity = Column(Integer, nullable=False)
