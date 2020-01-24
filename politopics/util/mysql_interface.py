import os, yaml
import mysql.connector
import logging as log

log.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO
)
base_path = os.path.dirname(os.path.realpath(__file__))

class MySQLInterface():
        def __init__(self):
            self.connect()

        def connect(self):
            config_file = os.path.join(base_path,'../conf/config.yaml')
            with open(config_file, 'r') as f:
                db_config = yaml.load(f, Loader=yaml.FullLoader)['mysql_creds']

            self.db = mysql.connector.connect(
                host = db_config['host'],
                user = db_config['user'],
                passwd = db_config['password'],
                database = db_config['database'],
                charset="utf8mb4",
            )

        def execute(self, sql_file, vars):
            sql_fp = os.path.join(base_path, f'../sql/{sql_file}')
            with open(sql_fp, 'r') as f:
                sql = f.read()
            cursor = self.db.cursor()
            cursor.execute(sql, vars)
            self.db.commit()
