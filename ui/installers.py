from launchers import *
import threading

def get_java_installer_onclick(javaverin):
    def java_installer_onclick():
        threading.Thread(target=launchers.mc_java.JavaManager.install_java, args=[javaverin.value]).start()
    return java_installer_onclick