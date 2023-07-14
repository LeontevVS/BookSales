import os
import json
from model import Publisher, Book, Shop, Sale, Stock, create_tables, drop_tables

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_dns():
    dotenv.load_dotenv()
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_type = os.getenv("DB_TYPE")
    ip = os.getenv("IP")
    port = os.getenv("PORT")
    return f'{db_type}://{user}:{password}@{ip}:{port}/{db_name}'

def insert_test_data(session):
    with open('fixtures/tests_data.json', 'r') as file:
        data = json.load(file)
    models = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }
    for item in data:
        model = models.get(item.get("model"))
        session.add(model(id=item.get("pk"), **item.get("fields")))
    session.commit()

def print_publisher_sales(session):
    publisher_id = int(input("Введите id автора: "))
    subq_books = session.query(Book).filter(Book.id_publisher == publisher_id).subquery("publisher_books")
    subq_stocks = session.query(Stock).join(subq_books, Stock.id_book == subq_books.c.id).subquery("books_in_stocks")
    q = session.query(Sale).join(subq_stocks, Sale.id_stock == subq_stocks.c.id)
    for item in q.all():
        date_sale = f"{item.date_sale.day}-{item.date_sale.month}-{item.date_sale.year}"
        print(f"{item.stock.book.title} | {item.stock.shop.name} | {item.price} | {date_sale}")

if __name__ == '__main__':
    engine = create_engine(get_dns())
    Session = sessionmaker(bind=engine)
    session = Session()
    drop_tables(engine)
    create_tables(engine)
    insert_test_data(session)
    print_publisher_sales(session)
    session.close()