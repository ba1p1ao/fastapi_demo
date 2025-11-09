"""
常用类、方法和函数
1. 核心函数
方法/函数	                  说明	                                    示例
asyncio.run(coro)	        运行异步主函数（Python 3.7+）	    asyncio.run(main())
asyncio.create_task(coro)	创建任务并加入事件循环	             task = asyncio.create_task(fetch_data())
asyncio.gather(*coros)	    并发运行多个协程	                await asyncio.gather(task1, task2)
asyncio.sleep(delay)	    异步等待（非阻塞）	                await asyncio.sleep(1)
asyncio.wait(coros)	        控制任务完成方式	                done, pending = await asyncio.wait([task1, task2])

2. 事件循环（Event Loop）
方法	说明	示例
loop.run_until_complete(future)	        运行直到任务完成	     loop.run_until_complete(main())
loop.run_forever()	                    永久运行事件循环	     loop.run_forever()
loop.stop()	                            停止事件循环	        loop.stop()
loop.close()	                        关闭事件循环	        loop.close()
loop.call_soon(callback)                安排回调函数立即执行	 loop.call_soon(print, "Hello")
loop.call_later(delay, callback)	    延迟执行回调	        loop.call_later(5, callback)

3. 协程（Coroutine）与任务（Task）
方法/装饰器	说明	示例
@asyncio.coroutine	            协程装饰器（旧版，Python 3.4-3.7）	    @asyncio.coroutine
                                                                     def old_coro():
async def	                    定义协程（Python 3.5+）	                async def fetch():
task.cancel()	                取消任务	                           task.cancel()
task.done()	                    检查任务是否完成	                    if task.done():
task.result()	                获取任务结果（需任务完成）	              data = task.result()


4. 同步原语（类似threading）
类	说明	示例
asyncio.Lock()	        异步互斥锁	lock = asyncio.Lock()
                                  async with lock:
asyncio.Event()	        事件通知	event = asyncio.Event()
                                   await event.wait()
asyncio.Queue()	        异步队列	queue = asyncio.Queue()
                                   await queue.put(item)
asyncio.Semaphore()	    信号量	    sem = asyncio.Semaphore(5)
                                   async with sem:


5. 网络与子进程
方法/类	                            说明	                        示例
asyncio.open_connection()	        建立TCP连接	        reader, writer = await asyncio.open_connection('host', 80)
asyncio.start_server()	            创建TCP服务器	    server = await asyncio.start_server(handle, '0.0.0.0', 8888)
asyncio.create_subprocess_exec()	创建子进程	        proc = await asyncio.create_subprocess_exec('ls')


6. 实用工具
方法	                        说明	            示例
asyncio.current_task()	        获取当前任务	    task = asyncio.current_task()
asyncio.all_tasks()	            获取所有任务	    tasks = asyncio.all_tasks()
asyncio.shield(coro)	        保护任务不被取消	await asyncio.shield(critical_task)
asyncio.wait_for(coro, timeout)	带超时的等待	    try: await asyncio.wait_for(task, 5)

"""

import asyncio


# 实例
# 1. 基本协程示例
async def say_hello():
    print("task start")
    for i in range(2):
        print(f"{i + 1}s...")
        await asyncio.sleep(1)
    print("task end")


async def main1():
    await asyncio.create_task(say_hello())


# if __name__ == "__main__":
#     asyncio.run(main1())


# 2. 并发执行任务


async def task1():
    print("task1 start")
    for i in range(2):
        print(f"{i + 1}s...")
        await asyncio.sleep(1)
    print("task1 end")


async def task2():
    print("task2 start")
    for i in range(2):
        print(f"{i + 1}s...")
        await asyncio.sleep(1)
    print("task2 end")


async def main2():
    tasks = await asyncio.gather(task1(), task2())
    print(tasks)


# if __name__ == "__main__":
#     asyncio.run(main2())




# 3. 使用异步队列
import random
async def producer(queue: asyncio.Queue):
    for i in range(50):
        await queue.put(i)
        print(f"queue.put: {i}")
        await asyncio.sleep(0.1)


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        print(f'consumer: {item}')
        await asyncio.sleep(0)
        queue.task_done()


async def main3():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

if __name__ == "__main__":
    asyncio.run(main3())