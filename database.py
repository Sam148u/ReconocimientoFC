import sqlite3

# Crear la base de datos si no existe
def create_database():
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insertar un nuevo usuario
def insert_user(name, encoding):
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, encoding) VALUES (?, ?)', (name, encoding))
    conn.commit()
    conn.close()

# Obtener todos los usuarios registrados
def get_all_users():
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('SELECT name, encoding FROM users')
    results = c.fetchall()
    conn.close()
    return results

def delete_user(name):
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

    

