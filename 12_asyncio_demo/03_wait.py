from utils import async_timed
import asyncio

async def eat(name, time):
    await asyncio.sleep(time)
    return f"{name} completed"



################# wait_for / wait ######################
# 1. wait _for(aw, timeout)函数 
# 函数只能用于等待一个协程或者任务，可以指定超时时间，wait for
# 1.wait _for
@async_timed
async def main1():
    # 1.wait _for
    try:
        # 如果这个协程超时了，那么就没法继续运行了
        result = await asyncio.wait_for(eat("aa", 2), timeout=1)
        print(result)
    except Exception as e:
        print(e, "timeout")
        print(asyncio.all_tasks())


# 2.wait(aws, timeout=None, return when=ALL COMPLETED)
# 函数这个函数可用于等待多个 Task 或 Future 对象，并且可以指定在什么情况下才会返回，
# 默认是ALL_COMPLETED ，并且注意，这个函数并不会触发 TimeoutError ，
# 而是将执行完的，以及超时的通过元组的形式返回。示例代码如下:

# 2.wait 
@async_timed
async def main2():
    task_list = [
        asyncio.create_task(eat("aa", 1)),
        asyncio.create_task(eat("bb", 3)),
        asyncio.create_task(eat("cc", 4)),
    ]
    # wait函数返回的结果是一个  元组(执行完成的任务，执行超时的任务)
    # 如果没有执行timeout 则永远不会超时

    #如果没有指定timeout参数，那么就永远不会超时。其中，return when
    # 除了默认的 ALL_COMPLETED 外，还有以下可选值:等所有任务都执行完成后再返回。
    # ALL_COMPLETED    等待所有任务执行完成再返回
    # FIRST_EXCEPTION  有任何任务发生异常后就立即返回，即使没有超时也会返回 
    # FIRST_COMPLETED  第一个任务执行完后就立即返回

    done_tasks, pending_tasks = await asyncio.wait(task_list, timeout=3, return_when=asyncio.ALL_COMPLETED)

    print(done_tasks)
    for task in done_tasks:
        print(task.result()) 
        
    print(pending_tasks)
    for task in pending_tasks:
        result = await task
        print(result)

if __name__ == "__main__":
    # # wait_for
    # asyncio.run(main1()

    # wait
    asyncio.run(main2())