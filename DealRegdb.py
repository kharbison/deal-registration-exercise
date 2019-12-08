from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine('postgresql://kate:@localhost:5432/DealRegDB')

if not database_exists(engine.url):
    print('Creating Database')
    create_database(engine.url)

print(database_exists(engine.url))


#Session = sessionmaker(bind=engine)
