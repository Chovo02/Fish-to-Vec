from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry_convert as pc
from statistics import mode
from statistics import mean
from tqdm import tqdm

def get_soup(url:str) -> BeautifulSoup:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ConnectionRefusedError("Connection refused")
    return BeautifulSoup(response.content, "lxml", from_encoding=response.encoding)

def country_to_continent(country:str) -> str:
    country = country.replace("\n", "").split(",")
    
    if country[0] == "":
        return None
    if "Europe" in country:
        country.remove("Europe")
        if len(country) == 0:
            return "EU"
    continent = []
    for c in country:
        if c[-1] == " ":
            c = c[:-1]
        if c == "Hawaii":
            c = "United States of America"
        if c == "Palau Island":
            c = "New Zealand"  
        if c[:len(c)//2] == c[len(c)//2:]:
            c = c[:len(c)//2]
        country_code = pc.country_name_to_country_alpha3(c, cn_name_format="default")
        continent.append(pc.country_alpha2_to_continent_code(pc.country_alpha3_to_country_alpha2(country_code)))
        if mode(continent) == "NA":
            return "NAM"
    return mode(continent)

def min_max_converter(min_max:str) -> str:
    if min_max == "":
        return None
    min_max_result = min_max.replace(" ", "").replace("to", "-").split("-")
    try:
        mean_list = [float(x) for x in min_max_result]
    except ValueError:
        return None
    return round(mean(mean_list), 2)    

def get_fish_data() -> pd.DataFrame:

    df = pd.DataFrame(columns=[ "Common Name",
                                "Link",
                                "Scientific Name",
                                "Classification",
                                "Order",
                                "Family",
                                "Temperament",
                                "Level",
                                "Diet",
                                "PH",
                                "GH",
                                "Temp",
                                "Size",
                                "Continent"])
    
    soup = get_soup("https://aquadiction.world/species-spotlight/")
    cards = soup.find_all("div", class_="card-body")
    for card, i in zip(cards, tqdm(range(len(cards)))):
        if card.find("a", class_="btn btn-view-profile wait"):
            link = "https://aquadiction.world" + card.find("a", class_="btn btn-view-profile wait")["href"]
        else:
            continue

        fish_page = get_soup(link)
        tables = fish_page.find_all("table", class_="table table-hover caption-top")
        table_fact = tables[0]
        try:
            scientific_name = table_fact.find("td", headers="scientific-Name").text 
            classification = table_fact.find("td", headers="classification").text
            order = table_fact.find("td", headers="order").text
            family = table_fact.find("td", headers="family").text
            origins = table_fact.find("td",  headers="origins").text
            if origins == None or origins == "" or origins == "\n":
                continue
            temperament = table_fact.find("td", headers="temperament").text
            level = table_fact.find("td", headers="aquarium-level").text
            diet = table_fact.find("td", headers="Feeding").text
        except AttributeError:
            continue
        
        table_param = tables[1]
        try:
            ph = table_param.find("td", headers="PH").text
            gh = table_param.find("td", headers="gh").text
        except AttributeError:
            continue
        
        table_temp = tables[2]
        try:
            temp = table_temp.find("td", headers="temp-c").text
        except AttributeError:
            continue
        
        try:
            size = fish_page.find("div", class_="species-profile-inner-container rounded box-shadow").text
        except AttributeError:
            continue

        scientific_name = scientific_name.replace("\n", "").replace(" ", "").replace("\r", "").split(",")[0]
        classification = classification.replace("\n", "").replace(" ", "").replace("\r", "").split(",")[0]
        order = order.replace("\n", "").replace(" ", "").replace("\r", "").split(",")[0]
        family = family.replace("\n", "").replace(" ", "").replace("\r", "").split(",")[0]

        mean_ph = min_max_converter(ph)
        mean_gh = min_max_converter(gh)
        
        if temp == '':
            try:
                temp = table_temp.find("td", headers="temp-f").text
            except AttributeError:
                continue
            mean_temp = min_max_converter(temp)
            mean_temp = round((float(mean_temp) - 32) / 1.8, 1)
        else:
            mean_temp = min_max_converter(temp)

        if mean_ph == None or mean_gh == None or mean_temp == None:
            continue

        numeric_size = ''.join(c for c in size if c.isdigit() or c == "." or c == "-")
        if "-" in numeric_size: 
            numeric_size = min_max_converter(numeric_size)
        
        continent = country_to_continent(origins)
        
        df = pd.concat([df, pd.DataFrame({"Common Name": [card.h2.text], 
                                        "Link": [link], 
                                        "Scientific Name": [scientific_name],
                                        "Classification": [classification],
                                        "Order": [order],
                                        "Family": [family],
                                        "Temperament": [temperament],
                                        "Level": [level],
                                        "Diet": [diet],
                                        "PH": [float(mean_ph)],
                                        "GH": [float(mean_gh)],
                                        "Temp": [float(mean_temp)],
                                        "Size": [float(numeric_size)],
                                        "Continent": [continent]})])

    return df