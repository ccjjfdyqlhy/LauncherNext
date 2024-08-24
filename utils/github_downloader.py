import argparse
import sys

# 引入你的代码
from internetDriver import *

def gdownload():
    parser = argparse.ArgumentParser(description="下载GitHub仓库的最新发布版本")
    parser.add_argument("repo", help="GitHub仓库名称，格式为：<作者名>/<仓库名>")
    parser.add_argument("--token", help="GitHub Token，用于认证下载权限", default=None)
    args = parser.parse_args()

    repo_name = args.repo
    token = args.token
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

        print(f"成功下载{repo_name}仓库的最新发布版本到 /downloads/ 目录。")

    except Exception as e:
        print(f"下载失败：{e}")
        sys.exit(1)
