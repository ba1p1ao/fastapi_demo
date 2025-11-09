from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
from tortoise.expressions import Q
from models.models import Files, Users
from schemas.file import FileResponseSchemas, FileUpdate, FileUpload, DirCreate
from core import deps
from config import SORT_DICT, FILE_ROOT_DIR, MIME_TYPES, MAX_CONCURRENT_UPLOADS
from pathlib import Path
import asyncio
import math
import aiofiles
import aiofiles.os
from concurrent.futures import ThreadPoolExecutor
import os


router = APIRouter()

# 创建线程池用于处理阻塞IO操作
io_executor = ThreadPoolExecutor(max_workers=min(32, (os.cpu_count() or 1) + 4))

# 全局信号量限制并发上传数量
upload_semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)

# 文件操作锁，避免同一目录下的文件冲突
file_locks = {}
def get_file_lock(file_path: str):
    """获取文件路径对应的锁，避免同一目录下的操作冲突"""
    if file_path not in file_locks:
        file_locks[file_path] = asyncio.Lock()
    return file_locks[file_path]

def is_safe_path(path: Path) -> bool:
    """检查路径是否安全（在 UPLOADS_DIR 内）"""
    try:
        path.resolve().relative_to(FILE_ROOT_DIR.resolve())
        return True
    except ValueError:
        return False


def build_query_conditions(q: str, path: str, currnet_path_file_id: int) -> Q:
    """构建查询条件"""
    if q:
        if path == "/":
            return Q(name__icontains=q)
        else:
            return Q(path__istartswith=path, name__icontains=q)
    else:
        return Q(parent_id=currnet_path_file_id)


@router.get("/", response_model=FileResponseSchemas)
async def getAllFiles(
    path: str = "/",
    q: str = "",
    page: int = 1,
    page_size: int = 20,
    sort: str = "name",
    order: str = "asc",
):
    skip = (page - 1) * page_size
    order_prefix = "" if order == "asc" else "-"

    file = await Files.get_or_none(path=path).values("id")
    currnet_path_file_id = file["id"]

    # 使用函数构建查询
    query_conditions: Q = build_query_conditions(q, path, currnet_path_file_id)

    files = (
        await Files.filter(query_conditions)
        .order_by(f"{order_prefix}{SORT_DICT[sort]}")
        .offset(skip)
        .limit(page_size)
    )
    # print(files)

    response_data = {
        "files": files,
        "path": path,
        "total": len(files),
        "page": page,
        "pages": math.ceil(len(files) / page_size),
    }

    return response_data



# 生成唯一的文件名，避免重名冲突
async def get_unique_filename(directory_path: str, filename: str) -> str:
    """
    生成唯一的文件名，避免重名冲突
    """
    path = Path(filename)
    name = path.stem
    extension = path.suffix

    # 检查是否已存在同名文件
    existing_file = await Files.get_or_none(
        path=f"{directory_path.rstrip('/')}/{filename}", is_directory=False
    )

    if not existing_file:
        return filename

    # 如果存在，添加序号
    counter = 1
    while True:
        new_filename = f"{name} ({counter}){extension}"
        existing_file = await Files.get_or_none(
            path=f"{directory_path.rstrip('/')}/{new_filename}", is_directory=False
        )
        if not existing_file:
            return new_filename
        counter += 1


def sync_file_exists(file_path: str) -> bool:
    """同步方式检查文件是否存在（在线程池中运行）"""
    return os.path.exists(file_path)


def sync_mkdir(path: str):
    """同步方式创建目录（在线程池中运行）"""
    os.makedirs(path, exist_ok=True)


def sync_remove_file(file_path: str):
    """同步方式删除文件（在线程池中运行）"""
    if os.path.exists(file_path):
        os.remove(file_path)


def sync_rename_file(old_path: str, new_path: str):
    """同步方式重命名文件（在线程池中运行）"""
    if os.path.exists(old_path):
        os.rename(old_path, new_path)


def sync_remove_directory(dir_path: str):
    """同步方式删除目录（在线程池中运行）"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        os.rmdir(dir_path)


def sync_create_directory(dir_path: str):
    """同步方式创建目录（在线程池中运行）"""
    os.makedirs(dir_path, exist_ok=True)


def sync_list_directory(dir_path: str):
    """同步方式列出目录内容（在线程池中运行）"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        return os.listdir(dir_path)
    return []


