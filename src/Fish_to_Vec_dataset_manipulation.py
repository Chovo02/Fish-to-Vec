import Fish_to_Vec_webscraping as web
from sklearn.manifold import TSNE
import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def importing_dataset(check_local:bool =True) -> pd.DataFrame:
    if os.path.exists("data/Fish_to_Vec.csv") and check_local:
        return pd.read_csv("data/Fish_to_Vec.csv")
    else:
        df = web.get_fish_data()
        df.to_csv("data/Fish_to_Vec.csv", index=False)
    return pd.read_csv("data/Fish_to_Vec.csv")


def embedding_dataset(df:pd.DataFrame, check_local:bool=True) -> pd.DataFrame:
    if os.path.exists("data/Fish_to_Vec_Embedding.csv") and check_local:
        return pd.read_csv("data/Fish_to_Vec_Embedding.csv")
    df = df.drop(["Common Name", "Link", "Scientific Name"], axis=1)

    for column in ["Classification", "Order", "Family"]:
        for i, classification in enumerate(df[column].unique()):
            df.loc[df[column] == classification, column] = i + 1

    for i, temperament in enumerate(["Peaceful", "Semi-Aggressive", "Aggressive"]):
        df.loc[df["Temperament"] == temperament, "Temperament"] = i + 1

    for i, level in enumerate(["Bottom", "Bottom - Middle", "Middle", "Middle - Top", "Top", "All Levels"]):
        df.loc[df["Level"] == level, "Level"] = i + 1

    for i, diet in enumerate(["Carnivore", "Omnivore",  "Herbivore"]):
        df.loc[df["Diet"] == diet, "Diet"] = i + 1
    df.loc[df["Diet"] == "Molluscivore", "Diet"] = 1

    for i, continent in enumerate(["NAM", "SA", "EU", "AF", "AS", "OC"]):
        df.loc[df["Continent"] == continent, "Continent"] = i + 1

    df.to_csv("data/Fish_to_Vec_Embedding.csv", index=False)
    return df

def normalized_dataset(df:pd.DataFrame, check_local:bool = True) -> pd.DataFrame:
    if os.path.exists("data/Fish_to_Vec_Normalized.csv") and check_local:
        return pd.read_csv("data/Fish_to_Vec_Normalized.csv")
    else:
        normalizer_dataset = df.apply(lambda x: (x-x.mean()) / x.std(), axis=0)
        normalizer_dataset.to_csv(
            "data/Fish_to_Vec_Normalized.csv", index=False)
        return normalizer_dataset
    

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


def neighbors_dataset(df, n_neighbors:int = 5, dimension:int = 3, check_local:bool = True) -> pd.DataFrame:
    n_neighbors = n_neighbors + 1
    if os.path.exists(f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv") and check_local:
        return pd.read_csv(f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv")

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
        value = [(df["Common Name"][x], round(y, 3)) for x, y in zip(indices[:, column_index], distances[:, column_index])]
        df[f"Nearest Neighbors {column_index+1}"] = value
    df.to_csv(f"data/Fish_to_Vec_Neighbors_{n_neighbors-1}_{dimension}D.csv", index=False)
    return df
