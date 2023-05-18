from sklearn.manifold import TSNE
import webscraping_aquadiction as wa
import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

def importing_dataset():
    if os.path.exists("data/fish_data_aquadiction.csv"):
        df = pd.read_csv("data/fish_data_aquadiction.csv")
    else:
        df = wa.get_fish_data()
        df.to_csv("data/fish_data_aquadiction.csv", index=False)
    return df


def normalizer_dataset(df):
    if os.path.exists("data/fish_data_aquadiction_normalizer.csv"):
        return pd.read_csv("data/fish_data_aquadiction_normalizer.csv")
    else:
        normalizer_dataset = pd.DataFrame()
        for column in df.columns:
            print(column)
            mean = df[column].mean()
            std = df[column].std()
            normalizer_dataset[column] = (df[column] - mean) / std
        normalizer_dataset.to_csv(
            "data/fish_data_aquadiction_normalizer.csv", index=False)
        return normalizer_dataset


def embedding_dataset():
    df = importing_dataset()
    if os.path.exists("data/fish_data_aquadiction_embedded.csv"):
        return pd.read_csv("data/fish_data_aquadiction_embedded.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)
    df = df.drop(["Common Name", "Link", "Scientific Name"], axis=1)

    for i, classification in enumerate(df["Classification"].unique()):
        df.loc[df["Classification"] == classification, "Classification"] = i + 1
    
    for i, order in enumerate(df["Order"].unique()):
        df.loc[df["Order"] == order, "Order"] = i + 1
    
    for i, family in enumerate(df["Family"].unique()):
        df.loc[df["Family"] == family, "Family"] = i + 1
    
    for i, temperament in enumerate(["Peaceful", "Semi-Aggressive", "Aggressive"]):
        df.loc[df["Temperament"] == temperament, "Temperament"] = i + 1

    for i, level in enumerate(["Bottom", "Bottom - Middle", "Middle", "Middle - Top", "Top", "All Levels"]):
        df.loc[df["Level"] == level, "Level"] = i + 1
    
    for i, diet in enumerate(["Carnivore", "Omnivore",  "Herbivore"]):
        df.loc[df["Diet"] == diet, "Diet"] = i + 1
    df.loc[df["Diet"] == "Molluscivore", "Diet"] = 1

    for i, continent in enumerate(["NAM", "SA", "EU", "AF", "AS", "OC"]):
        df.loc[df["Continent"] == continent, "Continent"] = i + 1

    df.to_csv("data/fish_data_aquadiction_embedded.csv", index=False)
    df = normalizer_dataset(df)
    return df

def tsne_dataset():
    if os.path.exists("data/fish_data_aquadiction_tsne.csv"):
        return pd.read_csv("data/fish_data_aquadiction_tsne.csv")
    df = embedding_dataset()
    tsne = TSNE(n_components=3, random_state=20)
    dataset_tsne = tsne.fit_transform(df)
    graph_df = importing_dataset()
    graph_df["X"] = dataset_tsne[:, 0]
    graph_df["Y"] = dataset_tsne[:, 1]
    graph_df["Z"] = dataset_tsne[:, 2]
    graph_df.to_csv("data/fish_data_aquadiction_tsne.csv", index=False)
    return graph_df

def neighbors_dataset(n_neighbors):
    if os.path.exists(f"data/fish_data_aquadiction_neighbors{n_neighbors}.csv"):
        return pd.read_csv(f"data/fish_data_aquadiction_neighbors{n_neighbors}.csv")
    n_neighbors = n_neighbors + 1
    df = tsne_dataset()

    from sklearn.model_selection import train_test_split
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(df[['X', 'Y', 'Z']])
    distances, indices = knn.kneighbors(df[['X', 'Y', 'Z']])

    indices = np.delete(indices, 0, axis=1)
    for column_index in range(indices.shape[1]):
        value = [df["Common Name"][x] for x in indices[:, column_index]]
        df[f"Nearest Neighbors {column_index+1}"] = value
    df.to_csv(f"data/fish_data_aquadiction_neighbors{n_neighbors-1}.csv", index=False)
    return df