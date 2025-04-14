from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración PostgreSQL
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT', '5432')  # Puerto por defecto de PostgreSQL

@app.route("/")
def home():
    try:
        # Cadena de conexión a PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        
        with conn.cursor() as cursor:
            # Consulta para PostgreSQL (diferente a SQL Server)
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 1")
            result = cursor.fetchone()
            
            if result:
                return f"¡Conexión exitosa! Primera tabla: {result[0]}"
            return "Conexión exitosa pero no se encontraron tablas"
            
    except psycopg2.OperationalError as e:
        return f"Error de conexión: {str(e)}", 500
    except psycopg2.ProgrammingError as e:
        return f"Error en la consulta SQL: {str(e)}", 500
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')