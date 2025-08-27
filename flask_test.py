import os
import sqlite3
import random
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = conn.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f"Welcome {username}!"
    return "Invalid credentials"

@app.route('/backup')
def backup_database():
    backup_name = request.args.get('name', 'backup')
    command = f"cp users.db backups/{backup_name}.db"
    os.system(command)
    return "Backup created"

@app.route('/download')
def download_file():
    filename = request.args.get('file')
    file_path = f"uploads/{filename}"
    return send_file(file_path)

@app.route('/generate_token')
def generate_token():
    token_length = 8
    token = ""
    for i in range(token_length):
        token += str(random.randint(0, 9))
    
    return f"Your security token: {token}"

@app.route('/ping')
def ping_server():
    host = request.args.get('host', 'localhost')
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return f"Ping result: {result.decode()}"

if __name__ == '__main__:
    init_db()
    app.run(debug=True)  # BUG 6: Debug mode in production
