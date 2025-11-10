from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.asyncio import Redis
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
from datetime import datetime
from urllib.parse import unquote
import aiofiles
import os
import uuid
import redis
import asyncio
import magic
import psutil
import logging
import multiprocessing

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Image Server - Optimized")

# 限流配置
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 配置 - 支持环境变量
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Redis连接池
redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    max_connections=100,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)
r = redis.Redis(connection_pool=redis_pool)

# 异步Redis连接池
async_redis = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global async_redis
    async_redis = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
        max_connections=50,
    )
    try:
        await async_redis.ping()
        logger.info("异步Redis连接成功")
    except Exception as e:
        logger.warning(f"异步Redis连接失败: {e}")
        async_redis = None

    # 确保预览图目录存在
    Path(PREVIEW_DIR).mkdir(exist_ok=True)

    yield

    if async_redis:
        await async_redis.close()


# 检查Redis连接
try:
    r.ping()
    logger.info("Redis连接成功")
except RedisConnectionError:
    logger.warning("Redis连接失败！服务可能无法正常工作")

# 线程池配置
cpu_count = multiprocessing.cpu_count()
thread_pool = ThreadPoolExecutor(max_workers=min(cpu_count * 2, 16))

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"
THUMBNAIL_DIR = BASE_DIR / "thumbnails"
PREVIEW_DIR = BASE_DIR / "previews"  # 新增预览图目录

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]

# 并发控制
MAX_CONCURRENT_UPLOADS = int(os.getenv("MAX_CONCURRENT_UPLOADS", 30))
MAX_CONCURRENT_THUMBNAILS = int(os.getenv("MAX_CONCURRENT_THUMBNAILS", 20))
MAX_MEMORY_CHUNK = 5 * 1024 * 1024

upload_semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)
thumbnail_semaphore = asyncio.Semaphore(MAX_CONCURRENT_THUMBNAILS)

# 系统状态缓存
_system_status_cache = {}
_system_status_cache_time = None
SYSTEM_STATUS_CACHE_TTL = 2

# 确保目录存在
Path(UPLOAD_DIR).mkdir(exist_ok=True)
Path(THUMBNAIL_DIR).mkdir(exist_ok=True)
Path(STATIC_DIR).mkdir(exist_ok=True)
Path(PREVIEW_DIR).mkdir(exist_ok=True)  # 确保预览图目录存在

# 挂载静态文件
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/thumbnails", StaticFiles(directory=THUMBNAIL_DIR), name="thumbnails")
app.mount(
    "/previews", StaticFiles(directory=PREVIEW_DIR), name="previews"
)  # 挂载预览图目录


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


def validate_filename(filename: str) -> bool:
    """验证文件名是否安全，防止路径遍历攻击"""
    if not filename:
        return False

    if os.sep in filename or "/" in filename or "\\" in filename:
        return False

    if os.path.isabs(filename):
        return False

    try:
        resolved = Path(UPLOAD_DIR, filename).resolve()
        base = Path(UPLOAD_DIR).resolve()
        if not str(resolved).startswith(str(base)):
            return False
    except (ValueError, OSError):
        return False

    if len(filename) > 255:
        return False

    dangerous_chars = ["..", "\x00", "\n", "\r"]
    return not any(char in filename for char in dangerous_chars)


@app.get("/system-status")
async def system_status(use_cache: bool = True):
    global _system_status_cache, _system_status_cache_time

    now = datetime.now()
    if (
        use_cache
        and _system_status_cache_time
        and (now - _system_status_cache_time).total_seconds() < SYSTEM_STATUS_CACHE_TTL
    ):
        return _system_status_cache

    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu_percent = psutil.cpu_percent(interval=0.1)

        redis_status = False
        try:
            r.ping()
            redis_status = True
        except:
            pass

        status = {
            "memory_used_percent": memory.percent,
            "disk_used_percent": disk.percent,
            "cpu_percent": cpu_percent,
            "redis_connected": redis_status,
            "active_uploads": MAX_CONCURRENT_UPLOADS - upload_semaphore._value,
            "active_thumbnails": MAX_CONCURRENT_THUMBNAILS - thumbnail_semaphore._value,
        }

        _system_status_cache = status
        _system_status_cache_time = now
        return status
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        raise HTTPException(status_code=500, detail="获取系统状态失败")


async def is_allowed_file(file: UploadFile) -> bool:
    """检查文件类型"""
    try:
        content = await file.read(1024)
        await file.seek(0)
        mime = magic.from_buffer(content, mime=True)
        return mime in ALLOWED_MIME_TYPES
    except Exception as e:
        logger.error(f"文件类型检查失败: {e}")
        return False


