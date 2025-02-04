from flask import Flask
import fdb

app = Flask(__name__)
app.config.from_pyfile('config.py')


host = app.config.get('DB_HOST')
database = app.config.get('DB_NAME')
user = app.config.get('DB_USER')
password = app.config.get('DB_PASSWORD')

try:
    con = fdb.connect(host=host, database=database, user=user, password=password)
    print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")


from view import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
