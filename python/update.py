import re
import requests
import os
import subprocess
import shutil
from bs4 import BeautifulSoup

def update_script(new_latest):
    script_file = __file__
    with open(script_file, 'r') as file:
        lines = file.readlines()

    # Find the second occurrence of 'latest ='
    found_first = False
    for i, line in enumerate(lines):
        if line.strip().startswith("latest ="):
            if not found_first:
                # Skip the first occurrence
                found_first = True
            else:
                # Update the second occurrence
                lines[i] = f'   latest = "{new_latest}"\n'
                break

    with open(script_file, 'w') as file:
        file.writelines(lines)
        
def download(url):
    if not os.path.exists("archive riot"):
        os.makedirs("archive riot")
    if not os.path.exists("Data"):
        os.makedirs("Data")
    path = "archive riot/"
    print("Downloading...")
    response = requests.get(url)
    response.raise_for_status()
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(path, url.split('/')[-1])
    print(f"archive in {local_filename}")
    
    with open(local_filename, 'wb') as w:
        for chunk in response.iter_content(chunk_size=8192):
            w.write(chunk)
            
    return local_filename
    
def dezip(path):
    print("unzip...")
    command=["tar","zxvf",path,"-C","Data/"]
    subprocess.run(command)
    print("unzip done.")

    return path

def isPatch(name:str) -> bool:
    pattern = r'^[0-9.]+$'
    return re.match(pattern,name)

def delete(path):
    #Delete the archive file and languages that arent specified 
    os.remove(path)
    path = f"Data/{path.split('/')[-1].split('-')[1].rsplit('.', 1)[0]}"
    keep = ['en_GB', 'en_US', 'fr_FR', 'ja_JP', 'ko_KR']
    for root, dirs, files in os.walk(f"{path}/data"):
        for direc in dirs:
            if direc not in keep:
                dir_path = os.path.join(path, "data", direc)
                if os.path.exists(dir_path):
                    print(f"Deleting directory: {dir_path}")
                    shutil.rmtree(dir_path)
        break
    
    # Remove files from patches older than the last 2 patches
    tab = []
    for root,dirs,files in os.walk("Data"):
        for direc in dirs:
            if isPatch(direc):
                tab.append(direc)
                
    if (len(tab)>2):
        while len(tab)>2 :
            oldest_patch = min(tab)
            print("removing patch "+ oldest_patch)
            shutil.rmtree("Data/" + oldest_patch)
            shutil.rmtree("Data/lolpatch_" + '.'.join(oldest_patch.split('.')[0:2]))
            tab.remove(oldest_patch)
        
                
    return path
    
def formatPrettier(path):
    print("Starting to format with prettier")
    pathToData1 = path.split('/')[0]
    pathToNumber = path.split('/')[1]
    os.chdir(pathToData1)
    command = ['prettier', '--write', '*.js']
    subprocess.run(command, shell=True)
    command[2] = '*.json'
    subprocess.run(command, shell=True)
    os.chdir(pathToNumber)
    command[2] = '**/*.js'
    subprocess.run(command, shell=True)
    command[2] = '**/*.json'
    subprocess.run(command, shell=True)
    pathToShortNumber = pathToNumber.split('.')[0] + '.' + pathToNumber.split('.')[1]
    os.chdir("../lolpatch_" + pathToShortNumber)
    command[2] = '*.js'
    subprocess.run(command, shell=True)
    command[2] = '*.json'
    subprocess.run(command, shell=True)
    
def update():
    global latest
    url="https://developer.riotgames.com/docs/lol"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    
    links = soup.find_all('a',href=True)
    for link in links:
        if ".tgz" in link['href'] and link['href']!=latest:
            latest = link['href']
            update_script(latest)
            print(f"\033[34mfound a recent patch : {latest.split('/')[-1]}\033[0m") # blue
            formatPrettier(delete(dezip(download(latest))))
            print(f"\033[32mupdated to patch {'.'.join(latest.split('/')[-1].split('-')[-1].split('.')[:-1])}\033[0m") # green
            gotUpdated = False
        elif ".tgz" in link['href'] and link['href']==latest:
            print("\033[34mPatch up to date\033[0m")
            gotUpdated = True  

if __name__ == "__main__" or __name__ == "update":
   latest = "https://ddragon.leagueoflegends.com/cdn/dragontail-14.24.1.tgz"
   update()