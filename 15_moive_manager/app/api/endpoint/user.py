from pathlib import Path
import uuid
import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from tortoise.expressions import Q
from models.user import User
from schemas.user import UserUpdate, UserOut, UserUpdatedOut
from core import deps, auth
import os
import magic

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def getMe(current_user: User = Depends(deps.get_current_user)):
    # print("me endpoint accessed")
    return current_user


@router.put("/me", response_model=UserUpdatedOut)
async def updateMe(
    user_data: UserUpdate, current_user: User = Depends(deps.get_current_user)
):
    if user_data.current_password is None:
        raise HTTPException(status_code=400, detail="当前密码不能为空")

    if user_data.username != current_user.username:
        # 检查新的用户名是否已存在
        existing_user = await User.get_or_none(username=user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")

    if user_data.email != current_user.email:
        # 检查新的邮箱是否已存在
        existing_user = await User.get_or_none(email=user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已存在")

    # 判断当前密码是否正确
    if auth.verify_password(user_data.current_password, current_user.password_hash):
        update_data = user_data.model_dump(
            exclude_unset=True, exclude={"current_password"}
        )
        print(update_data)
        if "new_password" in update_data:
            new_password_hash = auth.get_password_hash(update_data.pop("new_password"))
            update_data["password_hash"] = new_password_hash

        updated_user: User = await current_user.update_from_dict(update_data).save()
        if updated_user is None:
            updated_user = current_user

        # 生成新的 token
        token = auth.create_access_token(data={"sub": updated_user.username})
        response_data = {"updatedUser": updated_user, "token": token}

        return response_data

    else:
        raise HTTPException(status_code=400, detail="当前密码错误")


MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
UPLOAD_DIR = "static/user_avatar_imgs"


async def is_allowed_file(file: UploadFile) -> bool:
    """检查文件类型"""
    mime = magic.Magic(mime=True)
    file_content = await file.read(2048)  # 读取前2048字节进行检测
    await file.seek(0)  # 重置文件指针位置
    file_mime_type = mime.from_buffer(file_content)
    return file_mime_type in ALLOWED_MIME_TYPES


@router.post("/me/avatar")
async def updateAvatar(
    avatar: UploadFile = File(...), current_user: User = Depends(deps.get_current_user)
):
    if not await is_allowed_file(avatar):
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    file_extension = Path(avatar.filename).suffix.lower()
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件扩展名")

    filename = f"{uuid.uuid4()}_{avatar.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        total_size = 0
        while True:
            chunk = await avatar.read(1024 * 1024)  # 每次读取1MB
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="文件大小超过限制")
            await out_file.write(chunk)
    # 更新用户头像URL
    current_user.avatar_url = f"/static/user_avatar_imgs/{filename}"
    await current_user.save()
    return {"avatar_url": current_user.avatar_url}
