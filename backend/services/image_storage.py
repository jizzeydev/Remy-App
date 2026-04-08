"""
Image Storage Service using Cloudinary
Stores images permanently in Cloudinary CDN - survives container restarts
"""
import cloudinary
import cloudinary.uploader
import cloudinary.utils
import os
import logging
import time
import base64
from typing import Optional

logger = logging.getLogger(__name__)

# Initialize Cloudinary on module load
def init_cloudinary():
    """Initialize Cloudinary configuration"""
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    if not all([cloud_name, api_key, api_secret]):
        logger.warning("Cloudinary credentials not fully configured")
        return False
    
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    logger.info(f"Cloudinary initialized with cloud: {cloud_name}")
    return True

# Initialize on import
_cloudinary_ready = init_cloudinary()


def init_image_storage(database=None):
    """
    Compatibility function - Cloudinary doesn't need database
    Called from server.py startup
    """
    global _cloudinary_ready
    if not _cloudinary_ready:
        _cloudinary_ready = init_cloudinary()
    logger.info("Image storage service ready (Cloudinary)")


async def save_image(
    file_content: bytes,
    filename: str,
    content_type: str = "image/png",
    metadata: Optional[dict] = None,
    folder: str = "remy/questions"
) -> str:
    """
    Upload an image to Cloudinary
    Returns the public_id (use this to build URLs)
    """
    if not _cloudinary_ready:
        raise Exception("Cloudinary not configured")
    
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type="image",
            quality="auto:good"
        )
        
        public_id = result.get("public_id")
        secure_url = result.get("secure_url")
        
        logger.info(f"Uploaded image to Cloudinary: {public_id} ({len(file_content)} bytes)")
        logger.info(f"Cloudinary URL: {secure_url}")
        
        # Return the public_id - we'll use this to build URLs
        return public_id
        
    except Exception as e:
        logger.error(f"Error uploading to Cloudinary: {e}")
        raise


async def save_image_base64(
    base64_data: str,
    filename: str = "image.png",
    content_type: str = "image/png",
    metadata: Optional[dict] = None,
    folder: str = "remy/questions"
) -> str:
    """
    Upload a base64 encoded image to Cloudinary
    """
    # Handle data URL format
    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]
    
    file_content = base64.b64decode(base64_data)
    return await save_image(file_content, filename, content_type, metadata, folder)


async def get_image(image_id: str) -> Optional[dict]:
    """
    Get image info from Cloudinary
    For Cloudinary, we typically just use the URL directly
    This is kept for compatibility but redirects are preferred
    """
    if not _cloudinary_ready:
        return None
    
    try:
        # Build the Cloudinary URL
        url = cloudinary.CloudinaryImage(image_id).build_url(
            secure=True,
            quality="auto",
            fetch_format="auto"
        )
        
        return {
            "url": url,
            "public_id": image_id,
            "content_type": "image/auto"
        }
    except Exception as e:
        logger.error(f"Error getting image {image_id}: {e}")
        return None


async def delete_image(image_id: str) -> bool:
    """Delete an image from Cloudinary"""
    if not _cloudinary_ready:
        return False
    
    try:
        result = cloudinary.uploader.destroy(image_id, invalidate=True)
        success = result.get("result") == "ok"
        if success:
            logger.info(f"Deleted image from Cloudinary: {image_id}")
        else:
            logger.warning(f"Could not delete image {image_id}: {result}")
        return success
    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {e}")
        return False


def get_image_url(image_id: str) -> str:
    """
    Generate the full Cloudinary URL for an image
    This returns a direct Cloudinary CDN URL (permanent!)
    """
    if not image_id:
        return ""
    
    # If it's already a full URL, return as-is
    if image_id.startswith("http"):
        return image_id
    
    # Build Cloudinary URL
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'de7loz0sr')
    
    # Handle both old GridFS IDs and new Cloudinary public_ids
    if "/" not in image_id and not image_id.startswith("remy"):
        # Old format - try to serve via our API (will return 404 if not found)
        return f"/api/images/{image_id}"
    
    # Cloudinary URL with automatic format and quality
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/q_auto,f_auto/{image_id}"


def generate_upload_signature(folder: str = "remy/questions") -> dict:
    """
    Generate a signed upload signature for frontend direct uploads
    """
    if not _cloudinary_ready:
        raise Exception("Cloudinary not configured")
    
    timestamp = int(time.time())
    
    params = {
        "timestamp": timestamp,
        "folder": folder,
    }
    
    signature = cloudinary.utils.api_sign_request(
        params,
        os.environ.get('CLOUDINARY_API_SECRET')
    )
    
    return {
        "signature": signature,
        "timestamp": timestamp,
        "cloud_name": os.environ.get('CLOUDINARY_CLOUD_NAME'),
        "api_key": os.environ.get('CLOUDINARY_API_KEY'),
        "folder": folder
    }
