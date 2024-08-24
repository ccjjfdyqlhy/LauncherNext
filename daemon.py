import subprocess
import time
import threading
import logging
import os
import psutil
import winreg

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def exec(path,cwd=os.getcwd(),shell=False):
    """启动进程并监控其状态"""
    try:
        process = subprocess.Popen('cmd /c start '+path,shell=shell,cwd=cwd)
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

def is_alive(process_name):
  """检查给定名称的进程是否正在运行。

  Args:
    process_name: 要检查的进程名称。

  Returns:
    如果找到进程，则返回True，否则返回False。
  """
  for proc in psutil.process_iter(['name']):
    try:
      if proc.info['name'].lower() == process_name.lower():
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  return False

def get_installed_list_win():
    """获取 Windows 系统上安装的软件列表，以逗号分隔的字符串形式返回。"""

    software_list = []

    for i in range(2):  # 检查 32 位和 64 位注册表项
        if i == 0:
            reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        else:
            reg_path = r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                num_subkeys = winreg.QueryInfoKey(key)[0]

                for j in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(key, j)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            display_name, _ = winreg.QueryValueEx(subkey, 'DisplayName')
                            if display_name:
                                software_list.append(display_name)
                    except WindowsError:
                        pass
        except WindowsError:
            pass

    # 将软件列表转换为逗号分隔的字符串
    software_string = ", ".join(software_list)
    return software_string