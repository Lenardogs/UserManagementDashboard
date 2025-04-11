from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin user exists
    if not User.query.filter_by(username='admin').first():
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')
    else:
        print('Admin user already exists!')