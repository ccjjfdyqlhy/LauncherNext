from internetDriver import *
import os
import os.path
import platform
import subprocess

proxy=True
cwd=os.getcwd()
WIN_LINK1="https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_win-x64.zip"
WIN_LINK2="https://mirror.ghproxy.com/https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_win-x64.zip"
MAC_X64_LINK1="https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_osx-x64.zip"
MAC_X64_LINK2="https://mirror.ghproxy.com/https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_osx-x64.zip"
MAC_ARM_LINK1="https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_osx-arm64.zip"
MAC_ARM_LINK2="https://mirror.ghproxy.com/https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_osx-arm64.zip"
LINUX_X64_LINK1="https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_linux-x64.zip"
LINUX_X64_LINK2="https://mirror.ghproxy.com/https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_linux-x64.zip"
LINUX_ARM_LINK1="https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_win-arm64.zip"
LINUX_ARM_LINK2="https://mirror.ghproxy.com/https://raw.githubusercontent.com/2289182718/FastGithub/main/FastGithub-2.1.4/fastgithub_win-arm64.zip"

print("[FGDL] Running On "+platform.system(),platform.machine())

def install():
    if platform.system()=="Windows":
        if platform.machine()=="arm64":
            print("[FGDL] Unsupported Architecture")
        else:
            if proxy:
                DownloadFile(WIN_LINK2, os.path.join(cwd, "downloads", "fastgithub.zip"))
            else:
                DownloadFile(WIN_LINK1, os.path.join(cwd, "downloads", "fastgithub.zip"))
    if platform.system()=="Darwin":
        if platform.machine()=="X86_64":
            if proxy:
                DownloadFile(MAC_X64_LINK2, os.path.join(cwd, "downloads", "fastgithub.zip"))
            else:
                DownloadFile(MAC_X64_LINK1, os.path.join(cwd, "downloads", "fastgithub.zip"))
        if platform.machine()=="arm64":
            if proxy:
                DownloadFile(MAC_ARM_LINK2, os.path.join(cwd, "downloads", "fastgithub.zip"))
            else:
                DownloadFile(MAC_ARM_LINK1, os.path.join(cwd, "downloads", "fastgithub.zip"))
    if platform.system()=="Linux":
        if platform.machine()=="x86_64":
            if proxy:
                DownloadFile(LINUX_X64_LINK2, os.path.join(cwd, "downloads", "fastgithub.zip"))
            else:
                DownloadFile(LINUX_X64_LINK1, os.path.join(cwd, "downloads", "fastgithub.zip"))
        if platform.machine()=="aarch64":
            if proxy:
                DownloadFile(LINUX_ARM_LINK2, os.path.join(cwd, "downloads", "fastgithub.zip"))
            else:
                DownloadFile(LINUX_ARM_LINK1, os.path.join(cwd, "downloads", "fastgithub.zip"))
    UnzipToLocation(os.path.join(cwd, "downloads", "fastgithub.zip"), os.path.join(cwd, "downloads", "fastgithub"))

def launch():
    if platform.system()=="Windows":
        subprocess.Popen(os.path.join(cwd, "downloads", "fastgithub_win-x64", "fastgithub.exe"), shell=True)
    elif platform.system()=="Darwin":
        if platform.machine()=="arm64":
            subprocess.Popen(os.path.join(cwd, "downloads", "fastgithub_osx-arm64", "fastgithub"), shell=True)
        else:
            subprocess.Popen(os.path.join(cwd, "downloads", "fastgithub_osx-x64", "fastgithub"), shell=True)
    elif platform.system()=="Linux":
        if platform.machine()=="arm64":
            subprocess.Popen(os.path.join(cwd, "downloads", "fastgithub_linux-arm64", "fastgithub"), shell=True)
        else:
            subprocess.Popen(os.path.join(cwd, "downloads", "fastgithub_linux-x64", "fastgithub"), shell=True)
