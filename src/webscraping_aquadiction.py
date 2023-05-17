from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry_convert as pc
from statistics import mode
from statistics import mean
from tqdm import tqdm

def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionRefusedError("Connection refused")
    return BeautifulSoup(response.content, "lxml", from_encoding=response.encoding)

def country_to_continent(country):
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
    return mode(continent)

def min_max_converter(min_max):
    if min_max == "":
        return None, None
    min_max_result = min_max.replace(" ", "").replace("to", "-").split("-")
    mean_list = [float(x) for x in min_max_result] 
    return round(mean(mean_list), 2)    

def get_fish_data():

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
        name = card.h2.text
        if name == "Jaintia Danio":
            continue
        if card.find("a", class_="text-muted").text in [" Snail", " Caridina", "Other Shrimp", " Prawns", " Neocaridina"]:
            continue
        if card.find("a", class_="btn btn-view-profile wait"):
            link =[card.find("a", class_="btn btn-view-profile wait")["href"]]
        else:
            continue

        fish_page = get_soup("https://aquadiction.world" + link[0])
        tables = fish_page.find_all("table", class_="table table-hover caption-top")
        table_fact = tables[0]
        try:
            scientific_name = table_fact.find("td", headers="scientific-Name").text.replace("\n", "").replace(" ", "").replace("\r", "") 
            classification = table_fact.find("td", headers="classification").text.replace("\n", "").replace(" ", "").replace("\r", "")
            order = table_fact.find("td", headers="order").text.replace("\n", "").replace(" ", "").replace("\r", "")
            family = table_fact.find("td", headers="family").text.replace("\n", "").replace(" ", "").replace("\r", "")
            origins = table_fact.find("td",  headers="origins").text
            if origins == None or origins == "" or origins == "\n":
                continue
            temperament = table_fact.find("td", headers="temperament").text
            level = table_fact.find("td", headers="aquarium-level").text
            diet = table_fact.find("td", headers="Feeding").text
        except AttributeError:
            continue
        
        table_param = tables[1]
        ph = table_param.find("td", headers="PH").text
        gh = table_param.find("td", headers="gh").text

        table_temp = tables[2]
        temp = table_temp.find("td", headers="temp-c").text

        if temp == '':
            temp = table_temp.find("td", headers="temp-f").text
            mean_temp = min_max_converter(temp)
            mean_temp = round((float(mean_temp) - 32) / 1.8, 1)
        else:
            mean_temp = min_max_converter(temp)
        size = fish_page.find("div", class_="species-profile-inner-container rounded box-shadow").find("div", class_=None).text
        numeric_size = ''.join(c for c in size if c.isdigit() or c == "." or c == "-")
        if "-" in numeric_size: 
            numeric_size = numeric_size.split("-")[0]
        continent = country_to_continent(origins)
        if continent == "NA":
            continent = "NAM"

        mean_ph = min_max_converter(ph)
        mean_gh = min_max_converter(gh)
        
        df = pd.concat([df, pd.DataFrame({"Common Name": name, 
                                        "Link": link, 
                                        "Scientific Name": scientific_name,
                                        "Classification": classification,
                                        "Order": order,
                                        "Family": family,
                                        "Temperament": temperament,
                                        "Level": level,
                                        "Diet": diet,
                                        "PH": float(mean_ph),
                                        "GH": float(mean_gh),
                                        "Temp": float(mean_temp),
                                        "Size": float(numeric_size),
                                        "Continent": continent})])

    return df