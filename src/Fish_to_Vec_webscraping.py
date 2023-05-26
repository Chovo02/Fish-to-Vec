from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry_convert as pc
from statistics import mode
from statistics import mean
from tqdm import tqdm

def get_soup(url:str) -> BeautifulSoup:
    '''This function takes a URL as input, sends a GET request with headers to the URL, checks if the
    response status code is 200, and returns a BeautifulSoup object with the response content.
    
    Parameters
    ----------
    url : str
        The URL of the webpage that we want to scrape.
    
    Returns
    -------
        The function `get_soup` returns a `BeautifulSoup` object, which is created by parsing the HTML
    content of a webpage obtained from the given URL using the `requests` library and the `lxml` parser.
    The function also sets a user agent header in the request to avoid being blocked by the website. If
    the response status code is not 200, a `ConnectionRefusedError`
    
    '''

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ConnectionRefusedError("Connection refused")
    return BeautifulSoup(response.content, "lxml", from_encoding=response.encoding)

def country_to_continent(country:str) -> (str | None):
    '''This function takes a string representing a country name, removes any unnecessary characters, maps
    the country to its continent, and returns the continent code or None if the input is invalid.
    
    Parameters
    ----------
    country : str
        The input parameter is a string representing a country or a list of countries separated by commas.
    
    Returns
    -------
        a string representing the continent(s) that the given country belongs to. It can return "EU" for
    Europe, "NAM" for North America, or a string representing the continent code (e.g. "AS" for Asia) if
    the country belongs to a single continent. If the country name is invalid or cannot be mapped to a
    continent, the function returns None.
    
    '''

    country = country.replace("\n", "").split(",")
    
    if country[0] == "":
        return None
    
    continent = []
    for c in country:
        if c[-1] == " ":
            c = c[:-1]
        if c[0] == " ":
            c = c[1:]
        if c != "Europe":
            try:
                country_code = pc.country_name_to_country_alpha3(c, cn_name_format="default")
                continent.append(pc.country_alpha2_to_continent_code(pc.country_alpha3_to_country_alpha2(country_code)))
            except KeyError:
                return None
        else: continent.append("EU")
        if mode(continent) == "NA":
            return "NAM"
    return mode(continent)

def min_max_converter(min_max:str) -> (float | None):
    '''The function takes a string input representing a range of values and returns the average of the
    minimum and maximum values in the range, or None if the input is invalid.
    
    Parameters
    ----------
    min_max : str
        The input parameter `min_max` is a string representing a range of values separated by the word "to"
    or a hyphen. For example, "10 to 20" or "10-20". The function `min_max_converter` converts this
    string into a tuple of two floats representing the
    
    Returns
    -------
        a float value rounded to two decimal places or None if the input string is empty or cannot be
    converted to a list of floats.
    
    '''

    if min_max == "":
        return None
    min_max_result = min_max.replace(" ", "").replace("to", "-").split("-")
    try:
        mean_list = [float(x) for x in min_max_result]
    except ValueError:
        return None
    return round(mean(mean_list), 2)    

def get_fish_data() -> pd.DataFrame:
    '''This function scrapes data from a website about different fish species and returns a pandas
    dataframe with information such as their common name, scientific name, classification, temperament,
    diet, and environmental requirements.
    
    Returns
    -------
        A pandas DataFrame containing information about various fish species, including their common name,
    scientific name, classification, order, family, temperament, level, diet, pH, GH, temperature, size,
    and continent.
    
    '''

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

        if continent == None:
            continue
        
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