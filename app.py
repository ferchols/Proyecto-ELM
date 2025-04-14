from flask import Flask
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración desde variables de entorno
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
port = os.getenv('SQL_PORT', '1433')

@app.route("/")
def home():
    try:
        # Cadena de conexión compatible con Render
        conn_str = f"""
            DRIVER=ODBC Driver 17 for SQL Server;
            SERVER={server},{port};
            DATABASE={database};
            UID={username};
            PWD={password};
            Encrypt=yes;
            TrustServerCertificate=yes;
        """
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 name FROM sys.tables")
        result = cursor.fetchone()
        return f"¡Conexión exitosa! Primera tabla: {result[0]}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)