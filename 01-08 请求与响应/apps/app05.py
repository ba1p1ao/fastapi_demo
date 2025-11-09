from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import aiofiles
import os

app05 = APIRouter()


@app05.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    path = os.path.join("./images", filename)
    async with aiofiles.open(path, "wb") as f:
        content = await file.read()
        if file.size > 50 * 1024 * 1024:  # 大于50mb
            raise HTTPException(status_code=400, detail="文件太大")
        await f.write(content)

    return {"success": True, "filename": filename, "message": "上传成功"}


@app05.post("/uploadfiles")
async def upload_files(files: List[UploadFile]):
    filenames = []
    for file in files:
        filenames.append(file.filename)
        await upload_file(file)

    return {"success": True, "filenames": filenames, "message": "上传成功"}
