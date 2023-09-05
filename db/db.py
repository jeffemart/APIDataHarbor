import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco de dados
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Função para conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Função para executar consultas SQL
def execute_query(query, params=None):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print("Erro ao executar a consulta SQL:", e)
            conn.rollback()
            cursor.close()
            conn.close()
            return None
    else:
        return None
