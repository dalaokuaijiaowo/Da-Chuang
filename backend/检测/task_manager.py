"""任务管理器 - 用于跟踪检测任务进度"""
import threading
import time
import uuid
from typing import Dict, Optional

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, dict] = {}
        self.lock = threading.Lock()
    
    def create_task(self, filename: str, total: int) -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tasks[task_id] = {
                'id': task_id,
                'filename': filename,
                'status': 'running',  # running, completed, failed
                'progress': 0,
                'total': total,
                'current': 0,
                'result': None,
                'error': None,
                'created_at': time.time()
            }
        return task_id
    
    def update_progress(self, task_id: str, current: int):
        """更新任务进度"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['current'] = current
                self.tasks[task_id]['progress'] = int(current / self.tasks[task_id]['total'] * 100)
    
    def complete_task(self, task_id: str, result: dict):
        """完成任务"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'completed'
                self.tasks[task_id]['progress'] = 100
                self.tasks[task_id]['result'] = result
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['error'] = error
    
    def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务信息"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def cleanup_old_tasks(self, max_age: int = 3600):
        """清理旧任务"""
        current_time = time.time()
        with self.lock:
            to_remove = [
                task_id for task_id, task in self.tasks.items()
                if current_time - task['created_at'] > max_age
            ]
            for task_id in to_remove:
                del self.tasks[task_id]

# 全局任务管理器实例
task_manager = TaskManager()
