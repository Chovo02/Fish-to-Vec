import plotly.express as px
import dataset_manipulation_aquadiction as dm

df = dm.neighbors_dataset(5)
fig = px.scatter_3d(df, x='X', y='Y', z='Z', color="Order",
                    hover_data={'X':  False, 
                             'Y': False, 
                             'Z': False,
                             "Continent": False,
                             "Common Name": True,
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
                             "Nearest Neighbors 5": True
                             })

fig.show()
