pysyge
======
http://github.com/idlesign/pysyge

.. image:: https://idlesign.github.io/lbc/py2-lbc.svg
   :target: https://idlesign.github.io/lbc/
   :alt: LBC Python 2

----

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/pysyge.svg
    :target: https://pypi.python.org/pypi/pysyge

.. |lic| image:: https://img.shields.io/pypi/l/pysyge.svg
    :target: https://pypi.python.org/pypi/pysyge

.. |ci| image:: https://img.shields.io/travis/idlesign/pysyge/master.svg
    :target: https://travis-ci.org/idlesign/pysyge

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/pysyge/master.svg
    :target: https://coveralls.io/r/idlesign/pysyge



What's that
-----------

*pysyge is an API to access data from Sypex Geo IP database files from your Python code.*

For more information about Sypex Geo databases and their features please visit http://sypexgeo.net.

Direct DB link that might became broken over time:

  * Sypex Geo City DB - http://sypexgeo.net/files/SxGeoCity_utf8.zip



Requirements
------------

* Python 3.6+



Attention
---------

1. This version of pysyge works with **Sypex Geo DB version 2.2 or above**.

  The structure of a dictionary returned by GeoLocator.get_location() was preserved in a backward compatible manner
  as much as possible, yet it's advised to update your code to use data from `info` sub dictionary.

2. This version of pysyge works with **UTF-8** Sypex Geo Databases. Texts returned by pysyge are **UTF-8**.



Quickstart
----------

Download Geo IP database file from http://sypexgeo.net/ (example below uses ``SxGeoCityMax.dat`` file).

Application sample

.. code-block:: python

    # Import all we need from pysyge module.
    from pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY

    # Create GeoLocator object to access API
    # from 'SxGeoCityMax.dat' using fast memory mode.
    geodata = GeoLocator('SxGeoCityMax.dat', MODE_BATCH | MODE_MEMORY)

    # Let's get some meta information.
    print('DB version %s (%s)' % (geodata.get_db_version(), geodata.get_db_date()))

    # Request geo information for 77.88.21.3 IP address.
    # Getting detailed information, including region info.
    location = geodata.get_location('77.88.21.3', detailed=True)

    # Print out some lyrics.
    # Most interesting data is under `info` in `city`, `country` and `region` dictionaries
    print('%s (%s) calling. All the circuits are busy.' % (
        location['info']['city']['name_en'], location['info']['country']['iso']))

