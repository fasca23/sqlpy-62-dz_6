import json
from requests import session
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:1111111@localhost:5432/test'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)

session = Session()

with open('test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

def search_id(id1):
    while True:
        if id1.isdigit():
            for i in session.query(Publisher).filter(Publisher.id==id1).all():
                return i
        else: break

def search_pub(pub):
    for i in session.query(Publisher).filter(Publisher.name==pub).all():
        return i

while True:
    team = input('\nВведите команду id или pub (exit - выход): ')
    if team == 'id':

        id1 = input('\nДля поиска введите значение id: ')
        print(search_id(id1))

    elif team == 'pub':

        pub = input('\nДля поиска введите значение pub: ')
        print(search_pub(pub))

    elif team == 'exit':
        print('\nВы вышли из программы')
        break

    else: print('\nНеправильная команда')
