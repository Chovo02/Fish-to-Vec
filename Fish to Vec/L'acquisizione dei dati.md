Per l'acquisizione dei dati prenderò i dati da https://aquadiction.world/species-spotlight/ dov'è presente una tabella di pesci che cliccandoci sopra porta ad un altro sito (es. https://aquadiction.world/species-spotlight/adolfos-catfish/) dov'è presente una scheda tecnica del pesce. 
La funzione principale di questo modulo e' `get_fish_data()` dove e' contenuta la maggior parte del codice. In questa funzione la prima cosa che viene fatta è quella di creare un DataFrame grazie a pandas.

```python
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
```

Successivamente prendiamo l'oggetto BeautifulSoup che e' un oggetto che rappresenta il codice sorgente di un sito e ci permette di navigarlo in modo veloce. Ho creato una funzione visto che verra' usata piu' volte.

```python
soup = get_soup("https://aquadiction.world/species-spotlight/")
cards = soup.find_all("div", class_="card-body")
```

```python
def get_soup(url:str) -> BeautifulSoup:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ConnectionRefusedError("Connection refused")
    return BeautifulSoup(response.content, "lxml", from_encoding=response.encoding)
```

Grazie questo oggetto possiamo cercare tutte gli elementi div con classe card-body che rappresenta le carte dove è presente un tag a con classe btn btn-view-profile wait che contiene il link delle schede tecniche e da lì usando la stessa funzione di prima predo l'oggetto BeautifulSoup e trovo tutte le tabelle con classe table table-hover caption-top.

```python
fish_page = get_soup(link)
tables = fish_page.find_all("table", class_="table table-hover caption-top")
```

Facendo così prendiamo le tre tabelle che ci interessano che sono 3:
- La tabella delle informazioni principali;
- La tabella dei parametri dell'acqua;
- E la tabella delle temperature dell'acqua.

![[Tabella Info.png]]

Visto che che a volte le informazioni risultano mancanti estrarremo le informazioni in un            
`try except AttributeError:`  e nel caso ci fosse un errore `AttributeError` saltiamo il pesce, questo perchè ci sarebbe un informazione nulla che non possiamo riempire

```python
table_fact = tables[0]
try:
	scientific_name = table_fact.find("td", headers="scientific-Name").text
	classification = table_fact.find("td", headers="classification").text
	order = table_fact.find("td", headers="order").text
	family = table_fact.find("td", headers="family").text
	origins = table_fact.find("td",  headers="origins").text
	if origins == None or origins == "" or origins == "\n":
	    continue
	temperament = table_fact.find("td", headers="temperament").text
	level = table_fact.find("td", headers="aquarium-level").text
	diet = table_fact.find("td", headers="Feeding").text
except AttributeError:
	continue
```

Questo lo facciamo per tutte e tre le tabelle.
Una volta presi i dati dal sito dobbiamo pulirli o modificarli:

##### Nome scientifico, classificazione, ordine, famiglia
Queste 4 variabili sono molto simili fra di loro quindi verranno pulite nello stesso modo:

```python
family = family.replace("\n", "").replace(" ", "").replace("\r", "").split(",")[0]
```

##### PH, GH
Invece questi due valori sono scritti in questo modo: `valore_minimo - valore massimo` anche se a volte vengono anche `valore_minimo to valore massimo`. Per non ripetere il mio codice ho creato una funzione.

```python
def min_max_converter(min_max:str) -> str:
	if min_max == "":
		return None
	min_max_result = min_max.replace(" ", "").replace("to", "-").split("-")
	try:
		mean_list = [float(x) for x in min_max_result]
	except ValueError:
		return None
	return round(mean(mean_list), 2)
```

##### Temperatura
Per la temperatura seguiamo la stessa funzione di prima ma questa volta abbiamo due possibili unità di misura: celsius e fahrenheit. Quindi se il celsius non esiste lo faremo con fahrenheit facendo poi la converssione.

```python
if temp == '':
	try:
		temp = table_temp.find("td", headers="temp-f").text
	except AttributeError:
		continue
	mean_temp = min_max_converter(temp)
	mean_temp = round((float(mean_temp) - 32) / 1.8, 1)
else:
	mean_temp = min_max_converter(temp)
```

Visto che sia il pH , GH e temperatura possono restituire None se dovesse succeedere escludiamo il pesce. 

##### Dimensione
Per la dimesione sono andato a selezionare essendo che ci potrebbero essere dei caratteri li ho esclusi controllando tutti i caratteri della sezione dove si trova l'iformazione 

```python
numeric_size = ''.join(c for c in size if c.isdigit() or c == "." or c == "-")
	if "-" in numeric_size:
		numeric_size = min_max_converter(numeric_size)
```

##### Continente
Ho scelto il continente al posto del paese perche' siccome un pesce puo' provenire da piu' nazione ho deciso di convertirli in continente e trovare il continente piu' frequente fra tutti.

```python
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
		country_code = pc.country_name_to_country_alpha3(c, cn_name_format="default"
		continent.append(pc.country_alpha2_to_continent_code(
						 pc.country_alpha3_to_country_alpha2(country_code)))
        if mode(continent) == "NA":
            return "NAM"
    return mode(continent)
```

Per fare cio' ho usato una libreria chaimata pycoutry_converter dove prima converto il paese in un codice che rappresenta il continente. Una volta fatto questo lo converto nel nome del continente.

Tutte queste informazioni quindi andranno nel mio DataFrame usando la punzione `concat()` di pandas che serve per unire due o più DataFrame insieme lungo un asse specificato in caso non sia specificato viene fatto per righe.

```python
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
```

Alla fine della funzione ritorniamo il DataFrame per poi matipolarlo ne modulo successivo.

[[Modellazione del DataFrame]]