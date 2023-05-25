Il modulo per la modellazione serve per importare il DataFrame usato prima e fare alcune operazioni per renderlo utilizzabile per una rappresentazione su uno scatter plot a tre o duo dimensioni.

##### Importazione del DataFrame
La prima funzione importa il DataFrame dalla funsione `get_fish_data()` vista prima.

```python
def importing_dataset(check_local:bool = True) -> pd.DataFrame:
    if os.path.exists("data/Fish_to_Vec.csv") and check_local:
        return pd.read_csv("data/Fish_to_Vec.csv")
    else:
        df = web.get_fish_data()
        df.to_csv("data/Fish_to_Vec.csv", index=False)
    return pd.read_csv("data/Fish_to_Vec.csv")
```

Come si vede per prima cosa controlliamo se e' presente una versione locale del DataFrame in formato  `.csv` se presente leggiamo direttamete quella al posto di crealrla ogni volta oprerazione questo varra' applicata per tutti i DataFrame che vedremo successivamente per velocizzare il programma.

##### Embedding del DataFrame
Come detto nella sezione sugli algoritmi usati ([[Algoritmi usati]]) gli embedding servono per rappresentare un qualcosa come una parola che un computer che non capoisce in qualcosa che capisce molto meglio: numeri. 

```python
def embedding_dataset(df:pd.DataFrame, check_local:bool=True) -> pd.DataFrame:
	if os.path.exists("data/Fish_to_Vec_Embedding.csv") and check_local:
		return pd.read_csv("data/Fish_to_Vec_Embedding.csv")
	df = df.drop(["Common Name", "Link", "Scientific Name"], axis=1)
```

Tramite la funzione `drop()` di Pandas eliminiamo le colonne che non ci interessano. Per dare dei valori alle colonne piu' semplici come "Classification", "Order" e "Family" useremo la funzione `enumerate()` sui valori che compaiono solo una volta nella colonna.

```python
for column in ["Classification", "Order", "Family"]:
	for i, classification in enumerate(df[column].unique()):
		df.loc[df[column] == classification, column] = i + 1
```

Per colonne dove avere un valore piu' simile ad un altro a piu' senso bisogna fare la stessa cosa ma al posto di avere solo i valori univoci saranno anche ordinati.

```python
for i, temperament in enumerate(["Peaceful", "Semi-Aggressive", "Aggressive"]):
	df.loc[df["Temperament"] == temperament, "Temperament"] = i + 1
  
for i, level in enumerate(["Bottom", "Bottom - Middle", "Middle", 
						   "Middle - Top", "Top", "All Levels"]):
        df.loc[df["Level"] == level, "Level"] = i + 1
for i, diet in enumerate(["Carnivore", "Omnivore",  "Herbivore"]):
	df.loc[df["Diet"] == diet, "Diet"] = i + 1
df.loc[df["Diet"] == "Molluscivore", "Diet"] = 1

for i, continent in enumerate(["NAM", "SA", "EU", "AF", "AS", "OC"]):
	df.loc[df["Continent"] == continent, "Continent"] = i + 1
```

In fine creiamo il file in formato `.csv` e ritorniamo il DataFrame.

##### Normalizzazione del DataFrame
Quando abbiamo un DataFrame con colonne che sono distribuite con scale e unita' di misure diverse potrebbe influenzare la comparibilita' dei valori. La normalizzazione si effettua trasformando i valori in un range comune, solitamente tra 0 e 1 o -1 e 1. Uno dei modi piu' sempilici e quello della normalizzazione per la media.

```python
def normalized_dataset(df:pd.DataFrame, check_local:bool = True) -> pd.DataFrame:
	if os.path.exists("data/Fish_to_Vec_Normalized.csv") and check_local:
		return pd.read_csv("data/Fish_to_Vec_Normalized.csv")
	else:
		normalizer_dataset = df.apply(lambda x: (x-x.mean())/ x.std(), axis=0)
		normalizer_dataset.to_csv("data/Fish_to_Vec_Normalized.csv",
		index=False)
		return normalizer_dataset
```

