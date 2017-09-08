# coding: utf-8
from datetime import datetime
from sqlalchemy.orm import contains_eager, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, BigInteger, DATE, VARCHAR
from sqlalchemy.orm import relationship, backref
DbBase = declarative_base()


class ViewInfo(DbBase):
    __tablename__ = 'view_info'
    date = Column(DATE, primary_key=True)
    pv = Column(BigInteger, default=0)
    uv = Column(BigInteger, default=0)


class User(DbBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(64), unique=True, index=True)
    phone = Column(Integer, unique=True)
    username = Column(VARCHAR(64), unique=True, index=True)
    password = Column(VARCHAR(128))
    created_at = Column(DateTime, default=datetime.now)


class Article(DbBase):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(64))
    view_num = Column(Integer, default=0)
    content = deferred(Column(Text))  # 延迟加载 http://docs.sqlalchemy.org/en/latest/orm/loading_columns.html
    create_time = Column(DateTime, index=True, default=datetime.now)
    update_time = deferred(Column(DateTime, index=True, default=datetime.now, onupdate=datetime.now))
    user_id = Column(Integer, ForeignKey('users.id'))
