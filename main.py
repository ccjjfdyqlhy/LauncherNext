from ui import main
import utils.fastgithub_launcher as fglauncher

test=0

if __name__ in {"__main__", "__mp_main__"}: # Allow for multiprocessing
    if test == 0:
        main()
    elif test == 1:
        fglauncher.install()
        fglauncher.launch()