========
Korodata
========


.. image:: https://img.shields.io/pypi/v/korodata.svg
        :target: https://pypi.python.org/pypi/korodata

.. image:: https://img.shields.io/travis/ionlizarazu/korodata.svg
        :target: https://travis-ci.com/ionlizarazu/korodata

.. image:: https://readthedocs.org/projects/korodata/badge/?version=latest
        :target: https://korodata.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


EAEko herriz herriko Koronabirus datuak kontsultatzeko tresna


* Free software: GNU General Public License v3


Erabilera eta instalazioa
-------------------------

Instalatu paketea pip erabiliz:

    $ pip install korodata

Erabiltzeko inportatu paketea eta deitu metodoei:

    >>> from korodata import Korodata
    >>> Korodata.azken_eguneraketa()
    ...
    >>>
    >>> fitxategia, herri_izena = Korodata.herria('Antzuola', 60)
    ...
    >>>
    >>> fitxategia = Korodata.probintzia('01', 60)
    ...
    >>>
    >>> fitxategia = Korodata.eae(60)


Funtzioen azalpena
------------------

azken_eguneraketa()
~~~~~~~~~~~~~~~~~

Publikatuta dagoen JSON fitxategiaren azken eguneraketa itzultzen du.

herria(herri_izena, zenbat_egun)
~~~~~~~~~~~~~~~~~~~~~

Bi parametro hartzen ditu, herriaren izena eta zenbat egun.
Egun kopurua pasa ezean azken 60 egunetako datuak itzuliko ditu. 
Eskatzen zaion herriaren azken egunetako positibo bilakaera duen grafika bat eta herriaren izena itzultzen ditu.

probintzia(kodea, zenbat_egun)
~~~~~~~~~~~~~~~~~~~~~

Bi parametro hartzen ditu, probintziaren kodea eta zenbat egun.
Probintzia kodeak hauek dira: 
  - '01' - Araba
  - '48' - Bizkaia
  - '20' - Gipuzkoa
Egun kopurua pasa ezean azken 60 egunetako datuak itzuliko ditu. 
Eskatzen zaion probintziaren azken egunetako positibo bilakaera duen grafika bat itzultzen du.

eae(zenbat_egun)
~~~~~~~~~~~~~~~~~~~~~

Parametro bakarra hartzen du, zenbat egun.
Egun kopurua pasa ezean azken 60 egunetako datuak itzuliko ditu. 
Euskal Autonomia Erkidegoko azken egunetako positibo bilakaera duen grafika bat itzultzen du.

gorriak(muga)
~~~~~~~~~~~~~~~~~~~~~

Parametro bakarra hartzen du, muga deiturikoa.
Intzidentzia metatuaren muga zein izan nahi den aukeratu eta hortik gora daukaten herrien zerrenda itzultzen du, bakoitzaren informazioarekin. 


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
