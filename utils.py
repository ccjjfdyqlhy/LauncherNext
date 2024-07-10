import os
from internetDriver import *

cwd=os.getcwd()

def download(url,save_name):
    DownloadFile(url,cwd+'\\download\\'+save_name)