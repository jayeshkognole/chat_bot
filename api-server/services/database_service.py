import sqlite3

DATABASE = 'chatbot.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_tab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tab_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_tab_id INTEGER NOT NULL,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            refrence TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (chat_tab_id) REFERENCES chat_tab (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_file(user_id, filename, filepath):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file (user_id, filename, filepath) VALUES (?, ?, ?)", (user_id, filename, filepath))
    conn.commit()
    conn.close()

def get_files_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM file WHERE user_id = ?", (user_id,))
    files = cursor.fetchall()
    conn.close()
    return files

def create_chat_tab(user_id, tab_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_tab (user_id, tab_name) VALUES (?, ?)", (user_id, tab_name))
    chat_tab_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return chat_tab_id

def create_message(user_id, chat_tab_id, user_message, ai_response, refrence):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO message (user_id, chat_tab_id, user_message, ai_response, refrence) VALUES (?, ?, ?, ?, ?)", (user_id, chat_tab_id, user_message, ai_response, refrence))
    conn.commit()
    conn.close()

def get_chat_history(user_id, chat_tab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_message, ai_response, refrence FROM message WHERE user_id = ? AND chat_tab_id = ?", (user_id, chat_tab_id))
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_chat_tabs(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_tab WHERE user_id = ?", (user_id,))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_tab WHERE user_id = ?", (user_id,))
    chat_tabs = cursor.fetchall()
    conn.close()
    return chat_tabs

def delete_chat_tab(chat_tab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_tab WHERE id = ?", (chat_tab_id,))
    conn.commit()
    conn.close()

def edit_chat_tab(chat_tab_id, tab_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE chat_tab SET tab_name = ? WHERE id = ?", (tab_name, chat_tab_id,))
    conn.commit()
    conn.close()

def get_conversational_history( chat_tab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, ai_response FROM message WHERE chat_tab_id = ? ORDER BY timestamp DESC", (chat_tab_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages
