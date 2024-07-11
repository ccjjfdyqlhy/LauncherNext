from . import Launcher
import os
import os.path
import platform
from internetDriver import *

class MCLauncher(Launcher):
    JVM_ARGS = {}

    @classmethod
    def add_jvm_arg(cls, arg, val):
        cls.JVM_ARGS[arg] = val

    @classmethod
    def set_jvm_memory_allocation(cls, min_memory="8G", max_memory="8G"):
        cls.JVM_ARGS["Xmx"] = max_memory
        cls.JVM_ARGS["Xms"] = min_memory

    @classmethod
    def reset_jvm_flags(cls):
        cls.JVM_ARGS = {"Xmx": "8G", "Xms": "8G", 
                        "XX:+UnlockExperimentalVMOptions": "", 
                        "XX:+UnlockDiagnosticVMOptions":"",
                        "XX:+AlwaysPreTouch":"",
                        "XX:+DisableExplicitGC":"", 
                        "XX:+UseNUMA":"",
                        "XX:NmethodSweepActivity=":"1",
                        "XX:ReservedCodeCacheSize=":"400M",
                        "XX:NonNMethodCodeHeapSize=":"12M",
                        "XX:ProfiledCodeHeapSize=":"194M",
                        "XX:NonProfiledCodeHeapSize=":"194M",
                        "XX:-DontCompileHugeMethods":"",
                        "XX:MaxNodeLimit=":"240000",
                        "XX:NodeLimitFudgeFactor=":"8000",
                        "XX:+UseVectorCmov":"",
                        "XX:+PerfDisableSharedMem":"",
                        "XX:+UseFastUnorderedTimeStamps":"",
                        "XX:+UseCriticalJavaThreadPriority":"",
                        "XX:ThreadPriorityPolicy=":"1",
                        "XX:AllocatePrefetchStyle=":"3",
                        "XX:+UseG1GC":"",
                        "XX:MaxGCPauseMillis=":"37",
                        "XX:+PerfDisableSharedMem":"",
                        "XX:G1HeapRegionSize=":"16M",
                        "XX:G1NewSizePercent=":"23",
                        "XX:G1ReservePercent=":"20",
                        "XX:SurvivorRatio=":"32",
                        "XX:G1MixedGCCountTarget=":"3",
                        "XX:G1HeapWastePercent=":"20",
                        "XX:InitiatingHeapOccupancyPercent=":"10",
                        "XX:G1RSetUpdatingPauseTimePercent=":"0",
                        "XX:MaxTenuringThreshold=":"1",
                        "XX:G1SATBBufferEnqueueingThresholdPercent=":"30",
                        "XX:G1ConcMarkStepDurationMillis=":"5.0",
                        "XX:G1ConcRSHotCardLimit=":"16",
                        "XX:G1ConcRefinementServiceIntervalMillis=":"150",
                        "XX:GCTimeRatio=":"99",
                        "XX:+UseLargePages":"",
                        "XX:LargePageSizeInBytes=":"2m",
                        }

    @classmethod
    def gen_jvm_args(cls):
        jvm_args = []
        for arg, val in cls.JVM_ARGS.items():
            jvm_args.append("-" + arg + val)
        return jvm_args

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


