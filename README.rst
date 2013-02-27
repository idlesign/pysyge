pysyge
======
http://github.com/idlesign/pysyge


What's that
-----------

*pysyge is an API to access data from Sypex Geo IP database files from your Python code.*

For more information about Sypex Geo databases and their features please visit http://sypexgeo.net.


Quickstart
----------

Download Geo IP database file from http://sypexgeo.net/ (example below uses `SxGeoCity.dat` file).

Application sample::

    # Import all we need from pysyge module.
    from pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY

    # Create GeoLocator object to access API from 'SxGeoCity.dat' using fast memory mode.
    geodata = GeoLocator('SxGeoCity.dat', MODE_BATCH | MODE_MEMORY)

    # Request geo information for 77.88.21.3 IP address.
    location = geodata.get_location('77.88.21.3', detailed=True)

    # Print out some lyrics.
    print('%s (%s) calling. All the circuits are busy.' % (location['city'], location['country_iso']))