@app.post("/upload")
@limiter.limit("100/minute")
async def upload_image(
    request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    # 系统负载检查
    try:
        system_info = await system_status(use_cache=True)
        if system_info["memory_used_percent"] > 90 or system_info["cpu_percent"] > 85:
            raise HTTPException(status_code=503, detail="系统资源紧张，请稍后重试")
        if system_info["active_uploads"] > MAX_CONCURRENT_UPLOADS * 0.9:
            raise HTTPException(status_code=503, detail="上传任务过多，请稍后重试")
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"系统状态检查失败: {e}")

    if not await is_allowed_file(file):
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    async with upload_semaphore:
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="不支持的文件扩展名")

        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            total_size = 0
            async with aiofiles.open(file_path, "wb") as f:
                while True:
                    chunk = await file.read(MAX_MEMORY_CHUNK)
                    if not chunk:
                        break
                    total_size += len(chunk)
                    if total_size > MAX_FILE_SIZE:
                        await f.close()
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        raise HTTPException(status_code=400, detail="文件太大")
                    await f.write(chunk)

            background_tasks.add_task(
                delayed_thumbnail_processing,
                file_path,
                filename,
                file.filename,
                total_size,
            )

            return {
                "success": True,
                "filename": filename,
                "message": "上传成功，缩略图和预览图后台生成中...",
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"上传失败: {e}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
            raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


async def delayed_thumbnail_processing(file_path, filename, original_name, size):
    """延迟处理缩略图，避免立即占用资源"""
    active_thumbnails = MAX_CONCURRENT_THUMBNAILS - thumbnail_semaphore._value
    delay_time = min(2, active_thumbnails * 0.1)
    await asyncio.sleep(delay_time)
    await process_thumbnail_and_preview(file_path, filename, original_name, size)


async def process_thumbnail_and_preview(file_path, filename, original_name, size):
    """同时生成缩略图和预览图"""
    async with thumbnail_semaphore:
        try:
            thumbnail_path = os.path.join(THUMBNAIL_DIR, f"thumb_{filename}")
            preview_path = os.path.join(PREVIEW_DIR, f"preview_{filename}")

            # 同时生成缩略图和预览图
            await asyncio.gather(
                asyncio.get_event_loop().run_in_executor(
                    thread_pool, create_thumbnail, file_path, thumbnail_path
                ),
                asyncio.get_event_loop().run_in_executor(
                    thread_pool, create_preview, file_path, preview_path
                ),
            )

            file_info = {
                "filename": filename,
                "original_name": original_name,
                "size": str(size),
                "upload_time": datetime.now().isoformat(),
            }

            # 优先使用异步Redis
            if async_redis:
                try:
                    pipe = async_redis.pipeline()
                    pipe.hset(f"image:{filename}", mapping=file_info)
                    pipe.lpush("recent_images", filename)
                    pipe.ltrim("recent_images", 0, 199)
                    await pipe.execute()
                except Exception as e:
                    logger.error(f"异步Redis操作失败 {filename}: {e}")
                    # 降级到同步Redis
                    try:
                        r.hset(f"image:{filename}", mapping=file_info)
                        r.lpush("recent_images", filename)
                        r.ltrim("recent_images", 0, 199)
                    except RedisConnectionError:
                        pass
            else:
                # 同步Redis操作
                try:
                    r.hset(f"image:{filename}", mapping=file_info)
                    r.lpush("recent_images", filename)
                    r.ltrim("recent_images", 0, 199)
                except RedisConnectionError as e:
                    logger.error(f"Redis操作失败 {filename}: {e}")

        except Exception as e:
            logger.error(f"缩略图或预览图生成失败 {filename}: {e}")


def create_thumbnail(image_path, thumbnail_path, size=(200, 150)):
    """生成缩略图"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGB模式（如果必要）
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            # 如果图片很大，先进行初步缩放
            if max(img.size) > 1000:
                img.thumbnail((size[0] * 2, size[1] * 2), Image.NEAREST)

            # 生成最终缩略图
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # 确保输出为JPEG格式
            if not thumbnail_path.lower().endswith(".jpg"):
                thumbnail_path = thumbnail_path.rsplit(".", 1)[0] + ".jpg"

            img.save(thumbnail_path, quality=70, optimize=True)
            logger.info(f"缩略图生成成功: {thumbnail_path}")

    except Exception as e:
        logger.error(f"缩略图生成失败: {e}")
        try:
            # 生成占位图
            placeholder = Image.new("RGB", size, color=(200, 200, 200))
            placeholder.save(thumbnail_path, quality=70)
            logger.info(f"生成缩略图占位图: {thumbnail_path}")
        except Exception as e2:
            logger.error(f"缩略图占位图生成也失败: {e2}")


def create_preview(image_path, preview_path, max_size=(1200, 800)):
    """生成中等质量的预览图"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGB模式（如果必要）
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            # 保持原图比例，调整大小
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # 确保输出为JPEG格式以减小文件大小
            if not preview_path.lower().endswith(".jpg"):
                preview_path = preview_path.rsplit(".", 1)[0] + ".jpg"

            # 保存为中等质量，平衡画质和文件大小
            img.save(preview_path, quality=75, optimize=True)
            logger.info(f"预览图生成成功: {preview_path}")

    except Exception as e:
        logger.error(f"预览图生成失败: {e}")
        try:
            # 尝试生成一个占位图
            placeholder = Image.new("RGB", (400, 300), color=(200, 200, 200))
            placeholder.save(preview_path, quality=70)
            logger.info(f"生成预览图占位图: {preview_path}")
        except Exception as e2:
            logger.error(f"预览图占位图生成也失败: {e2}")


@app.get("/download/{filename}")
async def download_image(filename: str):
    if not validate_filename(filename):
        raise HTTPException(status_code=400, detail="无效的文件名")

    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    try:
        r.hincrby(f"image:{filename}", "download_count", 1)
    except RedisConnectionError:
        logger.warning("Redis连接失败，无法更新下载计数")

    return FileResponse(
        file_path, filename=filename, media_type="application/octet-stream"
    )


@app.get("/images")
async def list_images(page: int = 1, per_page: int = 20, q: str = None):
    """获取图片列表，支持搜索"""
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    # 搜索功能
    if q and q.strip():
        return await search_images(q.strip(), page, per_page)

    # 列表逻辑
    start = (page - 1) * per_page
    end = start + per_page - 1

    try:
        recent_images = r.lrange("recent_images", start, end)
    except RedisConnectionError:
        logger.error("Redis连接失败，无法获取图片列表")
        return {
            "images": [],
            "page": page,
            "per_page": per_page,
            "error": "Redis连接失败",
        }

    images = []
    invalid_images = []

    for filename in recent_images:
        if not validate_filename(filename):
            invalid_images.append(filename)
            continue

        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            invalid_images.append(filename)
            continue

        try:
            file_info = r.hgetall(f"image:{filename}")
            if file_info:
                images.append(
                    {
                        "filename": filename,
                        "original_name": file_info.get("original_name", ""),
                        "size": file_info.get("size", 0),
                        "download_count": file_info.get("download_count", 0),
                        "upload_time": file_info.get("upload_time", ""),
                    }
                )
        except RedisConnectionError:
            logger.warning(f"无法获取文件信息: {filename}")

    if invalid_images:
        asyncio.create_task(cleanup_invalid_records(invalid_images))

    return {"images": images, "page": page, "per_page": per_page}


async def search_images(keyword: str, page: int = 1, per_page: int = 20):
    """根据关键词模糊搜索图片"""
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    try:
        recent_images = r.lrange("recent_images", 0, -1)
    except RedisConnectionError:
        logger.error("Redis连接失败，无法获取图片列表")
        return {
            "images": [],
            "page": page,
            "per_page": per_page,
            "error": "Redis连接失败",
        }

    images = []
    invalid_images = []
    keyword_lower = keyword.lower()

    for filename in recent_images:
        if not validate_filename(filename):
            invalid_images.append(filename)
            continue

        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            invalid_images.append(filename)
            continue

        try:
            file_info = r.hgetall(f"image:{filename}")
            if file_info:
                original_name = file_info.get("original_name", "")
                original_name_lower = original_name.lower()
                if keyword_lower in original_name_lower:
                    images.append(
                        {
                            "filename": filename,
                            "original_name": original_name,
                            "size": file_info.get("size", 0),
                            "download_count": file_info.get("download_count", 0),
                            "upload_time": file_info.get("upload_time", ""),
                        }
                    )
        except RedisConnectionError:
            logger.warning(f"无法获取文件信息: {filename}")

    # 分页处理
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = images[start:end]

    # 异步清理无效记录
    if invalid_images:
        asyncio.create_task(cleanup_invalid_records(invalid_images))

    return {
        "images": paginated_images,
        "page": page,
        "per_page": per_page,
        "total": len(images),
        "keyword": keyword,
    }


async def cleanup_invalid_records(invalid_filenames):
    """异步清理无效记录"""
    try:
        for filename in invalid_filenames:
            try:
                r.delete(f"image:{filename}")
                r.lrem("recent_images", 0, filename)

                # 同时删除缩略图和预览图
                thumbnail_path = os.path.join(THUMBNAIL_DIR, f"thumb_{filename}")
                preview_path = os.path.join(PREVIEW_DIR, f"preview_{filename}")

                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
                if os.path.exists(preview_path):
                    os.remove(preview_path)

            except RedisConnectionError:
                logger.warning(f"清理Redis记录失败: {filename}")
        logger.info(f"清理了 {len(invalid_filenames)} 个无效记录")
    except Exception as e:
        logger.error(f"清理无效记录失败: {e}")


@app.get("/thumbnail/{filename}")
async def get_thumbnail(filename: str):
    # 解码URL编码的文件名
    filename = unquote(filename)

    if not validate_filename(filename):
        raise HTTPException(status_code=400, detail="无效的文件名")

    # 生成正确的缩略图文件名（添加thumb_前缀并转换为jpg）
    name_without_ext = os.path.splitext(filename)[0]
    thumbnail_filename = f"thumb_{name_without_ext}.jpg"
    thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)

    # print(f"Looking for thumbnail: {thumbnail_path}")  # 调试日志

    if os.path.exists(thumbnail_path):
        return FileResponse(thumbnail_path)

    original_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(original_path):
        try:
            await asyncio.get_event_loop().run_in_executor(
                thread_pool, create_thumbnail, original_path, thumbnail_path
            )
            if os.path.exists(thumbnail_path):
                return FileResponse(thumbnail_path)
        except Exception as e:
            logger.error(f"创建缩略图失败: {e}")

    raise HTTPException(status_code=404, detail="缩略图不存在")


