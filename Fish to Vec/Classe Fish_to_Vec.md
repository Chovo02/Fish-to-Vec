Per rendere piu' facile l'utilizzo ho creato una classe che rappresenti `Fish_to_Vec`.
Quando viene creato un oggetto `Fish_to_Vec` vengono passati 3 valori:
- il controllo dei file in locale,
- Le dimensioni se 2 o 3,
- Il numero dei punti vicini.
Nella creazione dell'oggetto vengono creati dei attributi privati che rappresentano i 5 passaggi del DataFrame:
- Il primo dell'acquisizione dei dati (`dataset`),
- Il secondo dove sono presenti gli embedding (`embedding`),
- Il terzo e' il secondo DataFrame ma normalizzato (`normalized`),
- Il quarto e' dove sono presenti le coordinate date dalla TSNE (`TSNE`),
- L'ultimo e' dove sono presenti anche i punti piu' vicini ed e' quello che viene usato per la visualizzazione (`neighbors`)

```python
def __init__(self, check_local = True, dimension = 3, n_neighbors = 5) -> None:
	self.__check_local = check_local
	self.__dimension = dimension
	self.__n_neighbors = n_neighbors
	self.__dataset = dm.importing_dataset(check_local)
	self.__embedding = dm.embedding_dataset(self.__dataset, check_local)
	self.__normalized = dm.normalized_dataset(self.__embedding, check_local)
	self.__TSNE = dm.tsne_dataset(self.__normalized, self.__dataset, self.__dimension,
							      self.__check_local)
	self.__neighbors = dm.neighbors_dataset(self.__TSNE, self.__n_neighbors,
										    self.__dimension, self.__check_local)
```

```python 
@property
def embedding(self):
	return self._embedding
```

Ho usato il decoratore `@property` per poter richiamare un getter quando proviamo ad accedere ad un attributo della classe.

##### Le Funzioni della classe
La prima funzione serve a creare il grafico usando la funzione vista in precedenza.

```python
def plot(self, color = "Order"):
	viz.plot(self.__neighbors, self.__dimension, color)
```

La seconda funzione ti permette di ritornare tutte le informazioni di un determinato pesce dato il nome comune.

```python
def search_by_common_name(self, common_name):
	fish = self.__neighbors[self.__neighbors["Common Name"] == common_name]
	if fish.empty:
		raise ValueError(f"Il pesce {common_name} non esiste.")
	return fish
```

La terza funzione ti permette di creare un file `.csv` dove ogni riga corrisponde alla riga di ogni DataFrame dato sempre il nome comune di un pesce.

```python
def difference_dataset_by_name(self, common_name):
	idx = self.search_by_common_name(common_name).index[0]
	return_df = pd.DataFrame()
	for df in [self.__dataset, self.__embedding, self.__normalized, self.__TSNE,
			   self.__neighbors]:
		return_df = pd.concat([return_df, df.iloc[[idx]]], )
	return_df.to_csv(f"data/fishs/{common_name}.csv", index=False)
```

Ho usato la funzione vista prima per avere l'indice del pesce. L'indice e' lo stesso per tutti i DataFrame perché si basano sullo stesso.
