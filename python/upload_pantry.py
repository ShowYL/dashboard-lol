import os
import re
import dotenv
import requests
import json
from pathlib import Path
from typing import List
import time

dotenv.load_dotenv()

PANTRY_API_KEY = os.getenv('VITE_PANTRY_API_KEY')

def select_file(file_path: str) -> Path:
    """
    Selects a file given its file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        Path: The Path object of the file if it exists.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    path = Path(file_path)
    if path.is_file():
        return path
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")

def send_file(file_name: str, data: dict, re_send: bool):
    """
    Sends a file to a specified URL using a POST request.
    Args:
        file_name (str): The name of the file to be sent.
        data (dict): The data to be sent in the request body.
        re_send (bool): A flag indicating whether this is a resend attempt.
    Returns:
        None
    Side Effects:
        Prints a success message if the file is sent successfully.
        Prints an error message and retries sending the file if the request fails.
    """
    time.sleep(0.6)
    
    url = f"https://getpantry.cloud/apiv1/pantry/{PANTRY_API_KEY}/basket/{file_name}"

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"\033[32mFile {file_name} {'resend' if re_send else 'send'} successfully.\033[0m") # green
    else:
        print(f"\033[31mFailed to {'resend' if re_send else 'send'} {file_name} file. Status code: {response.status_code}\033[0m") # red
        send_file(file_name, data, True)
        
def delete_file(file_name: str):
    """
    Deletes a file from the specified URL using the provided file name.
    Args:
        file_name (str): The name of the file to be deleted.
        data (dict): A dictionary containing additional data (not used in the function).
    Returns:
        None
    Side Effects:
        - Sends a DELETE request to the specified URL.
        - Prints the result of the delete operation.
        - Recursively calls itself if the delete operation fails with a status code other than 200 or 400.
    Notes:
        - The function includes a delay of 0.6 seconds before sending the DELETE request.
        - The PANTRY_API_KEY must be defined in the scope where this function is used.
    """
    time.sleep(0.6)
    
    url = f"https://getpantry.cloud/apiv1/pantry/{PANTRY_API_KEY}/basket/{file_name}"

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        print(f"\033[32mFile {file_name} deleted successfully.\033[0m") # green
    elif response.status_code == 400:
        print(f"\033[38;5;208m{file_name} probably doesnt exist\033[0m") # orange
    else:
        print(f"\033[31mFailed to delete {file_name} file. Status code: {response.status_code}\033[0m") # red
        delete_file(file_name)
        
def conditionner(files_path: dict):
    PACKET_SIZE = 1_400_000  # 1.40 MB in bytes
    packet = {}
    current_packet = {}
    current_size = 0

    for file_name, file_path in files_path.items():
        file_size = os.path.getsize(file_path)
        
        if current_size + file_size > PACKET_SIZE:
            packet_key = next(iter(current_packet)).split('.')[0]
            packet[packet_key] = current_packet
            current_packet = {}
            current_size = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        current_packet[file_name] = file_data
        current_size += file_size

    if current_packet:
        packet_key = next(iter(current_packet)).split('.')[0]
        packet[packet_key] = current_packet

    with open('Data/pantry.json', 'w', encoding='utf-8') as j:
        json.dump(packet, j, ensure_ascii=False, indent=4)

    for key, value in packet.items():
        size = sum(os.path.getsize(files_path[file_name]) for file_name in value.keys()) / (1024 * 1024)
        print(f"Size of {key}: {size:.2f} MB")

    return packet

def getPatch() -> str:
    for root, dirs, files in os.walk('Data/'):
        reg = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{1,2}$')
        for dirc in dirs:
            if reg.match(dirc):
                patch = dirc
    return patch
        
def upload(sources: List[str]):
    print("running upload_pantry.py")
    files_path={}
    for source in sources:
        for root, dirs, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                files_path[file]=file_path
                
    packet = conditionner(files_path)
    
    # for division,data in packet.items():
    #     delete_file(division)
    #     send_file(division,data,False)
        
    # with open('Data/changes.json',"r",encoding='utf-8') as changes:
    #     data = json.load(changes)
    #     delete_file('Changes')
    #     send_file('Changes',data,False)
    
    print("Done")

if __name__=="__main__" or __name__ == "upload_pantry":
    upload([f"Data/{getPatch()}/data/en_GB/champion"])