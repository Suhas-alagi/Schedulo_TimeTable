"""
Seed script to add super admin user to MongoDB
"""

import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import datetime, UTC

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
faculty_collection = db['faculty']

# Admin user data
admin_data = {
    "name": "Super Admin",
    "short_name": "ADMIN",
    "email": "suhasalagi10@gmail.com",
    "password": generate_password_hash("Admin@123"),
    "role": "ADMIN",
    "title": "Administrator",
    "created_at": datetime.now(UTC)
}

def seed_admin():
    try:
        # Check if admin already exists
        existing_admin = faculty_collection.find_one({"email": admin_data["email"]})
        
        if existing_admin:
            print(f"⚠️  Admin user with email {admin_data['email']} already exists!")
            print(f"ID: {existing_admin['_id']}")
            print(f"Role: {existing_admin['role']}")
            return
        
        # Insert admin user
        result = faculty_collection.insert_one(admin_data)
        
        print("✅ Super admin user created successfully!")
        print(f"ID: {result.inserted_id}")
        print(f"Email: {admin_data['email']}")
        print(f"Role: {admin_data['role']}")
        print(f"Created at: {admin_data['created_at']}")
        
    except Exception as e:
        print(f"❌ Error seeding admin user: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    seed_admin()
