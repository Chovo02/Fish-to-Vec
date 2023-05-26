import Fish_to_Vec_dataset_manipulation as dm
import Fish_to_Vec_visualization as viz
import pandas as pd
import os


class Fish_to_Vec:
    def __init__(self, check_local:bool = True, dimension:int = 3, n_neighbors:int = 5) -> None:
        '''This is the initialization function for a class that imports, embeds, normalizes, and performs
        t-SNE and nearest neighbor analysis on a dataset.
        
        Parameters
        ----------
        check_local : bool, optional
            A boolean value indicating whether the dataset is stored locally or needs to be downloaded from
        a remote source.
        dimension : int, optional
            The dimension parameter specifies the number of dimensions in which the dataset will be
        embedded using t-SNE algorithm. By default, it is set to 3, which means that the dataset will be
        embedded in a 3-dimensional space.
        n_neighbors : int, optional
            n_neighbors is an integer parameter that specifies the number of neighbors to consider when
        performing nearest neighbor search in the dataset. It is used in the dm.neighbors_dataset()
        function to find the nearest neighbors of each point in the dataset.
        
        '''
        if dimension != 2 and dimension != 3:
            raise ValueError("Dimension can only be 2 or 3")
        
        if not os.path.exists("data"):
            os.mkdir("data")

        self.__check_local = check_local
        self.__dimension = dimension
        self.__n_neighbors = n_neighbors
        self.__dataset = dm.importing_dataset(check_local)
        self.__embedding = dm.embedding_dataset(self.__dataset, check_local)
        self.__normalized = dm.normalized_dataset(self.__embedding, check_local)
        self.__TSNE = dm.tsne_dataset(self.__normalized, self.__dataset, self.__dimension, self.__check_local)
        self.__neighbors = dm.neighbors_dataset(self.__TSNE, self.__n_neighbors, self.__dimension, self.__check_local)

    @property
    def embedding(self):
        '''This function returns the embedding attribute of an object.
        
        Returns
        -------
            The method `embedding` is being defined as returning the private attribute `_embedding`.
        
        '''
        return self._embedding
    
    @property
    def normalized(self):
        '''This function returns the value of the private attribute "__normalized".
        
        Returns
        -------
            The method `normalized` is being defined as a method of a class, and it returns the private
        attribute `__normalized`.
        
        '''
        return self.__normalized
    
    @property
    def TSNE(self):
        '''The function returns the value of the private variable "__TSNE".
        
        Returns
        -------
            The method `TSNE` is being defined to return the private attribute `__TSNE`.
        
        '''
        return self.__TSNE
    
    @property
    def neighbors(self):
        '''This function returns the neighbors of an object.
        
        Returns
        -------
            The method `neighbors` is returning the private attribute `__neighbors`.
        
        '''
        return self.__neighbors

    def plot(self, color:str = "Order") -> None:
        '''This function plots the neighbors of an object in a specified color.
        
        Parameters
        ----------
        color : str, optional
            The color parameter is a string that specifies the color scheme to be used for the plot. The
        default value is "Order", which means that the points will be colored based on their order in
        the dataset.
        
        '''
        viz.plot(self.__neighbors, self.__dimension, color, self.__n_neighbors)

    def search_by_common_name(self, common_name:str) -> pd.DataFrame:
        '''This function searches for a fish by its common name in a pandas DataFrame and returns the
        matching rows.
        
        Parameters
        ----------
        common_name
            The common name of a fish that the user wants to search for in the dataset.
        
        Returns
        -------
            a pandas DataFrame containing information about fish species that have a common name matching
        the input parameter `common_name`. If no matches are found, a `ValueError` is raised with a
        message indicating that the fish species does not exist.
        
        '''
        fish = self.__neighbors[self.__neighbors["Common Name"] == common_name]
        if fish.empty:
            raise ValueError(f"The fish {common_name} do not exist.")
        return fish
    
    def difference_dataset_by_name(self, common_name:str) -> None:
        '''This function takes a common name as input and returns a concatenated dataframe of various
        datasets related to that name, which is then saved as a CSV file.
        
        Parameters
        ----------
        common_name
            The common name of a fish species.
        
        '''

        if not os.path.exists("data/fish"):
            os.mkdir("data/fish")

        idx = self.search_by_common_name(common_name).index[0]
        return_df = pd.DataFrame()
        for df in [self.__dataset, self.__embedding, self.__normalized, self.__TSNE, self.__neighbors]:
            return_df = pd.concat([return_df, df.iloc[[idx]]], )
        
        return_df.to_csv(f"data/fish/{common_name}.csv", index=False)