@router.post("/upload")
async def uploadFile(
    file: UploadFile = File(...),
    path: str = Form("/"),
    current_user: Users = Depends(deps.get_current_user),
):
    """
    上传文件到指定目录 - 优化并发性能版本
    """
    try:
        # 验证文件基本信息
        if not file.filename or file.filename.strip() == "":
            raise HTTPException(status_code=400, detail="文件名不能为空")

        # 获取父目录信息
        parent_file = await Files.get_or_none(path=path)
        if not parent_file:
            raise HTTPException(status_code=404, detail="目标目录不存在")

        # 准备文件信息
        file_extension = Path(file.filename).suffix.lower()
        safe_filename = await get_unique_filename(path, file.filename)

        file_data = {
            "name": safe_filename,
            "path": f"{path.rstrip('/')}/{safe_filename}",
            "mime_type": MIME_TYPES.get(file_extension, "application/octet-stream"),
            "is_directory": False,
            "owner_id": current_user.id,
            "parent_id": parent_file.id,
            "size": 0,  # 初始大小为0，上传完成后更新
        }
        
        # 使用信号量限制并发上传数量
        async with upload_semaphore:
            # 构建本地存储路径
            local_file_path = FILE_ROOT_DIR / file_data["path"].lstrip("/")
            local_file_path_str = str(local_file_path)

            # 安全路径验证
            if not is_safe_path(local_file_path):
                raise HTTPException(status_code=400, detail="文件路径不安全")

            # 获取目录锁，避免同一目录下的文件操作冲突
            directory_lock = get_file_lock(str(local_file_path.parent))
            async with directory_lock:
                # 在线程池中确保目录存在
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(io_executor, sync_mkdir, str(local_file_path.parent))

                # 在线程池中检查文件是否已存在
                file_exists = await loop.run_in_executor(
                    io_executor, sync_file_exists, local_file_path_str
                )
                if file_exists:
                    raise HTTPException(status_code=409, detail="文件已存在")

                # 分块写入文件并计算大小 - 优化块大小
                total_size = 0
                try:
                    async with aiofiles.open(local_file_path_str, "wb") as f:
                        while True:
                            # 使用更小的块大小，减少内存占用，提高并发性能
                            chunk = await file.read(64 * 1024)  # 64KB chunks
                            if not chunk:
                                break
                            total_size += len(chunk)
                            await f.write(chunk)

                except Exception as e:
                    # 如果上传过程中出错，删除部分文件
                    if await loop.run_in_executor(io_executor, sync_file_exists, local_file_path_str):
                        await loop.run_in_executor(io_executor, sync_remove_file, local_file_path_str)
                    raise HTTPException(status_code=500, detail=f"文件写入失败: {str(e)}")

            # 更新文件大小
            file_data["size"] = total_size

            # 创建数据库记录
            try:
                new_file = await Files.create(**file_data)
            except Exception as e:
                # 如果数据库操作失败，删除已上传的文件
                if await loop.run_in_executor(io_executor, sync_file_exists, local_file_path_str):
                    await loop.run_in_executor(io_executor, sync_remove_file, local_file_path_str)
                raise HTTPException(
                    status_code=500, detail=f"文件记录创建失败: {str(e)}"
                )

        return {
            "message": "文件上传成功",
            "file": {
                "id": new_file.id,
                "name": new_file.name,
                "path": new_file.path,
                "size": new_file.size,
                "mime_type": new_file.mime_type,
            },
        }

    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except asyncio.CancelledError:
        # 处理任务取消的情况
        raise HTTPException(status_code=499, detail="客户端关闭连接")
    except Exception as e:
        # 捕获其他未知异常
        raise HTTPException(
            status_code=500, detail=f"文件上传过程中发生未知错误: {str(e)}"
        )


async def createDir(path):
    local_dir_path = FILE_ROOT_DIR / str(path).lstrip("/")
    local_dir_path_str = str(local_dir_path)
    
    # 验证路径安全性
    if not is_safe_path(local_dir_path):
        raise HTTPException(status_code=400, detail="路径不安全")

    # 在线程池中检查目录是否存在
    loop = asyncio.get_event_loop()
    dir_exists = await loop.run_in_executor(io_executor, sync_file_exists, local_dir_path_str)
    if dir_exists:
        raise HTTPException(status_code=404, detail="文件夹已经存在")

    print(local_dir_path)
    # 在线程池中创建目录
    await loop.run_in_executor(io_executor, sync_create_directory, local_dir_path_str)


