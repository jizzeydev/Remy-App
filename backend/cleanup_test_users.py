#!/usr/bin/env python3
"""
Production Database Cleanup Script
Run this ONCE after deployment to remove test users

Usage:
  python cleanup_test_users.py

This will:
  1. Show all users in the database
  2. Ask for confirmation before deleting test users
  3. Keep only real user emails
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Real user emails to KEEP (modify this list as needed)
REAL_USER_EMAILS = [
    'jordi.bravo.bad@gmail.com',
    'seremonta.cl@gmail.com', 
    'j.bravo.silva@uc.cl',
    'jesusalonso.bravosilva@gmail.com'
]

async def cleanup():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 50)
    print("🧹 PRODUCTION DATABASE CLEANUP")
    print("=" * 50)
    
    # Show current users
    all_users = await db.users.find({}, {"_id": 0, "email": 1, "name": 1}).to_list(100)
    
    print(f"\n📊 Found {len(all_users)} total users:\n")
    
    to_delete = []
    to_keep = []
    
    for u in all_users:
        email = u.get('email', '')
        name = u.get('name', 'N/A')
        if email.lower() in [e.lower() for e in REAL_USER_EMAILS]:
            to_keep.append(email)
            print(f"  ✅ KEEP: {email} ({name})")
        else:
            to_delete.append(email)
            print(f"  ❌ DELETE: {email} ({name})")
    
    print(f"\n📋 Summary:")
    print(f"   To keep: {len(to_keep)} users")
    print(f"   To delete: {len(to_delete)} users")
    
    if not to_delete:
        print("\n✨ No test users to delete. Database is clean!")
        client.close()
        return
    
    # Confirm deletion
    print("\n⚠️  This action cannot be undone!")
    confirm = input("Type 'DELETE' to confirm deletion: ")
    
    if confirm != 'DELETE':
        print("❌ Cancelled. No changes made.")
        client.close()
        return
    
    # Delete test users
    result = await db.users.delete_many({
        "email": {"$nin": REAL_USER_EMAILS}
    })
    
    # Clean up sessions
    await db.user_sessions.delete_many({})
    
    print(f"\n✅ Deleted {result.deleted_count} test users")
    print("✅ Cleaned up all sessions")
    
    # Final count
    final_count = await db.users.count_documents({})
    print(f"\n📊 Final user count: {final_count}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(cleanup())
