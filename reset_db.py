import os
from app import app, db
from models import User, SolderingTip, MachineCalibration, OvertimeLogbook, EquipmentDowntime
from werkzeug.security import generate_password_hash

# Drop and recreate all tables
with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables...")
    db.create_all()
    
    # Create a default admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    
    print("Database reset complete. Default admin user created.")