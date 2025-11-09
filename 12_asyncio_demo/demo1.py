"""

******************************************************
**https://www.runoob.com/python3/python-asyncio.html**
******************************************************


Python asyncio 模块
asyncio 是 Python 标准库中的一个模块，用于编写异步 I/O 操作的代码。

asyncio 提供了一种高效的方式来处理并发任务，特别适用于 I/O 密集型操作，如网络请求、文件读写等。

通过使用 asyncio，你可以在单线程中同时处理多个任务，而无需使用多线程或多进程。

为什么需要 asyncio？
在传统的同步编程中，当一个任务需要等待 I/O 操作（如网络请求）完成时，程序会阻塞，直到操作完成。这会导致程序的效率低下，尤其是在需要处理大量 I/O 操作时。

asyncio 通过引入异步编程模型，允许程序在等待 I/O 操作时继续执行其他任务，从而提高了程序的并发性和效率。

"""

import asyncio
import time

"""
asyncio 的核心概念
1. 协程（Coroutine）
    协程是 asyncio 的核心概念之一。
    它是一个特殊的函数，可以在执行过程中暂停，并在稍后恢复执行。
    协程通过 async def 关键字定义，并通过 await 关键字暂停执行，等待异步操作完成。

"""


async def say_hello(id=12):
    print(f"hello {id}")
    await asyncio.sleep(1)
    print("id", id)


"""
2. 事件循环（Event Loop）
    事件循环是 asyncio 的核心组件，负责调度和执行协程。
    它不断地检查是否有任务需要执行，并在任务完成后调用相应的回调函数。
"""


async def main1():
    await say_hello()


"""
3. 任务（Task）
    任务是对协程的封装，表示一个正在执行或将要执行的协程。
    你可以通过 asyncio.create_task() 函数创建任务，并将其添加到事件循环中。
"""


async def main2():
    task = asyncio.create_task(say_hello())
    await task


"""
4. Future
    Future 是一个表示异步操作结果的对象。
    它通常用于底层 API，表示一个尚未完成的操作。你可以通过 await 关键字等待 Future 完成。
"""


async def main3():
    future = asyncio.Future()
    await future


if __name__ == "__main__":
    asyncio.run(main3())
