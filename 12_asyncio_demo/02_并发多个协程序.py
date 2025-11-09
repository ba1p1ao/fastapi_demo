from utils import async_timed
import asyncio


async def buy(name, time):
    await asyncio.sleep(time)
    if name == "aa":
        raise ValueError(f"Error occurred for {name}")
    print(f"hello : {name}")
    return f"{name} completed"


##### gather()


# @async_timed
# async def main():
#     try:

#         results = await asyncio.gather(
#             buy("aa", 1),
#             buy("bb", 2),
#             buy("cc", 3),
#             buy("dd", 3),
#             buy("aa", 1),
#         )
#     except ValueError as e:
#         print(e)
#     # gather 列表中存在有异常的协程，整个gather都会停止
#     # 所以需要获取全部的协程，重新await
#     try:
#         tasks = asyncio.all_tasks()
#         for task in tasks:
#             # 判断主协程不能await自己, 主协程也就是第一个task 所以名字就是 Task-1， 或者通过get_core().__name__ == 函数名
#             # 如果是直接contnue
#             if task.get_name() == "Task-1" or task.get_coro().__name__ == "main":
#                 continue
#             result = await task
#             print(result, task.get_name())
#     except ValueError as e:
#         print(e)

# # 以上方法存在缺陷，如果两个任务同时报错，只会显示第一个，所以不可取

# # 以下方法均可采用

# @async_timed
# async def main_return_exceptions():
#     # 方案1：使用 return_exceptions=True 处理异常
#     print("=== 方案1：使用 return_exceptions=True ===")
#     try:
#         results = await asyncio.gather(
#             buy("aa", 1),
#             buy("bb", 2),
#             buy("cc", 3),
#             buy("dd", 3),
#             buy("aa", 1),
#             return_exceptions=True  # 不抛出异常，而是作为结果返回
#         )

#         # 处理结果和异常
#         for i, result in enumerate(results):
#             if isinstance(result, Exception):
#                 print(f"Task {i} failed: {result}")
#             else:
#                 print(f"Task {i} succeeded: {result}")

#     except Exception as e:
#         print(f"Unexpected error: {e}")


# @async_timed
# async def main_alternative():
#     # 方案2：分别创建和管理任务
#     print("\n=== 方案2：分别创建任务 ===")
#     tasks = [
#         asyncio.create_task(buy("aa", 1), name="buy_aa_1"),
#         asyncio.create_task(buy("bb", 2), name="buy_bb_2"),
#         asyncio.create_task(buy("cc", 3), name="buy_cc_3"),
#         asyncio.create_task(buy("dd", 3), name="buy_dd_3"),
#         asyncio.create_task(buy("aa", 1), name="buy_aa_4"),
#     ]

#     # 分别等待每个任务完成，单独处理异常
#     for i, task in enumerate(tasks):
#         try:
#             result = await task
#             print(f"Task {i} ({task.get_name()}) succeeded: {result}")
#         except Exception as e:
#             print(f"Task {i} ({task.get_name()}) failed: {e}")


# async def main_best_practice():
#     # 最佳实践：结合多种方法
#     print("\n=== 最佳实践方案 ===")

#     # 创建任务时指定名称
#     tasks = {
#         asyncio.create_task(buy("aa", 1), name="buy_aa_1"): "aa_1",
#         asyncio.create_task(buy("bb", 2), name="buy_bb_2"): "bb_2",
#         asyncio.create_task(buy("cc", 3), name="buy_cc_3"): "cc_3",
#         asyncio.create_task(buy("dd", 3), name="buy_dd_3"): "dd_3",
#         asyncio.create_task(buy("aa", 1), name="buy_ee_4"): "ee_4",
#     }

#     # 使用 asyncio.wait 等待所有任务完成
#     done, pending = await asyncio.wait(
#         tasks.keys(),
#         return_when=asyncio.ALL_COMPLETED
#     )

#     # 处理完成的任务
#     for task in done:
#         task_name = tasks[task]
#         if task.cancelled():
#             print(f"Task {task_name} was cancelled")
#         elif task.exception():
#             print(f"Task {task_name} failed with: {task.exception()}")
#         else:
#             print(f"Task {task_name} succeeded with: {task.result()}")


#### 使用as_completed


# @async_timed
# async def main():
#     try:
#         # aws = [
#         #     buy("张三", 1),
#         #     buy("李四", 3),
#         # ]

#         # #可以指定超时时间
#         # #如果超过指定的超时时间，还有任务没有完成，那么会抛出TimeoutError异常
#         # #剩余的任务不会被取消
#         # for coro in asyncio.as_completed(aws, timeout=2):
#         #     result = await coro
#         #     print(result)
#         # as_completed 方法在其中某个任务抛出异常后，剩余的任务也不会被取消掉
#         aws = [
#             buy("aa", 1),
#             buy("李四", 3),
#         ]
#         for coro in asyncio.as_completed(aws):
#             result = await coro
#             print(result)
#     except Exception as e:
#         print(e)

#     try:
#         tasks = asyncio.all_tasks()
#         for task in tasks:
#             print(task.get_name(), task.cancelled())
#             if task.get_name() == "Task-1":
#                 continue
#             result = await task
#             print(result)
#     except Exception as e:
#         print(e)





if __name__ == "__main__":

    ####### gather ############## 
    # asyncio.run(main()) # 有问题

    # # # 运行各种方案
    # asyncio.run(main_return_exceptions()) # 没问题 , 最简单
    # asyncio.run(main_alternative()) # 没问题
    # asyncio.run(main_best_practice()) # 没问题


    ####### as_completed() #############
    # asyncio.run(main())


    ####### wait_for / wait ###############
    pass