from functools import wraps
import time

# 装饰器
def async_timed(func):
    @wraps(func)
    async def wrapper(*args, **kwrags):
        print(f"开始执行{func}，参数：{args}，{kwrags}")
        start = time.time()
        try:
            return await func(*args, **kwrags)
        finally:
            end = time.time()
            total = end - start
            print(f"结束执行{func}，耗时：{total:.4f}")
    return wrapper