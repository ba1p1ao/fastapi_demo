"""
asyncio 的基本用法
"""

"""
1. 运行协程
要运行一个协程，你可以使用 asyncio.run() 函数。它会创建一个事件循环，并运行指定的协程。

"""
import asyncio


async def main1():
    print("Start")
    await asyncio.sleep(1)
    print("End")


"""
2. 并发执行多个任务
你可以使用 asyncio.gather() 函数并发执行多个协程，并等待它们全部完成。
"""


async def task1():
    print("Task 1 started")
    await asyncio.sleep(1)
    print("Task 1 finished")


async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 finished")


async def main2():
    # asyncio.gather() 函数并发执行多个协程，并等待它们全部完成。
    tasks = asyncio.gather(task1(), task2())
    await tasks


"""
3. 超时控制
你可以使用 asyncio.wait_for() 函数为协程设置超时时间。
如果协程在指定时间内未完成，将引发 asyncio.TimeoutError 异常。
"""


async def wait():
    print("task start")
    for i in range(5):
        print(f"wait...{i+1}")
        await asyncio.sleep(1)
    print("task finished")


async def main3():
    try:
        await asyncio.wait_for(wait(), timeout=3)
    except asyncio.TimeoutError:
        print("Task timed out")


if __name__ == "__main__":
    asyncio.run(main3())



"""
asyncio 的应用场景
asyncio 特别适用于以下场景：

    网络请求：如 HTTP 请求、WebSocket 通信等。
    文件 I/O：如异步读写文件。
    数据库操作：如异步访问数据库。
    实时数据处理：如实时消息队列处理。
"""

