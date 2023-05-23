# Fish-to-Vec
L'idea di Fish to Vec è quella di creare un modello simile a Word to Vec ma al posto di usare le parole e il contesto vengo usati i pesci e alcuni valori per poi visualizzarli come su https://projector.tensorflow.org/ dove ogni punto rappresenta un pesce e la distanza fra due punti quanto i due pesci si assomigliano.

I dati li prendo da il sito https://aquadiction.world/ dove sono presenti molti dati di tanti pesci usati nel modo dell'acquariologia.

Il mio dataset sarà formato da questi valori:
|Common Name              |Link                                         |Scientific Name      |Classification|Order        |Family        |Temperament|Level          |Diet    |PH |GH  |Temp |Size|Continent|
|-------------------------|---------------------------------------------|---------------------|--------------|-------------|--------------|-----------|---------------|--------|---|----|-----|----|---------|
|Adolfos Catfish          |/species-spotlight/adolfos-catfish/          |Corydorasadolfoi     |Actinopterygii|Siluriformes |Callichthyidae|Peaceful   |Bottom         |Omnivore|6.0|11.0|22.5 |6.0 |SA       |
|Adonis Tetra             |/species-spotlight/adonis-tetra/             |Lepidarchusadonis    |Actinopterygii|Characiformes|Alestidae     |Peaceful   |Middle - Top   |Omnivore|6.5|7.0 |23.9 |2.1 |AF       |
|African Banded Barb      |/species-spotlight/african-banded-barb/      |Barbusfasciolatus    |Actinopterygii|Cypriniformes|Cyprinidae    |Peaceful   |Middle - Top   |Omnivore|6.5|8.5 |23.9 |6.0 |AF       |
|African Butterfly Cichlid|/species-spotlight/african-butterfly-cichlid/|Anomalochromisthomasi|Actinopterygii|Cichliformes |Cichlidae     |Peaceful   |Bottom - Middle|Omnivore|6.5|7.5 |24.75|8.0 |AF       |
|African Glass Catfish    |/species-spotlight/african-glass-catfish/    |Pareutropiusdebauwi  |Actinopterygii|Siluriformes |Schilbeidae   |Peaceful   |Bottom - Middle|Omnivore|7.0|10.0|25.3 |10.0|AF       |

Per maggiori informazione guardare la documentazione nella cartella Fish to Vec