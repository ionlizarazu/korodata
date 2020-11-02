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
    >>> Korodata.azkenEguneraketa()
    ...
    >>>
    >>> Korodata.herria('Herri izena')
    ...
    >>>
    >>> Korodata.zerrenda()

Funtzioen azalpena
------------------

azkenEguneraketa()
~~~~~~~~~~~~~~~~~

Publikatuta dagoen JSON fitxategiaren azken eguneraketa itzultzen du.

herria('Herri izena')
~~~~~~~~~~~~~~~~~~~~~

Eskatzen zaion herriaren azken 25 egunetako positibo bilakaera duen grafika bat gordetzen du 'grafikak' deituriko karpetan

zerrenda()
~~~~~~~~~~

Azken egunean 2 positibo edo gehiago izan duten herri guztien grafika bana gordetzen du 'grafikak' deituriko karpetan, azken 25 egunetako datuekin.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
