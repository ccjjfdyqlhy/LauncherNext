import json
import requests
import zipfile
import os
from tqdm import tqdm

def ConstructUrl(username, reponame):
  return "https://api.github.com/repos/" + username + "/" + reponame + "/releases/latest"

def GetJsonData(url, username = None):
  if(username):
    response = requests.get(url, auth = (username,'token'))
  else:
    response = requests.get(url,verify=False)
  loaded = json.loads(response.text)
  return loaded

def GetAssetDownloads(jsonData):
  assets = jsonData["assets"]
  out = []
  for i in assets:
    out += [i['browser_download_url']]
  return out

def RetrieveDownloadLinks(repoUsername, reponame, downloaderUsername = None):
  builtUrl = ConstructUrl(repoUsername, reponame)
  jsonData = GetJsonData(builtUrl, downloaderUsername)
  assetLinks = GetAssetDownloads(jsonData)
  return assetLinks

def GetFileNamesFromUrls(downloadLinks):
  out = []
  for currLink in downloadLinks:
    fileName = (currLink.split('/')[-1:][0])
    out += [fileName]
  return out

def CreateDirIfInvalid(dst):
  isDir = os.path.isdir(dst)
  if(not isDir):
    os.mkdir(dst)

def AbsPathConstructor(fileName, dst):
  if(not dst):
    return fileName
  if(dst[-1] != '/' and dst[-1] != "\\"):
    dst += '/'
  CreateDirIfInvalid(dst)
  return dst+fileName

def DownloadFile(url, fileName):
  try:
    fileObject = requests.get(url,stream=True,verify=False)
    total = int(fileObject.headers.get('content-length', 0))
    with open(fileName, 'wb') as localFile, tqdm(
      desc=fileName,
      total=total,
      unit='iB',
      unit_scale=True,
      unit_divisor=1024,
      ) as bar:
      bar.set_description('LauncherNext 内容下载')
      for data in fileObject.iter_content(chunk_size=1024):
        size = localFile.write(data)
        bar.update(size)
  except requests.exceptions.ConnectTimeout:
    print('[DWNL] 下载失败，连接超时。')

def UnzipToLocation(src, dst, deleteSrc = True):
  with zipfile.ZipFile(src, 'r') as zip_ref:
    zip_ref.extractall(dst)
  if deleteSrc:
    os.remove(src)

def CheckIfZip(fileName):
  return zipfile.is_zipfile(fileName)