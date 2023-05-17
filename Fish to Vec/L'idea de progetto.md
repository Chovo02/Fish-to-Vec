L'idea di Fish to Vec è quella di creare un modello simile a Word to Vec ma al posto di usare le parole e il contesto vengo usati i pesci e alcuni valori per poi visualizzarli come su https://projector.tensorflow.org/ dove ogni punto rappresenta un pesce e la distanza fra due punti quanto i due pesci si assomigliano.

## Word to Vec ##
Word to Vec è un insieme di modelli utilizzati per produrre word embedding. Il word embedding è un modo per rappresentare delle parole tramite dei vettori. Uno dei metodi più semplici è quello di creare un vettore di dimensione pari al numero di parole presenti nel dataset dove 1 corrisponde alla parola. Questo metodo è chiamato One-Hot encoding.  
|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 
|:-----|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|------:| 
| Uomo | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 
| Donna | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  
| Ragazzo | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 
| Ragazza | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 
| Principe | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 
| Principessa | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 
| Regina | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 
| Re | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 
| Monarca | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 

Non ho scelto questo modello perchè non ti permette di considerare il contesto, nel caso di Fish to Vec i vari valori. Quindi ho optato per un modello personalizzato dove ogni valore corrisponde ad uno dei miei valori.
|  | Femminilità | Giovane | Reale |
|:-----|:--------:|:--------:|------:| 
| Uomo | 0 | 0 | 0 |
| Donna | 1 | 0 | 0 |
| Ragazzo | 0 | 1 | 0 |
| Ragazza | 1 | 1 | 0 | 
| Principe | 0 | 1 | 1 | 
| Principessa | 1 | 0 | 1 | 
| Regina | 1 | 1 | 1 |
| Re | 0 | 0 | 1 | 
| Monarca | 0.5 | 0.5 | 1 | 

## PCA (Analisi delle coponenti principali)
