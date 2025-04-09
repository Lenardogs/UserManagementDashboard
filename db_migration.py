import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, text
from datetime import datetime

# Create a minimal Flask app for migration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///instance/database.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db = SQLAlchemy(app)

# Run this migration script to add the new columns to the tables
def main():
    # Soldering Tip table
    with app.app_context():
        db.session.execute(text("""
            ALTER TABLE soldering_tip 
            ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending' NOT NULL;
        """))
        db.session.execute(text("""
            ALTER TABLE soldering_tip 
            ADD COLUMN IF NOT EXISTS user_id INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE soldering_tip 
            ADD COLUMN IF NOT EXISTS approved_by INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE soldering_tip 
            ADD COLUMN IF NOT EXISTS approval_date TIMESTAMP;
        """))
        db.session.execute(text("""
            ALTER TABLE soldering_tip 
            ADD COLUMN IF NOT EXISTS rejection_reason TEXT;
        """))
        
        # Machine Calibration table
        db.session.execute(text("""
            ALTER TABLE machine_calibration 
            ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending' NOT NULL;
        """))
        db.session.execute(text("""
            ALTER TABLE machine_calibration 
            ADD COLUMN IF NOT EXISTS user_id INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE machine_calibration 
            ADD COLUMN IF NOT EXISTS approved_by INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE machine_calibration 
            ADD COLUMN IF NOT EXISTS approval_date TIMESTAMP;
        """))
        db.session.execute(text("""
            ALTER TABLE machine_calibration 
            ADD COLUMN IF NOT EXISTS rejection_reason TEXT;
        """))
        
        # Overtime Logbook table
        db.session.execute(text("""
            ALTER TABLE overtime_logbook 
            ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending' NOT NULL;
        """))
        db.session.execute(text("""
            ALTER TABLE overtime_logbook 
            ADD COLUMN IF NOT EXISTS user_id INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE overtime_logbook 
            ADD COLUMN IF NOT EXISTS approved_by INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE overtime_logbook 
            ADD COLUMN IF NOT EXISTS approval_date TIMESTAMP;
        """))
        db.session.execute(text("""
            ALTER TABLE overtime_logbook 
            ADD COLUMN IF NOT EXISTS rejection_reason TEXT;
        """))
        
        # Equipment Downtime table
        db.session.execute(text("""
            ALTER TABLE equipment_downtime 
            ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending' NOT NULL;
        """))
        db.session.execute(text("""
            ALTER TABLE equipment_downtime 
            ADD COLUMN IF NOT EXISTS user_id INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE equipment_downtime 
            ADD COLUMN IF NOT EXISTS approved_by INTEGER;
        """))
        db.session.execute(text("""
            ALTER TABLE equipment_downtime 
            ADD COLUMN IF NOT EXISTS approval_date TIMESTAMP;
        """))
        db.session.execute(text("""
            ALTER TABLE equipment_downtime 
            ADD COLUMN IF NOT EXISTS rejection_reason TEXT;
        """))
        
        db.session.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    main()