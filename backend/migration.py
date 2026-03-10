#!/usr/bin/env python3
"""
Migration Script for Remy Platform
Exports data from the preview database to JSON files for import into production.

Usage:
  1. Export (from preview environment):
     python migration.py export
     
  2. Import (in production):
     python migration.py import
     
Collections exported:
  - courses
  - chapters
  - lessons
  - questions
  - formulas
  - materials
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Export directory
EXPORT_DIR = ROOT_DIR / 'migration_data'

# Collections to migrate (content only, not user data)
COLLECTIONS = [
    'courses',
    'chapters', 
    'lessons',
    'questions',
    'formulas',
    'materials'
]

async def connect_db():
    """Connect to MongoDB"""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print(f"📦 Connected to database: {db_name}")
    return client, db

async def export_data():
    """Export all content collections to JSON files"""
    EXPORT_DIR.mkdir(exist_ok=True)
    
    client, db = await connect_db()
    
    try:
        export_summary = {
            'exported_at': datetime.now(timezone.utc).isoformat(),
            'collections': {}
        }
        
        for collection_name in COLLECTIONS:
            print(f"\n📤 Exporting {collection_name}...")
            
            # Get all documents, excluding MongoDB _id
            docs = await db[collection_name].find({}, {'_id': 0}).to_list(10000)
            
            if docs:
                # Convert any datetime objects to ISO strings
                for doc in docs:
                    for key, value in doc.items():
                        if isinstance(value, datetime):
                            doc[key] = value.isoformat()
                
                # Save to JSON file
                export_file = EXPORT_DIR / f'{collection_name}.json'
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(docs, f, ensure_ascii=False, indent=2)
                
                print(f"   ✅ Exported {len(docs)} documents to {export_file.name}")
                export_summary['collections'][collection_name] = len(docs)
            else:
                print(f"   ⚠️ No documents found in {collection_name}")
                export_summary['collections'][collection_name] = 0
        
        # Save summary
        summary_file = EXPORT_DIR / '_export_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(export_summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*50}")
        print("✅ EXPORT COMPLETE!")
        print(f"{'='*50}")
        print(f"📁 Files saved to: {EXPORT_DIR}")
        print("\nSummary:")
        for coll, count in export_summary['collections'].items():
            print(f"   • {coll}: {count} documents")
        
        print(f"\n📋 Next steps:")
        print("   1. Copy the 'migration_data' folder to your production server")
        print("   2. Run: python migration.py import")
        
    finally:
        client.close()

async def import_data():
    """Import data from JSON files into database"""
    if not EXPORT_DIR.exists():
        print("❌ Error: migration_data folder not found")
        print("   Run 'python migration.py export' first or copy the folder here")
        return
    
    client, db = await connect_db()
    
    try:
        print("\n⚠️  WARNING: This will ADD data to your database")
        print("   Existing documents with same IDs may cause duplicates")
        
        confirm = input("\nProceed? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Import cancelled")
            return
        
        import_summary = {
            'imported_at': datetime.now(timezone.utc).isoformat(),
            'collections': {}
        }
        
        for collection_name in COLLECTIONS:
            import_file = EXPORT_DIR / f'{collection_name}.json'
            
            if not import_file.exists():
                print(f"\n⚠️ Skipping {collection_name} - file not found")
                continue
            
            print(f"\n📥 Importing {collection_name}...")
            
            with open(import_file, 'r', encoding='utf-8') as f:
                docs = json.load(f)
            
            if not docs:
                print(f"   ⚠️ No documents to import")
                continue
            
            # Check for existing documents and handle upsert
            imported = 0
            updated = 0
            
            for doc in docs:
                doc_id = doc.get('id')
                if doc_id:
                    # Upsert: update if exists, insert if not
                    result = await db[collection_name].update_one(
                        {'id': doc_id},
                        {'$set': doc},
                        upsert=True
                    )
                    if result.upserted_id:
                        imported += 1
                    else:
                        updated += 1
                else:
                    # No id field, just insert
                    await db[collection_name].insert_one(doc)
                    imported += 1
            
            print(f"   ✅ Imported: {imported}, Updated: {updated}")
            import_summary['collections'][collection_name] = {
                'imported': imported,
                'updated': updated
            }
        
        print(f"\n{'='*50}")
        print("✅ IMPORT COMPLETE!")
        print(f"{'='*50}")
        print("\nSummary:")
        for coll, stats in import_summary['collections'].items():
            print(f"   • {coll}: {stats['imported']} new, {stats['updated']} updated")
        
    finally:
        client.close()

async def show_stats():
    """Show current database statistics"""
    client, db = await connect_db()
    
    try:
        print(f"\n{'='*50}")
        print("📊 DATABASE STATISTICS")
        print(f"{'='*50}")
        
        for collection_name in COLLECTIONS:
            count = await db[collection_name].count_documents({})
            print(f"   • {collection_name}: {count} documents")
        
    finally:
        client.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python migration.py [export|import|stats]")
        print("\nCommands:")
        print("  export  - Export data to JSON files")
        print("  import  - Import data from JSON files")  
        print("  stats   - Show current database statistics")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        asyncio.run(export_data())
    elif command == 'import':
        asyncio.run(import_data())
    elif command == 'stats':
        asyncio.run(show_stats())
    else:
        print(f"Unknown command: {command}")
        print("Use: export, import, or stats")

if __name__ == '__main__':
    main()
