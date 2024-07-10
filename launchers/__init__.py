import abc

launchers = {
    "Minecraft Java": "launchers.mc_java.MCLauncher",
}

class Launcher(abc.ABC):
    @abs.abstractmethod
    def launch(self, *args, **kwargs):
        "Launch the game"
        raise NotImplemented
