import secrets
import string
import os
from app import app, db, User
from werkzeug.security import generate_password_hash

def generate_random_password(length=32):
    """Generate a random password with letters, digits, and symbols"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def create_admin_user():
    """Create admin user with random password"""
    with app.app_context():
        # Remove database if it exists
        db_path = 'instance/notes.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")
        
        # Create all tables
        db.create_all()
        print("Created new database tables")
        
        # Generate random password
        admin_password = generate_random_password()
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@notes.app',
            password_hash=generate_password_hash(admin_password)
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("=" * 50)
        print("ADMIN USER CREATED SUCCESSFULLY")
        print("=" * 50)
        print(f"Username: admin")
        print(f"Password: {admin_password}")
        print(f"Email: admin@notes.app")
        print("=" * 50)

if __name__ == '__main__':
    create_admin_user()