from utils import async_timed
import asyncio
import time


async def eat(name, time):
    await asyncio.sleep(time)
    return f"{name}: success"


def zuofan(name):
    print(f"{name}: start")
    time.sleep(3)
    print(f"{name}: success")
    return f"{name}: success"

@async_timed
async def main():
    results = await asyncio.gather(
        # eat("aa", 2),
        # asyncio.to_thread(zuofan, "bb"),
        # asyncio.to_thread 将同步函数改写成异步的方式
        asyncio.to_thread(zuofan, name="bb"),
        eat("aa", 2),
    )
    print(results)

if __name__ == '__main__':
    asyncio.run(main())

