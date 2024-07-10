from . import Launcher
import os
import os.path
import platform
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
    versions = {
        "17": "https://download.oracle.com/java/17/latest/jdk-17_",
        "8": "https://github.com/hmsjy2017/get-jdk/releases/download/v8u231/jdk-8u231-"
    }
    @classmethod
    def install_java_windows(cls, version):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java"))
        DownloadFile(cls.versions[version]+"windows-x64_bin.exe", os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_windows-x64_bin.exe"))
        os.system("start "+os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_windows-x64_bin.exe"))

    @classmethod
    def install_java_macos(cls, version):
        if platform.machine() == "arm64":
            if version == "8":
                raise NotImplementedError("Doesn't support Java 8 on Apple M-seriess")
            # runnning on arm64
            url = cls.versions[version]+"macos-aarch64_bin.dmg"
        else:
            # running on x64
            url = cls.versions[version]+"macos-x64_bin.dmg"

        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java"))
        path = os.path.join(os.getcwd(), "downloads", "Minecraft_Java", "java", f"jdk-{version}_macos_bin.dmg")
        DownloadFile(url, path)
        print("[INFO] 请手动安装Java：双击Java安装器")
        import subprocess
        subprocess.Popen(["open", path])
    @classmethod
    def install_java(cls, version="17"):
        if platform.system() == "Darwin": #on MacOS
            cls.install_java_macos(version)
        elif platform.system() == "Windows": # on Windows
            cls.install_java_windows(version)
        else: #on Linux
            raise NotImplementedError("Not implemented yet")


        
        #unfinished


