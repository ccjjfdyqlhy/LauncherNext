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
    @classmethod
    def install_java_windows(cls, version):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        DownloadFile(f"https://download.oracle.com/java/{version}/latest/jdk-{version}_windows-x64_bin.exe", os.path.join(os.getcwd(), "downloads", "Minecraft_Java", f"jdk-{version}_windows-x64_bin.exe"))
        os.system("start "+os.path.join(os.getcwd(), "downloads", "Minecraft_Java", f"jdk-{version}_windows-x64_bin.exe"))

    @classmethod
    def install_java_macos(cls, version):
        if platform.machine == "arm64":
            # runnning on arm64
            url = f"https://download.oracle.com/java/{version}/latest/jdk-{version}_macos-aarch64_bin.dmg"
        else:
            # running on x64
            url = f"https://download.oracle.com/java/{version}/latest/jdk-{version}_macos-x64_bin.dmg"

        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        DownloadFile(url, os.path.join(os.getcwd(), "downloads", "Minecraft_Java", f"jdk-{version}_macos_bin.dmg"))
        #unfinished


