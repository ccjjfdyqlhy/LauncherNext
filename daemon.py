import subprocess
import time
import threading
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def exec(path,shell=False):
    """启动进程并监控其状态"""
    try:
        process = subprocess.Popen(path,shell=shell)
        logger.info(f"Executable {path} launched. PID: {process.pid}")
        # 创建线程监控进程状态
        def monitor_process(process, path):
            while True:
                if process.poll() is not None:
                    logger.info(f"Process {path} terminated.")
                    break
                time.sleep(1)
        monitor_thread = threading.Thread(target=monitor_process, args=(process, path))
        monitor_thread.start()
    except FileNotFoundError:
        logger.error(f"'{path}' does not exist.")
