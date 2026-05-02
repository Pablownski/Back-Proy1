import os
import uuid
from fastapi import UploadFile, HTTPException

MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


async def save_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail={"error": "Only JPG and PNG images are allowed"},
        )

    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={"error": "File extension must be jpg or png"},
        )

    content = await file.read()

    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail={"error": "Image size must not exceed 1 MB"},
        )

    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as f:
        f.write(content)

    return f"/uploads/{filename}"
