from pathlib import Path
import os
# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
FILE_ROOT_DIR = BASE_DIR / "uploads"

# 查看文件是排序用到的字典序列
SORT_DICT = {
    "name": "name",
    "size": "size",
    "modified": "modified_time",
}

# 并发控制
MAX_CONCURRENT_UPLOADS = int(os.getenv("MAX_CONCURRENT_UPLOADS", 30))

MIME_TYPES = {
    # 文本文件
    '.txt': 'text/plain',
    '.sql': 'text/plain',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.xml': 'application/xml',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.md': 'text/markdown',
    '.yaml': 'application/x-yaml',
    '.yml': 'application/x-yaml',
    
    # 图像文件
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    
    # 音频文件
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.aac': 'audio/aac',
    '.flac': 'audio/flac',
    '.m4a': 'audio/mp4',
    
    # 视频文件
    '.mp4': 'video/mp4',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    '.webm': 'video/webm',
    '.mkv': 'video/x-matroska',
    '.flv': 'video/x-flv',
    '.wmv': 'video/x-ms-wmv',
    
    # 文档文件
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.odt': 'application/vnd.oasis.opendocument.text',
    '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
    
    # 压缩文件
    '.zip': 'application/zip',
    '.rar': 'application/x-rar-compressed',
    '.7z': 'application/x-7z-compressed',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    
    # 配置文件
    '.conf': 'text/plain',
    '.ini': 'text/plain',
    '.properties': 'text/plain',
    '.cfg': 'text/plain',
    '.config': 'text/plain',
    
    # 其他文件
    '.exe': 'application/x-msdownload',
    '.dmg': 'application/x-apple-diskimage',
    '.iso': 'application/x-iso9660-image',
    '.bin': 'application/octet-stream',
    '.dat': 'application/octet-stream',
    '.torrent': 'application/x-bittorrent',
    
    # 默认类型
    'default': 'application/octet-stream'
}