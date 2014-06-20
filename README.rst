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



Attention
---------

**This version of pysyge works with Sypex Geo DB version 2.2 or above.**



Quickstart
----------

Download Geo IP database file from http://sypexgeo.net/ (example below uses `SxGeoCityMax.dat` file).

Application sample::

    # Import all we need from pysyge module.
    from pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY

    # Create GeoLocator object to access API from 'SxGeoCity.dat' using fast memory mode.
    geodata = GeoLocator('SxGeoCityMax.dat', MODE_BATCH | MODE_MEMORY)

    # Request geo information for 77.88.21.3 IP address.
    location = geodata.get_location('77.88.21.3', detailed=True)

    # Print out some lyrics.
    print('%s (%s) calling. All the circuits are busy.' % (location['details]['city']['name_en'], location['details']['country']['iso']))

