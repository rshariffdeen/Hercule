from bs4 import BeautifulSoup
import requests
import csv
import ssl
from typing import Any

ssl._create_default_https_context = ssl._create_unverified_context

package_list = ["pandas", "numpy", "beautifulsoup", "scipy", "matplotlib",
                "requests", "tensorflow", "pytorch", "beautifulsoup4", "six",
                "scrapy", "pyqt", "sympy", "dateutils", "urllib3", "setuptools"]

def write_as_csv(data: Any, output_file_path: str):
    with open(output_file_path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        for output in data:
            writer.writerow(output)


def get_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="iso-8859-1")
    return soup


def get_distributor_list(html_soup, package_name):
    result_table = html_soup.find("table")
    list_distro = result_table.find_all("tr")
    filtered_distro = []
    for distro in list_distro:
        dist_pkg_name = distro.find("strong")
        if not dist_pkg_name:
            continue
        dist_pkg_name = dist_pkg_name.text.lower()
        if dist_pkg_name and package_name == dist_pkg_name:
            distro_web_url = "https://anaconda.org" + distro.find_all("a")[1]["href"]
            filtered_distro.append(distro_web_url)
    return filtered_distro


def get_distro_info(html_soup):
    home_page = html_soup.find("li", title="Home Page")
    source_page = html_soup.find("li", title="Development Url")
    no_downloads = html_soup.find("li", title="Download Count")
    last_updated = html_soup.find("li", title="Last upload")
    info = {
        "home-page": "",
        "source-page": "",
        "download-count": "",
        "last-updated": ""
            }
    if home_page:
        info["home-page"] = home_page.text.strip().replace("\n", "")
    if source_page:
        info["source-page"] = source_page.text.strip().replace("\n", "")
    if no_downloads:
        info["download-count"] = no_downloads.text.strip().replace("\n", "")
    if last_updated:
        info["last-updated"] = last_updated.text.strip().replace("\n", "")
    return info


def get_download_links(html_soup, package_name):
    download_list = []
    file_table = html_soup.find("table")
    if file_table:
        download_item_list = file_table.find_all("tr")[1:] # skip head row
        for item in download_item_list:
            link_info = item.find_all('a')[1]
            download_link = f"https://anaconda.org/{link_info['href']}"
            print(link_info.text)
            file_name = link_info.text.replace("/", "-")
            if "/" in link_info.text:
                os_version, package_full_name = link_info.text.split("/")
            else:
                os_version = ""
                package_full_name = link_info.text
            package_version = package_full_name.replace(package_name + "-","").split("-")[0]
            python_version = package_full_name.replace(package_name + "-","").split("-")[-1]
            info = {
                "download-link": download_link,
                "package-version": package_version,
                "python-version": python_version,
                "os-version": os_version,
                "file-name": file_name
            }
            download_list.append(info)

    next_page = html_soup.find("li", class_="arrow ")
    if next_page:
        next_page_url = f"https://anaconda.org/{next_page['href']}"
        next_page_soup = get_html(next_page_url)
        next_download_list = get_download_links(next_page_soup, package_name)
        download_list = download_list + next_download_list
    return download_list


def run():
    global package_list
    output_content = []
    output_file_path = "anaconda.csv"
    for package_name in package_list:
        search_url = f"https://anaconda.org/search?q={package_name}&sort=ndownloads&reverse=true"
        print(f"querying for {package_name} in {search_url}")
        html_soup = get_html(search_url)
        url_list = get_distributor_list(html_soup, package_name)
        print(f"found {len(url_list)} distributors")
        output_content.append((
            "package-name",
            "distribution_url",
            "home-page",
            "source-page",
            "download-count",
            "last-updated",
            "package-version",
            "os-version",
            "python-version",
            "download-link",
            "file-name"
        ))
        for distro_web_url in url_list:
            print(f"extracting info from {distro_web_url}")
            profile_soup = get_html(distro_web_url)
            distro_info = get_distro_info(profile_soup)
            print(distro_info)
            file_page_url = f"{distro_web_url}/files"
            download_soup = get_html(file_page_url)
            download_list = get_download_links(download_soup, package_name)
            print(f"found {len(download_list)} downloads")
            for download_info in download_list:
                info = (
                    package_name,
                    distro_web_url,
                    distro_info["home-page"],
                    distro_info["source-page"],
                    distro_info["download-count"],
                    distro_info["last-updated"],
                    download_info["package-version"],
                    download_info["os-version"],
                    download_info["python-version"],
                    download_info["download-link"],
                    download_info["file-name"]
                )
                output_content.append(info)
        break

    if output_content:
        write_as_csv(output_content, output_file_path)


if __name__ == "__main__":
    run()
