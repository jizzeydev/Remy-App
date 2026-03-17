"""
Image Storage Service using MongoDB GridFS
Stores images persistently in MongoDB to avoid losing them on container restarts
"""
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from datetime import datetime, timezone
from typing import Optional
import logging
import uuid
import base64

logger = logging.getLogger(__name__)

# Global GridFS bucket
gridfs_bucket = None
db = None


def init_image_storage(database):
    """Initialize GridFS bucket with database"""
    global gridfs_bucket, db
    db = database
    gridfs_bucket = AsyncIOMotorGridFSBucket(database)
    logger.info("Image storage service initialized with GridFS")


async def save_image(
    file_content: bytes,
    filename: str,
    content_type: str = "image/png",
    metadata: Optional[dict] = None
) -> str:
    """
    Save an image to MongoDB GridFS
    Returns the image ID (use this to retrieve the image)
    """
    if not gridfs_bucket:
        raise Exception("Image storage not initialized")
    
    image_id = str(uuid.uuid4())
    ext = filename.split('.')[-1] if '.' in filename else 'png'
    stored_filename = f"{image_id}.{ext}"
    
    file_metadata = {
        "original_filename": filename,
        "content_type": content_type,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        **(metadata or {})
    }
    
    # Upload to GridFS
    await gridfs_bucket.upload_from_stream(
        stored_filename,
        file_content,
        metadata=file_metadata
    )
    
    logger.info(f"Saved image {stored_filename} to GridFS ({len(file_content)} bytes)")
    
    return image_id


async def get_image(image_id: str) -> Optional[dict]:
    """
    Retrieve an image from MongoDB GridFS
    Returns dict with content (bytes), content_type, and filename
    """
    if not gridfs_bucket:
        raise Exception("Image storage not initialized")
    
    # Find file by ID prefix in filename
    try:
        # GridFS stores files with filenames, search by prefix
        cursor = gridfs_bucket.find({"filename": {"$regex": f"^{image_id}"}})
        file_doc = await cursor.to_list(1)
        
        if not file_doc:
            logger.warning(f"Image not found: {image_id}")
            return None
        
        file_info = file_doc[0]
        
        # Download content
        stream = await gridfs_bucket.open_download_stream(file_info["_id"])
        content = await stream.read()
        
        return {
            "content": content,
            "content_type": file_info.get("metadata", {}).get("content_type", "image/png"),
            "filename": file_info["filename"],
            "size": len(content)
        }
    except Exception as e:
        logger.error(f"Error retrieving image {image_id}: {e}")
        return None


async def delete_image(image_id: str) -> bool:
    """Delete an image from GridFS"""
    if not gridfs_bucket:
        raise Exception("Image storage not initialized")
    
    try:
        cursor = gridfs_bucket.find({"filename": {"$regex": f"^{image_id}"}})
        file_doc = await cursor.to_list(1)
        
        if file_doc:
            await gridfs_bucket.delete(file_doc[0]["_id"])
            logger.info(f"Deleted image {image_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {e}")
        return False


async def save_image_base64(
    base64_data: str,
    filename: str = "image.png",
    content_type: str = "image/png",
    metadata: Optional[dict] = None
) -> str:
    """
    Save a base64 encoded image to MongoDB GridFS
    """
    # Remove data URL prefix if present
    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]
    
    file_content = base64.b64decode(base64_data)
    return await save_image(file_content, filename, content_type, metadata)


def get_image_url(image_id: str) -> str:
    """Generate the URL to access an image"""
    return f"/api/images/{image_id}"
