from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
import configparser
from services.database_service import get_db_connection, create_tables
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

config = configparser.ConfigParser()
config.read('config.ini')

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    create_tables()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create a dummy user
    cursor.execute("SELECT * FROM user WHERE username = ?", ('dummy',))
    dummy_user = cursor.fetchone()
    if not dummy_user:
        hashed_password = generate_password_hash('dummy')
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ('dummy', hashed_password))
        conn.commit()

    # Create a default chat tab for the dummy user
    cursor.execute("SELECT * FROM user WHERE username = ?", ('Default Chat',))
    default_chat_tab = cursor.fetchone()
    if not default_chat_tab:
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ('Default Chat', ''))
        conn.commit()

    conn.close()
    app.run(debug=True, port=5001)
