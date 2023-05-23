import plotly.express as px
import pandas as pd

def plot(df:pd.DataFrame, dimension:int = 3, color:str = "Order") -> None:
    if dimension != 2 and dimension != 3:
        raise ValueError("Le dimensioni possono essere 2 o 3")
    
    if dimension == 3:
        fig = px.scatter_3d(df, x='X', y='Y', z='Z', color=color, hover_name="Common Name", category_orders={color: sorted(df[color].unique())},
                            hover_data={'X':  False, 
                                    'Y': False, 
                                    'Z': False,
                                    "Continent": True,
                                    "Classification": True,
                                    "Order": True,
                                    "Family": True,
                                    "Temperament":  True,
                                    "Level": True,
                                    "Diet": True,
                                    "PH": True,    
                                    "GH": True,
                                    "Temp": True,
                                    "Size": True,
                                    "Nearest Neighbors 1": True,
                                    "Nearest Neighbors 2": True,
                                    "Nearest Neighbors 3": True,
                                    "Nearest Neighbors 4": True,
                                    "Nearest Neighbors 5": True,
                                    }, range_x=[-20,20], range_y=[-20, 20], range_z=[-20, 20])
        fig.update_layout(scene=dict(aspectmode='cube'))
    else:
        fig = px.scatter(df, x='X', y='Y', color=color, hover_name="Common Name", category_orders={color: sorted(df[color].unique())},
                         hover_data={'X':  False, 
                                    'Y': False, 
                                    'Z': False,
                                    "Continent": True,
                                    "Classification": True,
                                    "Order": True,
                                    "Family": True,
                                    "Temperament":  True,
                                    "Level": True,
                                    "Diet": True,
                                    "PH": True,    
                                    "GH": True,
                                    "Temp": True,
                                    "Size": True,
                                    "Nearest Neighbors 1": True,
                                    "Nearest Neighbors 2": True,
                                    "Nearest Neighbors 3": True,
                                    "Nearest Neighbors 4": True,
                                    "Nearest Neighbors 5": True,
                                    })

    fig.show()