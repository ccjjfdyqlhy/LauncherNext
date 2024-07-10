from . import Launcher
import os
import os.path
from internetDriver import *

CMCL_DOWNLOAD_URL = "https://github.com/MrShieh-X/console-minecraft-launcher/releases/download/latest/cmcl.jar"
JAVA_DOWNLOAD_URL = "https://download.oracle.com/java/{version}/latest/jdk-{version}_windows-x64_bin.exe"

class MCLauncher(Launcher):
    def install_cmcl(self):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        DownloadFile(CMCL_DOWNLOAD_URL, os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
    def launch(self):
        pass

class JavaManager():
    def install_java_windows(version):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        DownloadFile(f"https://download.oracle.com/java/{version}/latest/jdk-{version}_windows-x64_bin.exe", os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        os.start(os.path.join(os.getcwd(), "downloads", "Minecraft_Java", f"jdk-{version}_windows-x64_bin.exe"))
