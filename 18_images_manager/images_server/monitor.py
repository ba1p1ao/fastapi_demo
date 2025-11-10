#!/usr/bin/env python3
import psutil
import time
import redis

def monitor_system():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    while True:
        # 系统指标
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Redis指标
        try:
            redis_info = r.info()
            connected_clients = redis_info['connected_clients']
            used_memory = redis_info['used_memory_human']
        except:
            connected_clients = 0
            used_memory = "N/A"
        
        print(f"\r内存使用: {memory.percent:.1f}% | CPU使用: {cpu_percent:.1f}% | 磁盘使用: {disk.percent:.1f}% | Redis连接: {connected_clients} | Redis内存: {used_memory}", end="", flush=True)
        
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        monitor_system()    
    except KeyboardInterrupt:
        print("\n监控结束")
