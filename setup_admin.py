#!/usr/bin/env python
"""
Admin User Setup Script
This script creates an initial admin user in the museum app database.
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User

def create_admin():
    """Create an admin user in the database."""
    
    with app.app_context():
        # Create all tables first
        db.create_all()
        
        # Check if admin already exists
        admin_exists = User.query.filter_by(username="admin").first()
        if admin_exists:
            print("❌ Admin user 'admin' already exists.")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@museum.local",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Email: admin@museum.local")
            print("   Password: admin123")
            print("\n⚠️  Change this password after first login!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin()
