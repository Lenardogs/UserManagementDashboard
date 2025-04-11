from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('Admin user found, resetting password...')
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print('Admin password reset successfully!')
    else:
        print('Admin user not found!')