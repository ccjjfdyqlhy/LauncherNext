from ui import main
import utils.fastgithub_launcher as fglauncher
import logging

test=0
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ in {"__main__", "__mp_main__"}: # Allow for multiprocessing
    if test == 0:
        main()
    elif test == 1:
        logger.warn('Testing FastGithub Launcher')
        fglauncher.install()
        fglauncher.launch()