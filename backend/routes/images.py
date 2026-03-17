"""
Image API Routes
Serves images from MongoDB GridFS storage
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import logging
import os

from services.image_storage import save_image, get_image, delete_image, get_image_url

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


@router.get("/{image_id}")
async def serve_image(image_id: str):
    """
    Serve an image from MongoDB GridFS (public access)
    This endpoint is public so images can be displayed in the app
    """
    image_data = await get_image(image_id)
    
    if not image_data:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return Response(
        content=image_data["content"],
        media_type=image_data["content_type"],
        headers={
            "Cache-Control": "public, max-age=31536000",  # Cache for 1 year
            "Content-Disposition": f"inline; filename={image_data['filename']}"
        }
    )


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """
    Upload an image to MongoDB GridFS (admin only)
    """
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail="Tipo de archivo no permitido. Use JPG, PNG, WebP o GIF."
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size (max 5MB)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 5MB.")
    
    # Save to GridFS
    image_id = await save_image(
        content,
        file.filename,
        file.content_type,
        metadata={"source": "admin_upload"}
    )
    
    return {
        "success": True,
        "image_id": image_id,
        "url": get_image_url(image_id),
        "size": len(content)
    }


@router.delete("/{image_id}")
async def remove_image(
    image_id: str,
    _: str = Depends(verify_admin_token)
):
    """Delete an image from GridFS (admin only)"""
    success = await delete_image(image_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return {"success": True, "message": "Imagen eliminada"}
