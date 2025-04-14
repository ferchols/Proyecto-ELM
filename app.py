from flask import Flask
import pyodbc
import os
from dotenv import load_dotenv
from contextlib import closing

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración centralizada
class Config:
    SQL_SERVER = os.getenv('SQL_SERVER')
    SQL_DATABASE = os.getenv('SQL_DATABASE')
    SQL_USERNAME = os.getenv('SQL_USERNAME')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD')
    SQL_PORT = os.getenv('SQL_PORT', '1433')
    SQL_DRIVER = 'ODBC Driver 17 for SQL Server'

app.config.from_object(Config)

def get_connection():
    """Crea y retorna una conexión a la base de datos"""
    conn_str = (
        f"DRIVER={app.config['SQL_DRIVER']};"
        f"SERVER={app.config['SQL_SERVER']},{app.config['SQL_PORT']};"
        f"DATABASE={app.config['SQL_DATABASE']};"
        f"UID={app.config['SQL_USERNAME']};"
        f"PWD={app.config['SQL_PASSWORD']};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route("/")
def home():
    try:
        with closing(get_connection()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT TOP 1 name FROM sys.tables")
                result = cursor.fetchone()
                
                if result:
                    return f"¡Conexión exitosa! Primera tabla: {result[0]}"
                return "Conexión exitosa pero no se encontraron tablas"
                
    except pyodbc.OperationalError as e:
        return f"Error de conexión: {str(e)}", 500
    except pyodbc.ProgrammingError as e:
        return f"Error en la consulta SQL: {str(e)}", 500
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')