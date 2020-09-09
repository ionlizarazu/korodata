# korodata-python
EAEko herriz herriko Koronabirus datuak kontsultatzeko tresna

## Nola erabili:
### **1.** Ingurune birtuala sortu
Deskargatu kode hau eta sortu [virtualenv](https://virtualenv.pypa.io/en/latest/) bat
karpetan bertan, horrela zure sistemako python ingurunea ez duzu kakaztuko.
```bash
    $ python3 -m venv myvenv
```

### **2.** Beharrezko paketeak instalatu
```bash
    $ ./myvenv/bin/pip install -r requirements.txt
```

### **3.** Python ingurunea abiatu eta Korodata inportatu
```bash
    $ ./myvenv/bin/python3
    ...
    >>> from korodata import Korodata
    >>> 
```
### **4.** Interesatzen zaiguna exekutatu
```bash
    >>>
    >>> Korodata.azkenEguneraketa()
    ...
    >>> 
    >>> Korodata.herria('Herri izena')
    ...
    >>>
    >>> Korodata.zerrenda()
    ...
    >>> 
```

## Funtzioak:
### azkenEguneraketa()
Publikatuta dagoen JSON fitxategiaren azken eguneraketa itzultzen du.
### herria('Herri izena')
Eskatzen zaion herriaren azken 25 egunetako positibo bilakaera duen grafika bat gordetzen du 'grafikak' deituriko karpetan
### zerrenda()
Azken egunean 2 positibo edo gehiago izan duten herri guztien grafika bana gordetzen du 'grafikak' deituriko karpetan, azken 25 egunetako datuekin.


