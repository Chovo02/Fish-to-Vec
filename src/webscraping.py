from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionRefusedError("Connection refused")
    return BeautifulSoup(response.content, "lxml", from_encoding=response.encoding)


def get_max_page(soup):
    page = soup.find_all("div", {"class": "slide"})[-1]["onclick"].split(
        "(")[1].replace("'", "").split(",")[0].split("=")
    return page[0]+"=", int(page[1])


def get_fish_dataframe():

    df = pd.DataFrame(columns=["Name", "Min Temp", "Min Gh", "Min Ph", "Max Temp", "Max Gh", "Max Ph"])
    link_list = []
    name_list = []
    element_list = []
    soup = get_soup("https://www.mare2000.it/Indici/pescidolce.php?id=1")
    prefix, max_page = get_max_page(soup)
    for page in range(1, max_page):
        soup = get_soup(f"https://www.mare2000.it/Indici/{prefix}{page}")
        element_list += soup.find_all("div", {"class": "cel"})

    print(f"Found {len(element_list)} fish")
    for element in element_list:
        name_list.append(element.text)
        link_list.append(element["onclick"].split(
            "(")[1].replace(")", "").replace("'", ""))

    for name, link in zip(name_list, link_list):
        time.sleep(0.5)
        if "Poecilia Reticulata<br>Varietà Golden Sunset" in link:
            continue
        soup = get_soup(f"https://www.mare2000.it/{link[2:]}")

        temp = soup.find_all("div", {"class": "ts5"})[2].text.replace(
            "\xc2\xb0", "").split("C")[0].replace("°", "").replace(" ", "").split("/")
        gh = soup.find_all("div", {"class": "ts5"})[2].text.replace("\xc2\xb0", "").split(
            "C")[1].split("dGh")[0].replace("°", "") .replace(" ", "").split("/")
        ph = soup.find_all("div", {"class": "ts5"})[2].text.replace(
            "\xc2\xb0", "").split("C")[1].split("dGh")[1].replace(" ", "").split("/")
        min_temp = ''.join(
            c for c in temp[0] if c.isdigit() or c == ",").replace(",", ".")
        min_gh = ''.join(
            c for c in gh[0] if c.isdigit() or c == ",").replace(",", ".")
        min_ph = ''.join(
            c for c in ph[0] if c.isdigit() or c == ",").replace(",", ".")
        max_temp = temp[1].replace(",", ".")
        max_gh = gh[1].replace(",", ".")
        max_ph = ph[1].replace(",", ".")

        if soup.find_all("div", {"class": "ts5"})[1].text == None or soup.find_all("div", {"class": "ts5"})[1].text == "":
            min_dim = 999
            max_dim = 999
        else:
            if "cm" in soup.find_all("div", {"class": "ts5"})[1].text.replace("\xc2\xb0", "").replace(" ", ""):
                dim = soup.find_all("div", {"class": "ts5"})[1].text.replace(
                    "\xc2\xb0", "").replace(" ", "").split("cm")[1].split("/")
            else:
                dim = soup.find_all("div", {"class": "ts5"})[1].text.replace(
                    "\xc2\xb0", "").replace(" ", "").split("mm")[1].split("/")
            if len(dim) == 2:
                min_dim = ''.join(
                    c for c in dim[0] if c.isdigit() or c == ",").replace(",", ".")
                max_dim = ''.join(
                    c for c in dim[1] if c.isdigit() or c == ",").replace(",", ".")
            else:
                min_dim = ''.join(
                    c for c in dim[0] if c.isdigit() or c == ",").replace(",", ".")
                max_dim = min_dim

        if max_dim == '':
            max_dim = 999

        if min_dim == '':
            min_dim = 999

        behavior = soup.find("div", {"class": "spi"})
        if behavior.contents[1]["class"][1] == "ang":
            behavior = 0
        elif behavior.contents[1]["class"][1] == "dia":
            behavior = 0.5
        else:
            behavior = 2

        df = pd.concat([df, pd.DataFrame({"Name": [name],
                                          "Min Temp": [float(min_temp)],
                                          "Min Gh": [float(min_gh)],
                                          "Min Ph": [float(min_ph)],
                                          "Max Temp": [float(max_temp)],
                                          "Max Gh": [float(max_gh)],
                                          "Max Ph": [float(max_ph)],
                                          "Min Dim": [float(min_dim)],
                                          "Max Dim": [float(max_dim)],
                                          "Behavior": [float(behavior)]})])
        print(f"Added {name}")
    return df