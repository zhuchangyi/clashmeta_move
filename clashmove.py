import os
import requests
import re
import zipfile
import subprocess
import stat
subprocess.run(["pip", "install", "psutil"])
import psutil
from tqdm import tqdm

def download_file(url, file_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(file_path, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        print("下载失败！")
    else:
        print("文件下载成功！")

def find_clash_for_windows():
    process_name = "clash-win64.exe"
    findpath = False
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['name'] == process_name:
            process_path = proc.info['exe']
            process_path = os.path.dirname(process_path)
            print(f"{process_name} 的路径是：{process_path}")
            findpath = True
            break
    if findpath == True:
        return process_path
    else:
        #print(f"未打开 {process_name} 程序！")
        return None
parent_path = find_clash_for_windows()
if parent_path is None:
    print("请先打开clash for windows!")
    exit()

#os.startfile(parent_path)

direct = False

    
url = "https://github.com/MetaCubeX/Clash.Meta/releases/latest"

try:
    response = requests.get(url, allow_redirects=False, timeout=5)
    
except:
    url = f"https://ghproxy.com/{url}"
    direct = True
    response = requests.get(url, allow_redirects=False)
if response.status_code == 302:
    redirect_url = response.headers["Location"]
    print(f"重定向后的 URL 是：{redirect_url}")
    version = re.search(r"/tag/v(\d+\.\d+\.\d+)", redirect_url).group(1)
    v1 = {'v'+version}
    v2={'clash.meta-windows-amd64-v'+version+'.zip'}
    asset_url = f"https://github.com/MetaCubeX/Clash.Meta/releases/download/{'v'+version}/{'clash.meta-windows-amd64-v'+version+'.zip'}"
    
    if direct == False:
        print(f"下载地址是：{asset_url}") 
        
    else:
        asset_url = f"https://ghproxy.com/{asset_url}"
        print(f"下载地址是：{asset_url}") 

     
    response = requests.get(asset_url)
    
    if response.status_code == 200:
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        download_file(asset_url, os.path.join(parent_path, f"clash.meta-windows-amd64-v{version}.zip"))
        zip_file_path = os.path.join(parent_path, 'clash.meta-windows-amd64-v'+version+'.zip')
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(parent_path)
        print("文件解压成功！")
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'Clash for Windows.exe':
                # 关闭进程
                proc.kill()
        file_path = os.path.join(parent_path, "clash-win64.exe")
        if os.path.exists(file_path):
            print("clash-win64.exe exists, removing...")
            os.chmod(file_path, stat.S_IWRITE)
            os.remove(file_path)
        pathmeta = os.path.join(parent_path, "clash.meta-windows-amd64.exe")
        os.rename(pathmeta, os.path.join(parent_path, "clash-win64.exe"))
        print("内核更换成功！")

    else:
            print("文件下载失败！")
else:
    print("获取重定向后的 URL 失败！")


