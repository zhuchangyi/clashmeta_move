import os
import requests
import re

def find_clash_for_windows():
    # 获取系统盘符
    system_drive = os.getenv("SystemDrive")

    # 在系统盘符下查找 Clash for Windows 的安装路径
    for root, dirs, files in os.walk(system_drive):
        if "Clash for Windows.exe" in files:
            return os.path.join(root, "Clash for Windows.exe")

    # 如果找不到 Clash for Windows 的安装路径，则返回 None
    return None
clash_path = find_clash_for_windows()
if clash_path:
    print(f"Clash for Windows 的安装路径是：{clash_path}")
    parent_path = os.path.dirname(clash_path)
    print(f"Clash for Windows 的上一层路径是：{parent_path}")

else:
    print("找不到 Clash for Windows 的安装路径！")

parent_path = os.path.join(parent_path, "resources", "static", "files", "win", "x64")
print(f"Clash for Windows 的配置文件路径是：{parent_path}")
#os.startfile(parent_path)
url = "https://github.com/MetaCubeX/Clash.Meta/releases/latest"
response = requests.get(url, allow_redirects=False)
if response.status_code == 302:
    redirect_url = response.headers["Location"]
    print(f"重定向后的 URL 是：{redirect_url}")
    version = re.search(r"/tag/v(\d+\.\d+\.\d+)", redirect_url).group(1)
    v1 = {'v'+version}
    v2={'clash.meta-windows-amd64-v'+version+'.zip'}
    asset_url = f"https://github.com/MetaCubeX/Clash.Meta/releases/download/{'v'+version}/{'clash.meta-windows-amd64-v'+version+'.zip'}"
    print(f"下载地址是：{asset_url}")
    response = requests.get(asset_url)
    if response.status_code == 200:
        file_path = os.path.join(parent_path, "clash-win64.exe")
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "clash-win64.exe") as f:
            f.write(response.content)
        print("文件下载成功！")
    else:
            print("文件下载失败！")
else:
    print("获取重定向后的 URL 失败！")


