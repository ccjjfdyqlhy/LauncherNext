from internetDriver import *
import sys
import os

os.system('cls')
try:
  with open('DSproduct.cfg', 'r') as f:
    PRODUCT_NAME = f.read()
    f.close()
except FileNotFoundError:
  print('请放入产品配置文件。')
  input('[Enter] 退出...')
  os.system('cls')
  quit()

def BeautifyStringArray(items):
  out = []
  for i in range(len(items)):
    out += [("["+str(i)+"]: " + items[i])]
  return out

def chooseFile(linkFileNames):
  beautified = BeautifyStringArray(linkFileNames)
  print("\n可供选择的更新:")
  for i in beautified:
    print(i)

  chosenInd = input("输入你要下载的更新对应序号:\n")
  return(int(chosenInd))

#generate parameters via text input if no commandline input
def GenerateParameters():
  repouser = 'ccjjfdyqlhy'
  reponame = PRODUCT_NAME
  dst = os.getcwd()
  myuser = ''

  return repouser,reponame,dst,myuser

def GetParameters():
  #get parameters
  params = []
  if (len(sys.argv) > 1):
    for i in sys.argv[1:]:
      params += [i]

  #verify enough params, else have entry manually
  if(len(params) < 2):
    print("\nTEAM ENCHANTED Product Update Tool\n接收更新的产品: "+PRODUCT_NAME+"\n请确保你是收到更新消息后打开的程序。\n\n随时按下 [Ctrl+C] 取消操作。")
    #print("main.py <repo owner> <repo name> <destination (optional)> <your username (optional)>")
    return GenerateParameters()
  
  #add dst if not found
  if(len(params) < 3):
    params += [""]

  #add myuser if not found
  if(len(params) < 4):
    params += [None]

  #return parameters
  return params[0],params[1],params[2],params[3]
  

def main():
  cwd=os.getcwd()
  print('正在获取更新信息...')
  repouser, reponame, dst, myuser = GetParameters()
  try:
    downloadLinks = RetrieveDownloadLinks(repouser, reponame, myuser)
    linkFileNames = GetFileNamesFromUrls(downloadLinks)
  except KeyError:
    print("无法获取更新信息。请确保你的网络连接正常且产品文件有效。")
    input('[Enter] 退出...')
    os.system('cls')
    quit()
  if(len(linkFileNames) < 2):
    chosenInd = 0
  else:
    chosenInd = chooseFile(linkFileNames)
  chosenUrl = 'https://mirror.ghproxy.com/'+downloadLinks[chosenInd]
  chosenFile = AbsPathConstructor(linkFileNames[chosenInd], dst)
  print("更新包下载位置: " + chosenFile)
  print('\n')
  #print("\nDownloading " + chosenFile + " from " + chosenUrl + "...")
  try:
    DownloadFile(chosenUrl, chosenFile)
  except KeyboardInterrupt:
    print("下载已取消。")
    input('[Enter] 退出...')
    os.system('cls')
    quit()
  print("下载完成。")

  if(CheckIfZip(chosenFile) == True):
    print("正在应用更新。少安毋躁，这用不了太久。")
    UnzipToLocation(chosenFile, dst, True)
    print("完成。")
  else:
    print("没有检测到要应用的更新，遂跳过。")

  print('MCSA 已就绪。')
  input('[Enter] 退出...')
  os.system('cls')
  quit()

if __name__ == "__main__":
  main()