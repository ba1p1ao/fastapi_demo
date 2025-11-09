import asyncio
from functools import partial
from utils import async_timed

# # 1. exception()
# async def task_error(name):
#     await asyncio.sleep(1)
#     raise ValueError(f"{name} 报错")

# @async_timed
# async def main1():
#     task = asyncio.create_task(task_error("aa"))
#     await asyncio.sleep(2)
#     # 如果协程没有异常，调用exception会报错
#     print(task.exception())


# 2. add_done_callback()

# async def eat(name, time):
#     await asyncio.sleep(time)
#     print(f"{name} eat")
#     return f"{name} success"

# def my_callback(future, name):
#     print(type(future))
#     print(name, future.result())

# @async_timed
# async def main2():
#     task = asyncio.create_task(eat("aa", 2), name='AA')
#     #partial:偏函数。作用是可以将这个函数提前准好一些参数
#     # task.add_done_callback(my_callback, name=task.get_name())
#     task.add_done_callback(partial(my_callback, name=task.get_name()))
#     await task
#     print(task)



# 3. cancell 取消任务
async def eat(name, time):
    await asyncio.sleep(time)
    # print(f"{name} end")
    return f"{name} success"

@async_timed
async def main3():
    task = asyncio.create_task(eat("aa", 1))

    await asyncio.sleep(2)
    task.cancel()
    try:
        await task
    except asyncio.exceptions.CancelledError as e:
        print(e)
        print(task.cancelled())
  

if __name__ == "__main__":
    # asyncio.run(main1())
    # asyncio.run(main2())
    asyncio.run(main3())