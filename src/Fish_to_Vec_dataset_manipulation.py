import Fish_to_Vec_webscraping as web
from sklearn.manifold import TSNE
import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def importing_dataset(check_local:bool = True) -> pd.DataFrame:
    '''This function imports a dataset from a local file or from the web and returns it as a pandas
    DataFrame.
    
    Parameters
    ----------
    check_local : bool, optional
        A boolean parameter that determines whether to check for a local copy of the dataset or not. If set
    to True, the function will check if a local copy of the dataset exists and return it if it does. If
    set to False, the function will always download the dataset from the web.
    
    Returns
    -------
        The function `importing_dataset` returns a pandas DataFrame containing fish data. If the file
    "data/Fish_to_Vec.csv" exists locally and `check_local` is True, the function reads the file and
    returns the DataFrame. Otherwise, the function calls the `get_fish_data` function from the `web`
    module to retrieve the data, saves it to the file "data/Fish
    
    '''
    if os.path.exists("data/Fish_to_Vec.csv") and check_local:
        return pd.read_csv("data/Fish_to_Vec.csv")
    else:
        df = web.get_fish_data()
        df.to_csv("data/Fish_to_Vec.csv", index=False)
    return pd.read_csv("data/Fish_to_Vec.csv")


def embedding_dataset(df:pd.DataFrame, check_local:bool=True) -> pd.DataFrame:
    '''This function takes a pandas DataFrame of fish data and converts categorical variables into
    numerical embeddings, returning the updated DataFrame or loading a cached version if available.
    
    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing information about fish species.
    check_local : bool, optional
        A boolean parameter that determines whether to check for a local file containing the embedding
    dataset or not. If set to True, the function will check for a local file and return its contents if
    it exists. If set to False, the function will always generate a new embedding dataset. The default
    value is True
    
    Returns
    -------
        a pandas DataFrame.
    
    '''

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
    '''This function normalizes a given pandas DataFrame and saves it to a CSV file or loads it from a
    local file if it exists.
    
    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing the dataset to be normalized.
    check_local : bool, optional
        A boolean parameter that indicates whether to check if a local file "Fish_to_Vec_Normalized.csv"
    exists before computing the normalized dataset. If set to True and the file exists, the function
    will return the contents of the file instead of recomputing the normalized dataset.
    
    Returns
    -------
        a pandas DataFrame that contains the normalized dataset. If the normalized dataset has been
    previously saved in a CSV file and the `check_local` parameter is set to `True`, the function reads
    the CSV file and returns the DataFrame. Otherwise, the function normalizes the input DataFrame and
    saves it to a CSV file before returning it.
    
    '''
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
    '''The function performs t-SNE dimensionality reduction on a normalized embedding dataset and adds the
    resulting coordinates to a final dataset, which is then saved to a CSV file.
    
    Parameters
    ----------
    normalized_embedding_dataset : pd.DataFrame
        A pandas DataFrame containing the normalized embedding dataset.
    final_dataset : pd.DataFrame
        A pandas DataFrame that contains the original dataset to which the t-SNE embedding will be added as
    new columns.
    dimension : int, optional
        The dimension parameter specifies the number of dimensions for the t-SNE algorithm to reduce the
    data to. It can be either 2 or 3.
    check_local : bool, optional
        A boolean parameter that indicates whether to check if a local file with the same name as the
    output file already exists. If it does, the function will return the contents of the local file
    instead of running the t-SNE algorithm again.
    
    Returns
    -------
        A pandas DataFrame containing the original dataset with additional columns for the t-SNE
    coordinates in 2D or 3D. If the function finds a previously saved file with the same t-SNE
    dimension, it returns the saved DataFrame instead of recomputing the t-SNE.
    
    '''
    
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
    '''This function takes a dataframe of coordinates and finds the nearest neighbors for each point,
    returning a new dataframe with the added nearest neighbor information.
    
    Parameters
    ----------
    df
        A pandas DataFrame containing the data to be used for finding nearest neighbors
    n_neighbors : int, optional
        The number of nearest neighbors to find for each data point in the dataset.
    dimension : int, optional
        The dimension parameter specifies the number of dimensions in the dataset. It can be either 2 or 3.
    check_local : bool, optional
        A boolean parameter that determines whether to check if a local file with the same name as the
    output file already exists. If it does, the function returns the contents of the local file instead
    of recomputing the nearest neighbors.
    
    Returns
    -------
        A pandas DataFrame containing the original data with additional columns indicating the nearest
    neighbors of each data point, based on the specified number of neighbors and dimensions. If a local
    file with the same parameters exists, the function returns that file instead of recomputing the
    neighbors.
    
    '''
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
