import abc

launchers = {
    "Minecraft Java": "launchers.mc_java.MCLauncher",
}

class Launcher(abc.ABC):
    @abc.abstractmethod
    def launch(self, *args, **kwargs):
        "Launch the game"
        raise NotImplemented
