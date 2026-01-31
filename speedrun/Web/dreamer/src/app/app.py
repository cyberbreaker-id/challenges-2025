import os
import sqlite3
import uuid
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

app = Flask(__name__)
app.secret_key = os.urandom(64).hex()

DATABASE = 'notes.db'
ENCRYPTION_KEY = os.urandom(64).hex()

class Encryption:
    @staticmethod
    def encrypt_data(data, password):
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, 32)
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(salt + nonce + tag + ciphertext).decode('utf-8')
    
    @staticmethod
    def decrypt_data(encrypted_data, password):
        try:
            data = base64.b64decode(encrypted_data.encode('utf-8'))
            salt = data[:16]
            nonce = data[16:32]
            tag = data[32:48]
            ciphertext = data[48:]
            
            key = PBKDF2(password, salt, 32)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        except:
            return None

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flag (
            nice TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO flag (nice) VALUES ('%s')
    ''' % open('/flag.txt','r').read())
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    notes = []
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        encrypted_title = Encryption.encrypt_data(title, ENCRYPTION_KEY)
        encrypted_content = Encryption.encrypt_data(content, ENCRYPTION_KEY)
        
        conn = get_db_connection()
        note_id = str(uuid.uuid4())
        conn.execute('INSERT INTO notes (id, title, content) VALUES (?, ?, ?)', 
                    (note_id, encrypted_title, encrypted_content))
        conn.commit()
        conn.close()
        
        flash('Note added successfully!')
        return redirect(url_for('view_note', note_id=note_id))
    
    return render_template('add_note.html')

@app.route('/note/<string:note_id>')
def view_note(note_id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = "%s"' % (note_id,)).fetchone()
    conn.close()
    
    if not note:
        flash('Note not found!')
        return redirect(url_for('index'))
    
        
    encrypted_title = Encryption.encrypt_data(note['title'], ENCRYPTION_KEY)
    encrypted_content = Encryption.encrypt_data(note['content'], ENCRYPTION_KEY)
    note_data = {
        'title': encrypted_title,
        'content': encrypted_content,
    }
    
    return render_template('view_note.html', note=note_data)

@app.route('/secret')
def secret():
    return jsonify({"encryption_key":ENCRYPTION_KEY})


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5000)