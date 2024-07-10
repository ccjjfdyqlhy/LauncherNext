from . import Launcher
import os
import os.path
import platform
import dmglib
from internetDriver import *

class MCLauncher(Launcher):
    @classmethod
    def install_cmcl(cls):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        all_links = RetrieveDownloadLinks("MrShieh-X", "console-minecraft-launcher")
        for link in all_links:
            if link.endswith("jar"):
                url = link
                break
        else:
            assert False, "This shouldn't happen: no jar version of cmcl"
        DownloadFile("https://mirror.ghproxy.com/"+url, os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "cmcl.jar"))
    @classmethod
    def launch(cls):
        pass

class JavaManager():
    @classmethod
    def install_java_windows(cls, version):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java"))
        DownloadFile(f"https://download.oracle.com/java/{version}/latest/jdk-{version}_windows-x64_bin.exe", os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_windows-x64_bin.exe"))
        os.start(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_windows-x64_bin.exe"))

    @classmethod
    def install_java_macos(cls, version):
        if platform.machine == "arm64":
            # runnning on arm64
            url = f"https://download.oracle.com/java/{version}/latest/jdk-{version}_macos-aarch64_bin.dmg"
        else:
            # running on x64
            url = f"https://download.oracle.com/java/{version}/latest/jdk-{version}_macos-x64_bin.dmg"

        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java"))
        path = os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_macos_bin.dmg")
        DownloadFile(url, path)
        print("[INFO] 请手动安装Java：双击Java安装器")
        import subprocess
        subprocess.Popen(["open", path])

    def install_java(cls, version="17"):
        if platform.system() == "Darwin": #on MacOS
            cls.install_java_macos(version)
        elif platform.system() == "Windows" # on Windows
            cls.install_java_windows(version)
        else: #on Linux
            raise NotImplementedError("Not implemented yet")


        
        #unfinished


