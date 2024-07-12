import threading
from launchers.mc_java import *

def get_java_installer_onclick(javaverin):
    def java_installer_onclick():
        threading.Thread(target=JavaManager.install_java, args=[javaverin.value]).start()
    return java_installer_onclick