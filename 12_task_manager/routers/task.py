from fastapi import APIRouter, HTTPException
from schemas.task import TaskCreate
from fastapi.responses import Response
from backend.models import Task as dbTask
from datetime import datetime

task = APIRouter()


@task.get("")
async def getAllTask():
    """获取全部的task信息"""
    tasks = await dbTask.all()
    return tasks


@task.get("/{task_id}")
async def getOneTask(task_id: int):
    """获取ID为task_id的task数据信息"""
    task_one = await dbTask.get(id=task_id)
    if not task_one:
        raise HTTPException(status_code=404, detail=f"task_id {task_id} not find")
    return task_one


@task.post("")
async def addTask(task_create: TaskCreate):
    """添加task信息"""
    create_time = datetime.now()
    task = await dbTask.create(
        title=task_create.title,
        description=task_create.description,
        is_completed=False,
        created_at=create_time,
        updated_at=create_time,
    )

    return task


@task.put("/{task_id}")
async def updateTask(task_id: int, task_update: TaskCreate):
    """更新task"""

    task = await dbTask.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task_id {task_id} not find")
    update_time = datetime.now()
    task = await dbTask.filter(id=task_id).update(
        is_completed=task_update.is_completed,
        updated_at=update_time
    )
    return task


@task.delete("/{task_id}")
async def deleteTask(task_id: int):
    print("delete", task_id)

    task_one = await dbTask.filter(id=task_id).delete()
    if not task_one:
        raise HTTPException(status_code=404, detail=f"task_id {task_id} not find")

    return {"msg": "deleteTask", "data": task_one}
