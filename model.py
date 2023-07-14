from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

class Publisher(Base):
    __tablename__ = "publisher"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.VARCHAR(75), nullable=False)

class Shop(Base):
    __tablename__ = "shop"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.VARCHAR(75), nullable=False)

class Book(Base):
    __tablename__ = "book"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.VARCHAR(75), nullable=False)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

class Stock(Base):
    __tablename__ = "stock"

    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.Integer, sa.ForeignKey("book.id"), nullable=False)
    id_shop = sa.Column(sa.Integer, sa.ForeignKey("shop.id"), nullable=False)
    count = sa.Column(sa.Integer, nullable=False, default=1)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

    __table_args__ = (UniqueConstraint('id_book', 'id_shop', name='book_shop_uc'),
                      )
    
class Sale(Base):
    __tablename__ = "sale"

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    date_sale = sa.Column(sa.DateTime(), nullable=False, default=datetime.now())
    count = sa.Column(sa.Integer, nullable=False, default=1)
    id_stock = sa.Column(sa.Integer, sa.ForeignKey("stock.id"), nullable=False)

    stock = relationship(Stock, backref='sales')