import requests
from bs4 import BeautifulSoup
from scholarly import ProxyGenerator, scholarly
import requests
from typing import Optional
import re
import PyPDF2
from pathlib import Path
import csv
import ssl
import os
import sys

ssl._create_default_https_context = ssl._create_unverified_context

def read_csv(file_path: str):
    csv_data = []
    if os.path.isfile(file_path):
        with open(file_path, newline="") as csv_file:
            content = csv.DictReader(csv_file)
            for r in content:
                csv_data.append(r)
    return csv_data

def download_file(file_url, file_path):
    response = requests.get(file_url)
    if os.path.isfile(file_path):
        print("duplicate file found", file_path)
    dir_path = os.path.dirname(file_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return


def run(arg_list):
    if not arg_list:
        print("please provide file path to meta-data")
        exit(1)
    meta_data_file = arg_list[0]
    if not os.path.isfile(meta_data_file):
        print("meta data file not found at", meta_data_file)
    meta_data = read_csv(meta_data_file)
    count = 0
    total_downloads = len(meta_data)
    for d in meta_data:
        count = count + 1
        pkg_name = d["package-name"]
        download_url = d["download-link"]
        download_name = d["file-name"]
        distro_url = d["distribution_url"]
        distro_name = distro_url.split("/")[-2]
        download_path = f"downloads/{pkg_name}/{distro_name}-{download_name}"
        print(f"download #{count} of #{total_downloads}")
        print(f"downloading {download_name} from {download_url}")
        download_file(download_url, download_path)

if __name__ == "__main__":
    run(sys.argv[1:])