@router.post("/dir")
async def addDri(data: DirCreate, current_user: Users = Depends(deps.get_current_user)):

    file = await Files.get_or_none(is_directory=True, name=data.dirname, path=data.path)
    if file:
        raise HTTPException(status_code=400, detail="文件夹已存在")
    
    print(data.dirname, data.path)
    file = await Files.get_or_none(path=data.path)
    if file.owner_id != current_user.id:
        if file.path not in ["/", "/用户文件"]:
            raise HTTPException(status_code=400, detail="权限不足，创建失败")

    file_data = {
        "name": data.dirname,
        "path": f"{data.path.rstrip('/')}/{data.dirname}",
        "is_directory": True,
        "owner_id": current_user.id,
        "parent_id": file.id,
        "size": 0,  # 初始大小为0，上传完成后更新
    }
    file = await Files.create(**file_data)

    await createDir(file_data["path"])
    return {"msg": "success"}


async def renameFile(old_path: str, new_path: str):
    print(FILE_ROOT_DIR)
    print(old_path, new_path)
    old_path = FILE_ROOT_DIR / str(old_path).lstrip("/")
    new_path = FILE_ROOT_DIR / str(new_path).lstrip("/")
    old_path_str = str(old_path)
    new_path_str = str(new_path)
    
    print(old_path, new_path)
    # 验证路径安全性
    if not is_safe_path(old_path) or not is_safe_path(new_path):
        raise HTTPException(status_code=400, detail="路径不安全")

    # 在线程池中检查文件是否存在
    loop = asyncio.get_event_loop()
    file_exists = await loop.run_in_executor(io_executor, sync_file_exists, old_path_str)
    if not file_exists:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 在线程池中重命名文件
    await loop.run_in_executor(io_executor, sync_rename_file, old_path_str, new_path_str)


@router.put("/{file_id}")
async def updateFile(
    file_id: int, data: FileUpdate, current_user: Users = Depends(deps.get_current_user)
):
    # 验证文件基本信息
    if not data.name or data.name.strip() == "":
        raise HTTPException(status_code=400, detail="文件名不能为空")

    file = await Files.get_or_none(id=file_id)
    if not file:
        raise HTTPException(status_code=400, detail="文件不存在")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有该权限")

    file_extension = Path(file.name).suffix.lower()
    new_file_name = f"{data.name}{file_extension}"

    new_path = Path(file.path).parent / new_file_name

    await renameFile(file.path, new_path)
    print(file_extension, new_file_name, new_path)
    file.name = new_file_name
    file.path = new_path

    file = await file.save()
    return {"msg": "success"}


async def removeFile(path: Path):
    path_str = str(path)
    
    # 验证路径安全性
    if not is_safe_path(path):
        raise HTTPException(status_code=400, detail="路径不安全")

    # 在线程池中检查文件是否存在
    loop = asyncio.get_event_loop()
    file_exists = await loop.run_in_executor(io_executor, sync_file_exists, path_str)
    if not file_exists:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 在线程池中检查是否为目录
    is_dir = await loop.run_in_executor(io_executor, os.path.isdir, path_str)
    if is_dir:
        # 在线程池中列出目录内容
        files = await loop.run_in_executor(io_executor, sync_list_directory, path_str)
        if files:
            raise HTTPException(status_code=400, detail="该目录不为空，不能删除")
        else:
            # 在线程池中删除目录
            await loop.run_in_executor(io_executor, sync_remove_directory, path_str)
    else:
        # 在线程池中删除文件
        await loop.run_in_executor(io_executor, sync_remove_file, path_str)


@router.delete("/{file_id}")
async def deleteFile(
    file_id: int, current_user: Users = Depends(deps.get_current_user)
):
    file = await Files.get_or_none(id=file_id)
    if not file:
        raise HTTPException(status_code=400, detail="文件不存在")

    if not current_user.is_admin and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限")

    local_file_path = FILE_ROOT_DIR / str(file.path).lstrip("/")
    print(local_file_path)

    is_deleted = await file.delete()

    await removeFile(local_file_path)

    return is_deleted


@router.get("/{file_id}/download")
async def downloadFile(file_id: int):
    file = await Files.get_or_none(id=file_id)
    if not file:
        raise HTTPException(status_code=400, detail="文件不存在")

    local_file_path = FILE_ROOT_DIR / str(file.path).lstrip("/")
    local_file_path_str = str(local_file_path)
    
    print(local_file_path)
    
    # 在线程池中检查文件是否存在
    loop = asyncio.get_event_loop()
    file_exists = await loop.run_in_executor(io_executor, sync_file_exists, local_file_path_str)
    if not file_exists:
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        local_file_path_str, filename=file.name, media_type="application/octet-stream"
    )