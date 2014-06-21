# -*- coding: utf-8 -*-
from pysyge import pysyge
import unittest
import datetime


# DATABASE_CITY_FILE = 'SxGeo.dat'  # от 2014.06.04
# DATABASE_CITY_FILE = 'SxGeoCity.dat'  # от 2014.06.04
DATABASE_CITY_FILE = 'db/SxGeoCityMax.dat'  # от 2014.06.04
BASE_IP = '77.88.21.3'


class GeoLocatorBasicCheck(unittest.TestCase):

    def test_file_not_found(self):
        self.assertRaises(IOError, pysyge.GeoLocator, 'nosuchfile.dat')

    def test_wrong_file(self):
        self.assertRaises(pysyge.GeoLocatorException, pysyge.GeoLocator, 'tests/runtests.py')

    def test_db_version(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        self.assertGreaterEqual(geodata.get_db_version(), 21)

    def test_db_date(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        self.assertIsInstance(geodata.get_db_date(), datetime.datetime)

    def test_localhost(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        self.assertEqual(geodata.get_location('127.0.0.1'), False)


class GeoLocatorFileModeCheck(unittest.TestCase):

    def test_location_basic(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)

        location = geodata.get_location(BASE_IP)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertNotIn('region', location)
        self.assertNotIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 0)

    def test_location_detailed(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)

        location = geodata.get_location(BASE_IP, detailed=True)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertIn('region', location)
        self.assertIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 524894)

        self.assertEqual(location['region'], u'Москва')
        self.assertEqual(location['tz'], 'Europe/Moscow')


class GeoLocatorMemoryModeCheck(unittest.TestCase):

    def test_location_basic(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, pysyge.MODE_MEMORY)

        location = geodata.get_location(BASE_IP)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertNotIn('region', location)
        self.assertNotIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 0)

    def test_location_detailed(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, pysyge.MODE_MEMORY)

        location = geodata.get_location(BASE_IP, detailed=True)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertIn('region', location)
        self.assertIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 524894)

        self.assertEqual(location['region'], u'Москва')
        self.assertEqual(location['tz'], 'Europe/Moscow')


class GeoLocatorBatchModeCheck(unittest.TestCase):

    def test_location_basic(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, pysyge.MODE_BATCH)

        location = geodata.get_location(BASE_IP)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertNotIn('region', location)
        self.assertNotIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 0)

    def test_location_detailed(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, pysyge.MODE_BATCH)

        location = geodata.get_location(BASE_IP, detailed=True)
        self.assertIn('city', location)
        self.assertIn('country_id', location)
        self.assertIn('country_iso', location)
        self.assertIn('lon', location)
        self.assertIn('lat', location)
        self.assertIn('fips', location)
        self.assertIn('region_id', location)

        self.assertIn('region', location)
        self.assertIn('tz', location)

        self.assertEqual(location['city'], u'Москва')
        self.assertEqual(location['country_id'], 185)
        self.assertEqual(location['country_iso'], 'RU')
        self.assertEqual(location['lon'], 37.61556)
        self.assertEqual(location['lat'], 55.75222)
        self.assertEqual(location['fips'], '0')
        self.assertEqual(location['region_id'], 524894)

        self.assertEqual(location['region'], u'Москва')
        self.assertEqual(location['tz'], 'Europe/Moscow')


if __name__ == '__main__':
    unittest.main()
