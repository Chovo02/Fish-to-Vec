Per visualizzare i pesci ho utilizzato lo scatter plot a 2 o 3 dimensioni perchè riesce a far rappresentare ogni pesce nel piano in modo distinto. Nel modulo e' presente solo una funzione per tutti e due i tipo di grafici.

```python
if dimension != 2 and dimension != 3:
	raise ValueError("Le dimensioni possono essere 2 o 3")
if dimension == 3:

	fig = px.scatter_3d(df, x='X', y='Y', z='Z', color=color, 
	hover_name="Common Name", category_orders={color: sorted(df[color].unique())},
						hover_data={'X':  False,
								'Y': False,
								'Z': False,
								"Continent": True,
								"Classification": True,
								"Order": True,
								"Family": True,
								"Temperament":  True,
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
								}, range_x=[-20,20], range_y=[-20, 20], 
								range_z=[-20, 20])

	fig.update_layout(scene=dict(aspectmode='cube'))
```

In questo caso sto creando uno scatter plot a 3 dimensioni. `hover_data` e' un attributo che corrisponde alle informazioni che vengono visualizzano se si passa sopra ad un punto del grafico.

![[Hover Data.png]]

Per rendere tutto piu' compatto e dover importare meno moduli possibili ho creato una classe che racchiude tutti i moduli precedenti. [[Classe Fish_to_Vec]]