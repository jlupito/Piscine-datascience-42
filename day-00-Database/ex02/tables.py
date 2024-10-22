import pandas as pd
from sqlalchemy import * #pour interagir avec la BDD SQL
from sqlalchemy_utils import * # #utilitaires en +, par ex verif l existence dune BDD ou sa creation


#step 1: creer le moteur et connexion a la BDD

#create_engine("mysql+mysqlconnector://username:password@hostname:port/database_name")
engine = create_engine("postgresql+psycopg2://jarthaud:mysecretpassword@localhost:5432/piscineds")
if not database_exists(engine.url):
  create_database(engine.url)
else:
  engine.connect()

#step 2: creer les tables et definir la stucture

#on definie les tables de la BDD via la class MetaData()
metadata = MetaData() 
my_table = Table('my_table', metadata,
  Column('event_time',DateTime),
  Column('event_type',String(255)),
  Column('product_id',String(255)),
  Column('price',Float),
  Column('user_id',Integer),
  Column('user_session',String(255))
)

# puis on crée toutes les tables définies dans MetaData dans la base de données
metadata.create_all(engine)

df = pd.read_csv('data_2022_oct.csv')

# on ajoute le append pour ne pas supprimer les anciennes donnees et juste ajouter les nouvelles
df.to_sql('my_table', engine, if_exists='append', index=False)