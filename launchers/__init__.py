import abc

import os
if not os.path.exists(os.path.join(os.getcwd(), "downloads")):
    os.mkdir(os.path.join(os.getcwd(), "downloads"))

launchers = {
    "Minecraft Java": "launchers.mc_java.MCLauncher",
}

class Launcher(abc.ABC):
    @abc.abstractmethod
    def launch(self, *args, **kwargs):
        "Launch the game"
        raise NotImplemented
