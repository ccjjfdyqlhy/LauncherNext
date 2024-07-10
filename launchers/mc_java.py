from . import Launcher
import os
import os.path
from internetDriver import *

CMCL_DOWNLOAD_URL = "https://github.com/MrShieh-X/console-minecraft-launcher/releases/download/latest/cmcl.jar"

class MCLauncher(Launcher):
    def install_cmcl(self):
        CreateDirIfInvalid(os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
        DownloadFile(CMCL_DOWNLOAD_URL, os.path.join(os.getcwd(), "downloads", "Minecraft_Java"))
    def launch(self):
        pass