# 修改预览图获取接口
@app.get("/preview/{filename}")
async def get_preview(filename: str):
    # 解码URL编码的文件名
    filename = unquote(filename)

    if not validate_filename(filename):
        raise HTTPException(status_code=400, detail="无效的文件名")

    # 生成正确的预览图文件名（添加preview_前缀并转换为jpg）
    name_without_ext = os.path.splitext(filename)[0]
    preview_filename = f"preview_{name_without_ext}.jpg"
    preview_path = os.path.join(PREVIEW_DIR, preview_filename)

    # print(f"Looking for preview: {preview_path}")  # 调试日志

    if os.path.exists(preview_path):
        return FileResponse(preview_path)

    original_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(original_path):
        try:
            await asyncio.get_event_loop().run_in_executor(
                thread_pool, create_preview, original_path, preview_path
            )
            if os.path.exists(preview_path):
                return FileResponse(preview_path)
        except Exception as e:
            logger.error(f"创建预览图失败: {e}")

    raise HTTPException(status_code=404, detail="预览图不存在")


@app.delete("/image/{filename}")
async def delete_image(filename: str):
    if not validate_filename(filename):
        raise HTTPException(status_code=400, detail="无效的文件名")

    file_path = os.path.join(UPLOAD_DIR, filename)
    thumbnail_path = os.path.join(THUMBNAIL_DIR, f"thumb_{filename}")
    preview_path = os.path.join(PREVIEW_DIR, f"preview_{filename}")

    try:
        deleted_files = []
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_files.append("原图")
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            deleted_files.append("缩略图")
        if os.path.exists(preview_path):
            os.remove(preview_path)
            deleted_files.append("预览图")

        try:
            r.delete(f"image:{filename}")
            r.lrem("recent_images", 0, filename)
        except RedisConnectionError:
            logger.warning(f"Redis删除失败: {filename}")

        return {"success": True, "message": f"删除成功: {', '.join(deleted_files)}"}
    except Exception as e:
        logger.error(f"删除失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@app.get("/health")
async def health_check():
    redis_ok = False
    try:
        r.ping()
        redis_ok = True
    except:
        pass

    return {
        "status": "healthy" if redis_ok else "degraded",
        "service": "image_server",
        "timestamp": datetime.now().isoformat(),
        "redis_connected": redis_ok,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=min(multiprocessing.cpu_count(), 4),
        loop="asyncio",
        limit_max_requests=1000,
        timeout_keep_alive=5,
        reload=True,
    )
