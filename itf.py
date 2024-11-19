import requests
import pandas as pd
import json
import csv
import datetime
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from io import StringIO


conf ={
    'host':"itfranking.cbkg2yy0m7td.ap-southeast-2.rds.amazonaws.com",
    'port':'3306',
    'database':"ITFRanking",
    'user':"koolio",
    'password':"Jaeger01**"
}
engine = create_engine("mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}".format(**conf))
metadata = MetaData()

# Define the table
user_table = Table('itf_junior_female', metadata,
    Column('id', Integer, primary_key=True),
    Column('family_name', String(100)),
    Column('given_name', String(100)),
    Column('nationality', String(100)),
    Column('birth_year', String(4)),
    Column('rank', String(4)),
    Column('tournaments_played', String(50)),
    Column('points', String(50)),
    Column('fullname', String(100))
)

# Create the table in the database
metadata.create_all(engine)

req = requests.get(
  url='https://www.itftennis.com/tennis/api/PlayerRankApi/GetPlayerRankings?circuitCode=JT&playerTypeCode=G&juniorRankingType=itf&take=3000&skip=0&isOrderAscending=true',
)
url_content = req.content
if req.status_code == 200:
  status = req.status_code
  now = datetime.datetime.now()
  current = now.strftime('%d-%m-%Y')
  convert_json = json.loads(url_content)
  last_updated = convert_json['rankDate']
  final_data = convert_json['items']
else:
  status = req.status_code
print(status) 