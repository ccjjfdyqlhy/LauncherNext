import requests
import os
import sys
from bs4 import BeautifulSoup

cwd = os.getcwd()

def findit(line):
    request = requests.get("http://localhost:7345/?search=" + line)
    content = request.text
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')
    rowcnt = 0
    results = []  # 创建一个列表存储结果
    for row in table.find_all('tr'):
        row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        rowcnt += 1
        if rowcnt >= 4:
            results.append(row_data)  # 将结果添加到列表
    return results  # 返回结果列表

while True:
    results = findit(input('> ')) 
    print(results)