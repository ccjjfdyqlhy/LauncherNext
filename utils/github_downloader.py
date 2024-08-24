import sys,logging

# 引入你的代码
from internetDriver import *

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def gdownload(repo_name, token=None):
    """
    下载GitHub仓库的最新发布版本

    Args:
        repo_name (str): GitHub仓库名称，格式为：<作者名>/<仓库名>
        token (str, optional): GitHub Token，用于认证下载权限. Defaults to None.
    """
    
    repo_author, repo_name = repo_name.split('/')

    try:
        download_links = RetrieveDownloadLinks(repo_author, repo_name, downloaderUsername=token)
        file_names = GetFileNamesFromUrls(download_links)

        for i in range(len(download_links)):
            file_name = file_names[i]
            download_link = download_links[i]
            abs_path = AbsPathConstructor(file_name, "/downloads/")
            DownloadFile(download_link, abs_path)
            if CheckIfZip(abs_path):
                UnzipToLocation(abs_path, "/downloads/")

        logger.info(f"成功下载{repo_name}仓库的最新发布版本到 /downloads/ 目录。")

    except Exception as e:
        logger.error(f"下载失败：{e}")