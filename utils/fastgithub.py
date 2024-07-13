import logging
import os
import os.path
import platform
import subprocess

from internetDriver import *

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
cwd=os.getcwd()
logger.info("Running On "+platform.system()+platform.machine())

def unzip(ver="win-x64"):
    UnzipToLocation(os.path.join(cwd, "FastGithub-2.1.4", "fastgithub_"+ver+".zip"), os.path.join(cwd, "apps"),False)

def install():
    if platform.system()=="Windows":
        if platform.machine()=="arm64":
            logger.error("[FGDL] Unsupported Architecture")
        else:
            unzip()
    if platform.system()=="Darwin":
        if platform.machine()=="X86_64":
            unzip("osx-x64")
        if platform.machine()=="arm64":
            unzip("osx-arm64")
    if platform.system()=="Linux":
        if platform.machine()=="x86_64":
            unzip("linux-x64")
        if platform.machine()=="aarch64":
            unzip("linux-arm64")
    if platform.system()=="Windows":
        return # no need for chmod
    elif platform.system()=="Darwin":
        if platform.machine()=="arm64":
            os.chmod(os.path.join(cwd, "apps", "fastgithub_osx-arm64", "fastgithub"), 0o777)
        else:
            os.chmod(os.path.join(cwd, "apps", "fastgithub_osx-x64", "fastgithub"), 0o777)
    elif platform.system()=="Linux":
        if platform.machine()=="arm64":
            os.chmod(os.path.join(cwd, "apps", "fastgithub_linux-arm64", "fastgithub"), 0o777)
        else:
            os.chmod(os.path.join(cwd, "apps", "fastgithub_linux-x64", "fastgithub"), 0o777)

def launch():
    if not os.path.exists(os.path.join(cwd, "apps", "fastgithub_win-x64" or "fastgithub_osx-x64" or "fastgithub_osx-arm64" or "fastgithub_linux-x64" or "fastgithub_linux-arm64")):
        install()
    if platform.system()=="Windows":
        subprocess.Popen(os.path.join(cwd, "apps", "fastgithub_win-x64", "fastgithub.exe"), shell=True)
    elif platform.system()=="Darwin":
        if platform.machine()=="arm64":
            subprocess.Popen(os.path.join(cwd, "apps", "fastgithub_osx-arm64", "fastgithub"), shell=True)
        else:
            subprocess.Popen(os.path.join(cwd, "apps", "fastgithub_osx-x64", "fastgithub"), shell=True)
    elif platform.system()=="Linux":
        if platform.machine()=="arm64":
            subprocess.Popen(os.path.join(cwd, "apps", "fastgithub_linux-arm64", "fastgithub"), shell=True)
        else:
            subprocess.Popen(os.path.join(cwd, "apps", "fastgithub_linux-x64", "fastgithub"), shell=True)

def kill(): #Does not work yet
    if platform.system()=="Windows":
        subprocess.Popen("taskkill /f /im fastgithub.exe", shell=True)
        subprocess.Popen("taskkill /f /im dnscrypt-proxy.exe", shell=True)
    elif platform.system()=="Linux":
        subprocess.Popen("pkill fastgithub", shell=True)
        subprocess.Popen("pkill dnscrypt-proxy", shell=True)
    elif platform.system()=="Darwin":
        subprocess.Popen("pkill fastgithub", shell=True)
        subprocess.Popen("pkill dnscrypt-proxy", shell=True)