from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

class LoginEvent(object):
    def __init__(self, user_id, ip_address, user_agent, login_time):
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.login_time = login_time

def format_login_event(format_string, login_event):
    return format_string.format(login_event=login_event)

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes = db.relationship('Note', backref='author', lazy=True)
    login_logs = db.relationship('LoginLog', backref='user', lazy=True)

class Note(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

class LoginLog(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=False)
    login_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

@app.before_request
def create_tables():
    if not hasattr(create_tables, 'done'):
        db.create_all()
        create_tables.done = True

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    notes = Note.query.filter_by(user_id=session['user_id']).order_by(Note.updated_at.desc()).all()
    return render_template('index.html', user=user, notes=notes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            
            login_log = LoginLog(
                user_id=user.id,
                ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown')),
                user_agent=request.user_agent.string,
                login_time=datetime.utcnow()
            )
            db.session.add(login_log)
            db.session.commit()
            
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        note = Note(
            title=title,
            content=content,
            user_id=session['user_id']
        )
        db.session.add(note)
        db.session.commit()
        
        flash('Note added successfully')
        return redirect(url_for('index'))
    
    return render_template('add_note.html')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != session['user_id']:
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Note updated successfully')
        return redirect(url_for('index'))
    
    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != session['user_id']:
        flash('Access denied')
        return redirect(url_for('index'))
    
    db.session.delete(note)
    db.session.commit()
    
    flash('Note deleted successfully')
    return redirect(url_for('index'))

@app.route('/login_history')
def login_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    login_logs = LoginLog.query.filter_by(user_id=session['user_id']).order_by(LoginLog.login_time.desc()).all()
    
    formatted_logs = []
    for log in login_logs:
        login_event = LoginEvent(
            user_id=log.user_id,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            login_time=log.login_time
        )
        formatted_event = format_login_event(f"[+] User login from {log.ip_address} at {log.login_time} using {log.user_agent}", login_event=login_event)
        formatted_logs.append({
            'original': log,
            'formatted': formatted_event
        })
    
    return render_template('login_history.html', login_logs=formatted_logs)

@app.route('/debug')
def debug():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    
    return render_template_string(request.args.get('template'))

if __name__ == '__main__':
    from migrate import create_admin_user
    create_admin_user()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=3002)
