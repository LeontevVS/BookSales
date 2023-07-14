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
    user_input = input("Введите id или имя автора: ")
    try:
        search_data = int(user_input)
    except:
        search_data = user_input
    q = session.query(
        Book.title, 
        Shop.name, 
        Sale.price, 
        Sale.date_sale
        ).select_from(Publisher).\
            join(Book, Publisher.id == Book.id_publisher).\
            join(Stock, Stock.id_book == Book.id).\
            join(Shop, Shop.id == Stock.id_shop).\
            join(Sale, Sale.id_stock == Stock.id).\
            filter(Publisher.id == search_data if isinstance(search_data, int) else Publisher.name == search_data)
    for item in q.all():
        print(f"{item[0]: <40} | {item[1]: <10} | {item[2]: <8} | {item[3].strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    engine = create_engine(get_dns())
    Session = sessionmaker(bind=engine)
    session = Session()
    drop_tables(engine)
    create_tables(engine)
    insert_test_data(session)
    print_publisher_sales(session)
    session.close()