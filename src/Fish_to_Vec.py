import Fish_to_Vec_dataset_manipulation as dm
import Fish_to_Vec_visualization as viz
import pandas as pd

class Fish_to_Vec:
    def __init__(self, check_local:bool = True, dimension:int = 3, n_neighbors:int = 5) -> None:
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
        return self._embedding
    
    @property
    def normalized(self):
        return self.__normalized
    
    @property
    def TSNE(self):
        return self.__TSNE
    
    @property
    def neighbors(self):
        return self.__neighbors

    def plot(self, color:str = "Order") -> None:
        viz.plot(self.__neighbors, self.__dimension, color)

    def search_by_common_name(self, common_name) -> pd.DataFrame:
        fish = self.__neighbors[self.__neighbors["Common Name"] == common_name]
        if fish.empty:
            raise ValueError(f"Il pesce {common_name} non esiste.")
        return fish
    
    def difference_dataset_by_name(self, common_name) -> None:
        idx = self.search_by_common_name(common_name).index[0]
        return_df = pd.DataFrame()
        for df in [self.__dataset, self.__embedding, self.__normalized, self.__TSNE, self.__neighbors]:
            return_df = pd.concat([return_df, df.iloc[[idx]]], )
        
        return_df.to_csv(f"data/fishs/{common_name}.csv", index=False)