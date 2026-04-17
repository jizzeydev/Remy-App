"""
Image API Routes
Handles image uploads via Cloudinary for permanent storage
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import cloudinary
import cloudinary.uploader
import logging
import os

from services.image_storage import (
    save_image, 
    get_image, 
    delete_image, 
    get_image_url,
    generate_upload_signature
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/images", tags=["images"])

security = HTTPBearer()


async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin JWT token for upload/delete operations"""
    try:
        token = credentials.credentials
        secret_key = os.environ.get('ADMIN_SECRET_KEY')
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/cloudinary/signature")
async def get_cloudinary_signature(
    folder: str = Query("remy/questions"),
    _: str = Depends(verify_admin_token)
):
    """
    Get a signed upload signature for direct frontend uploads to Cloudinary
    This allows the frontend to upload directly to Cloudinary CDN
    """
    try:
        sig_data = generate_upload_signature(folder)
        return sig_data
    except Exception as e:
        logger.error(f"Error generating signature: {e}")
        raise HTTPException(status_code=500, detail="Error generando firma")


@router.get("/{image_id:path}")
async def serve_image(image_id: str):
    """
    Serve an image - redirects to Cloudinary CDN URL
    For old GridFS images, returns 404 (they're gone)
    For Cloudinary images, redirects to the CDN
    """
    # Build Cloudinary URL
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    
    # Check if it's a Cloudinary public_id (contains folder path)
    if "/" in image_id or image_id.startswith("remy"):
        # Cloudinary image - redirect to CDN
        url = f"https://res.cloudinary.com/{cloud_name}/image/upload/q_auto,f_auto/{image_id}"
        return RedirectResponse(url=url, status_code=302)
    
    # Old GridFS format (UUID) - these are lost, return 404
    # But first check if we have it in Cloudinary somehow
    try:
        # Try to find in Cloudinary
        result = cloudinary.api.resource(f"remy/questions/{image_id}")
        if result:
            url = result.get("secure_url")
            return RedirectResponse(url=url, status_code=302)
    except:
        pass
    
    raise HTTPException(
        status_code=404, 
        detail="Imagen no encontrada. Las imágenes antiguas ya no están disponibles."
    )


@router.post("/upload")
async def upload_image(
    image: UploadFile = File(None),
    file: UploadFile = File(None),
    folder: str = Query("remy/questions"),
    _: str = Depends(verify_admin_token)
):
    """
    Upload an image directly to Cloudinary (admin only)
    Returns permanent CDN URL
    Accepts either 'image' or 'file' field name for compatibility
    """
    # Use whichever file was provided
    upload_file = image or file
    if not upload_file:
        raise HTTPException(status_code=400, detail="No se proporcionó archivo de imagen")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if upload_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail="Tipo de archivo no permitido. Use JPG, PNG, WebP o GIF."
        )
    
    # Read file content
    content = await upload_file.read()
    
    # Validate file size (max 10MB for Cloudinary)
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 10MB.")
    
    try:
        # Upload to Cloudinary
        public_id = await save_image(
            content,
            upload_file.filename,
            upload_file.content_type,
            folder=folder
        )
        
        # Get the full URL
        url = get_image_url(public_id)
        
        return {
            "success": True,
            "image_id": public_id,
            "url": url,
            "size": len(content)
        }
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {str(e)}")


@router.delete("/{image_id:path}")
async def remove_image(
    image_id: str,
    _: str = Depends(verify_admin_token)
):
    """Delete an image from Cloudinary (admin only)"""
    success = await delete_image(image_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Imagen no encontrada o no se pudo eliminar")
    
    return {"success": True, "message": "Imagen eliminada de Cloudinary"}
