pysyge
======
http://github.com/idlesign/pysyge

.. image:: https://badge.fury.io/py/pysyge.png
    :target: http://badge.fury.io/py/pysyge

.. image:: https://pypip.in/d/pysyge/badge.png
        :target: https://crate.io/packages/pysyge



What's that
-----------

*pysyge is an API to access data from Sypex Geo IP database files from your Python code.*

For more information about Sypex Geo databases and their features please visit http://sypexgeo.net.

Direct DB links that might became broken over time:

  * Sypex Geo City DB - http://sypexgeo.net/files/SxGeoCity_utf8.zip

  * Sypex Geo City Max DB - http://sypexgeo.net/files/SxGeoCityMax_utf8.zip



Requirements
------------

Python 2.7+, 3.2+



Attention
---------

1. This version of pysyge works with **Sypex Geo DB version 2.2 or above**.

  The structure of a dictionary returned by GeoLocator.get_location() was preserved in a backward compatible manner
  as much as possible, yet it's advised to update your code to use data from `info` sub dictionary.

2. This version of pysyge works with **UTF-8** Sypex Geo Databases. Texts returned by pysyge are **UTF-8**.



Quickstart
----------

Download Geo IP database file from http://sypexgeo.net/ (example below uses `SxGeoCityMax.dat` file).

Application sample::

    # Import all we need from pysyge module.
    from pysyge.pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY

    # Create GeoLocator object to access API from 'SxGeoCityMax.dat' using fast memory mode.
    geodata = GeoLocator('SxGeoCityMax.dat', MODE_BATCH | MODE_MEMORY)

    # Let's get some meta information.
    print('DB version %s (%s)' % (geodata.get_db_version(), geodata.get_db_date()))

    # Request geo information for 77.88.21.3 IP address. Getting detailed information, including region info.
    location = geodata.get_location('77.88.21.3', detailed=True)

    # Print out some lyrics. Most interesting data is under `info` in `city`, `country` and `region` dictionaries
    print('%s (%s) calling. All the circuits are busy.' % (location['info]['city']['name_en'], location['info']['country']['iso']))

