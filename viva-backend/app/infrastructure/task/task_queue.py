import asyncio
from typing import Callable, Any
from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.is_processing = False

    async def add_task(self, task: Callable[..., Any], *args, **kwargs):
        self.queue.append((task, args, kwargs))
        if not self.is_processing:
            asyncio.create_task(self.process_queue())

    async def process_queue(self):
        self.is_processing = True
        while self.queue:
            task, args, kwargs = self.queue.popleft()
            try:
                if asyncio.iscoroutinefunction(task):
                    await task(*args, **kwargs)
                else:
                    task(*args, **kwargs)
            except Exception as e:
                print(f"Error processing task: {e}")
        self.is_processing = False

    def get_queue_size(self):
        return len(self.queue)

# 创建一个全局的 TaskQueue 实例
global_task_queue = TaskQueue()

def get_task_queue():
    return global_task_queue