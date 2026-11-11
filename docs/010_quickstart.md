# Quickstart

Download Geo IP database file from <https://sypexgeo.net/> (example below uses `SxGeoCityMax.dat` file).

Application sample:

```python
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
```