##### Riduzione di dimesionalita' del DataFrame
Per poter visualizzare i nostri pesci dobbiamo ridurre le dimensioni da 11 dimensioni a 3 o 2. Il metodo piu' veloce e comune e' quello della PCA spiegato nelle sezioni differenti, ma una caratteristica della PCA e' quella di essere lineare e come possiamo vedere nell'immagine sotto i nostri valori snon hanno una grossa correlazione non e' possibile usarla.

![[Correlation_Matrix.png]]

Quindi possiamo usare la T-distributed Stochastic Neighbor Embedding (T-SNE) che e' un algoritmo di ridusione delle dimensionalita' non lineare.

```python
def tsne_dataset(normalized_embedding_dataset:pd.DataFrame,
				 final_dataset:pd.DataFrame,
				 dimension:int = 3,
				 check_local:bool = True) -> pd.DataFrame:
              
	if os.path.exists(f"data/Fish_to_Vec_TSNE_{dimension}D.csv") and check_local:
		return pd.read_csv(f"data/Fish_to_Vec_TSNE_{dimension}D.csv")
  
	if dimension != 2 and dimension != 3:
		raise ValueError("Le dimensioni possono essere 2 o 3")
  
	tsne = TSNE(n_components=dimension, random_state=47)
	dataset_tsne = tsne.fit_transform(normalized_embedding_dataset)
	for i, axis in enumerate(['X', 'Y', 'Z']):
		if i > dimension:
			break
		final_dataset[axis] = dataset_tsne[:, i-1]
  
	final_dataset.to_csv(f"data/Fish_to_Vec_TSNE_{dimension}D.csv", index=False)
	return final_dataset
```

Per prima cosa dobbiamo creare il nostro oggetto TSNE per poi fittarlo nel nostro DataFrame. Una volta fatto cio' creiamo delle nuove nuove colonne nel DataFrame che abbiamo creato nel modulo di webscraping perche' li ci sono le informazioni complete e saranno quelle usate nel nostro grafico.

##### Calco dei punti piu' vicine nel DataFrame
Come ultima informazione voglio sapere quali sono i pesci pesci piu' vicini per ogni pesce quindi useremo il Unsupervised Nearest Neighbors (NN) che e' un algoritmo di machine learning non supervisionato per calcolare i punti piu' vicini per ogni punto.

```python
def neighbors_dataset(df, n_neighbors:int = 5, 
					  dimension:int = 3, 
					  check_local:bool = True) -> pd.DataFrame:
					  
	n_neighbors = n_neighbors + 1
	if os.path.exists(
	f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv") and check_local:
		return pd.read_csv(
		f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv")
  
	if dimension != 2 and dimension != 3:
		raise ValueError("Le dimensioni possono essere 2 o 3")
  
	knn = NearestNeighbors(n_neighbors=n_neighbors)
	if dimension == 3:
		knn.fit(df[['X', 'Y', 'Z']])
		distances, indices = knn.kneighbors(df[['X', 'Y', 'Z']])
	else:
		knn.fit(df[['X', 'Y']])
		distances, indices = knn.kneighbors(df[['X', 'Y']])
  
	distances = np.delete(distances, 0, axis=1)
	indices = np.delete(indices, 0, axis=1)
  
	for column_index in range(indices.shape[1]):
		value = [(df["Common Name"][x], round(y, 3)) 
		for x, y in zip(indices[:, column_index], distances[:, column_index])]
		df[f"Nearest Neighbors {column_index+1}"] = value
	df.to_csv(
	f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv", index=False)
	return df
```


Un problema di questo algoritmo e' che come elemento piu' vicino calcolalcola anche il punto stesso quindi dobbiamo trovare un punto in piu' rispetto a quello che verra messo quando usiamo la funzione. La funzione `kneighnbors()` restituisce due matrici uno per le distanze e l'altra degli indici del DataFrame per avere al posto di avere il numero reovo il Nome comune nella posizione dell'indice.

Adesso che ho un le coodinate di ogni pesce possiamo passare alla parte di visualizzazione.
[[Visualizzazione del DataFrame]]