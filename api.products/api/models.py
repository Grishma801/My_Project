import os
from peewee import (
    Model,
    IntegerField,
    CharField,
    Field
)
from playhouse.mysql_ext import MariaDBConnectorDatabase

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

db = MariaDBConnectorDatabase(
    'marz',
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT
)

