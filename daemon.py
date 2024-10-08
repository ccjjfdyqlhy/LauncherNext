import subprocess
import time
import threading
import logging
import os
import re
import sys
import asyncio
from sys import platform

if platform == 'win32':  
  import psutil
  import winreg

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
cwd = os.getcwd()


async def read_stream(stream, log_function):
    """异步读取流数据并打印"""
    while True:
        line = await stream.readline()
        if not line:
            break
        log_function(line.decode().rstrip())

async def exec_and_capture_output(path, cwd=os.getcwd(), shell=False):
    """
    启动进程，监控其状态，并捕获终端输出（异步方式）。

    Args:
        path: 可执行文件的路径。
        cwd: 工作目录，默认为当前工作目录。
        shell: 是否使用 shell 执行命令，默认为 False。
    """
    try:
        if platform == 'win32':
            process = await asyncio.create_subprocess_exec(
                *path.split(),
                shell=shell,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        elif platform == 'darwin':  # macOS
            process = await asyncio.create_subprocess_exec(
                'open', '-a', 'Terminal', '--args', path,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            raise OSError("Unsupported operating system.")

        logger.info(f"实例入口点 {path} 已启动。 追踪PID: {process.pid}")

        # 异步读取 stdout 和 stderr
        await asyncio.gather(
            read_stream(process.stdout, logger.info),
            read_stream(process.stderr, logger.error),
        )

        await process.wait()
        logger.info(f"实例进程 {path} 已外部终止。")

    except FileNotFoundError:
        logger.error(f"'{path}' 不存在。")
        raise FileNotFoundError(f"'{path}' does not exist.")

def run_in_event_loop(coro):
    """在新线程的 event loop 中运行异步函数"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()

def exec(path,cwd=os.getcwd(),shell=False):
    """启动进程并监控其状态"""
    try:
        process = subprocess.Popen('cmd /c start '+path,shell=shell,cwd=cwd)
        logger.info(f"实例入口点 {path} 已启动。 追踪PID: {process.pid}")
        # 创建线程监控进程状态
        def monitor_process(process, path):
            while True:
                if process.poll() is not None:
                    logger.info(f"实例进程 {path} 已外部终止。")
                    break
                time.sleep(1)
        monitor_thread = threading.Thread(target=monitor_process, args=(process, path))
        monitor_thread.start()
    except FileNotFoundError:
        logger.error(f"'{path}' 不存在。")
        raise FileNotFoundError(f"'{path}' does not exist.")

def run_commands(*commands):
    """
    在同一个终端实例中按顺序执行多条命令，并保留历史记录，输出所有命令的输出和错误信息。

    Args:
        *commands: 要执行的命令，每个命令都是一个字符串。
    """
    if platform == 'win32':
       shell = subprocess.Popen("cmd.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    elif platform == 'Darwin':
        shell = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with shell as master_process:
        for i, command in enumerate(commands):
            # 将每个命令的输出和错误信息都写入主进程的标准输入
            master_process.stdin.write(f"{command}\n")
        # 关闭主进程的标准输入，以便读取所有输出
        master_process.stdin.close()
        # 读取并打印所有命令的输出
        output = master_process.stdout.read()
        print(output)

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

def runtime_out(input_string):
  """
  剔除字符串中匹配预定义正则表达式模式的项目。

  Args:
    input_string: 含有待处理项目的逗号分隔字符串。

  Returns:
    剔除匹配项后，剩余项目组成的逗号分隔字符串。
  """
  patterns = [
    r"^cu.*",
    r"^nv.*",
    r"^Nvidia.*",
    r"^NVIDIA.*",               # 匹配所有以 "NVIDIA" 开头的项目。
    r"^CUDA.*",                 # 匹配所有以 "CUDA" 开头的项目。
    r"^CUBLAS.*",               # 匹配所有以 "CUBLAS" 开头的项目。
    r"^CUFFT.*",                # 匹配所有以 "CUFFT" 开头的项目。
    r"^CUPTI.*",                # 匹配所有以 "CUPTI" 开头的项目。
    r"^CURAND.*",               # 匹配所有以 "CURAND" 开头的项目。
    r"^CUSOLVER.*",             # 匹配所有以 "CUSOLVER" 开头的项目。
    r"^CUSPARSE.*",             # 匹配所有以 "CUSPARSE" 开头的项目。
    r"^Microsoft Visual C++.*", # 匹配所有以 "Microsoft Visual C++" 开头的项目。
    r"^NVRTC.*",                # 匹配所有以 "NVRTC" 开头的项目。
    r"^NV.*",                   # 匹配所有以 "NV" 开头的项目（除了已经被以上规则覆盖的项目）。
    r".*Runtime.*",             # 匹配所有包含 "Runtime" 的项目。
    r".*Documentation.*",       # 匹配所有包含 "Documentation" 的项目。
    r".*Profiler.*",            # 匹配所有包含 "Profiler" 的项目。
    r".*Container.*",           # 匹配所有包含 "Container" 的项目。
    r".*Suite.*",               # 匹配所有包含 "Suite" 的项目。
    r".*Driver.*",              # 匹配所有包含 "Driver" 的项目。
    r".*Installer.*",           # 匹配所有包含 "Installer" 的项目。
    r"vs_FileTracker_Singleton",# 匹配 "vs_FileTracker_Singleton" 项目。
    r"\${{arpDisplayName}}"     # 匹配 "${{arpDisplayName}}" 项目。
  ]

  input_list = [item.strip() for item in input_string.split(',')]
  filtered_list = input_list.copy()

  for pattern in patterns:
    filtered_list = [item for item in filtered_list if not re.match(pattern, item)]

  # 去重
  unique_list = list(set(filtered_list)) 

  return ', '.join(unique_list)

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
    software_string = runtime_out(software_string)
    return software_string

def scan_instances():
    """扫描 /apps/ 文件夹下的内容，并更新 game_local 配置项"""
    apps_dir = os.path.join(cwd, "apps")
    game_local_list = []
    invalid_instance = 0
    exclude_list = ["fastgithub_win-x64","fastgithub_linux-x64","fastgithub_linux-arm64","fastgithub_osx-x64","fastgithub_osx-arm64"]  # 添加排除列表

    if os.path.exists(apps_dir):
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            if os.path.isdir(item_path):
                # 如果是文件夹，且不在排除列表中，则判断是否存在同名 lnxt 文件
                if item not in exclude_list:
                    if os.path.exists(os.path.join(item_path, item + ".lnxt")):
                        # 如果存在，则记录文件夹名
                        game_local_list.append(item)
                    else:
                        # 如果不存在，则 invalid_instance 加 1，但不记录文件夹名
                        invalid_instance += 1
            elif item.endswith(".lnxt"):
                # 如果是 lnxt 文件，则记录文件名
                game_local_list.append(item[:-5])  # 去掉 ".lnxt" 后缀

    # 将文件名统计总数并把它们放到一个用逗号分隔的字符串中
    game_local_str = ",".join(game_local_list)
    return game_local_str, invalid_instance
