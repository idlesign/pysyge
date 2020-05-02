import datetime
from os import path

import pytest

from pysyge import pysyge

DIR_CURRENT = path.dirname(__file__)
DATABASE_CITY_FILE = path.join(DIR_CURRENT, 'SxGeoCity.dat')  # 2019-11-19
BASE_IP = '77.88.55.80'  # Yandex


def test_quirks():
    geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, pysyge.MODE_MEMORY)
    result = geodata.get_location('49.206.213.75', detailed=True)
    assert result['city'] == 'Хайдарабад'
    assert result['country_iso'] == 'IN'
    assert result['tz'] == ''
    assert result['info']['country']['name_en'] == 'India'


class TestGeoLocatorBasicCheck:

    def test_file_not_found(self):

        with pytest.raises(IOError):
            pysyge.GeoLocator('nosuchfile.dat')

    def test_wrong_file(self):

        with pytest.raises(pysyge.GeoLocatorException):
            pysyge.GeoLocator(path.join(DIR_CURRENT, 'test_module.py'))

    def test_db_version(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        assert geodata.get_db_version() >= 21

    def test_db_date(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        assert isinstance(geodata.get_db_date(), datetime.datetime)

    def test_invalid_ips(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        assert geodata.get_location('127.0.0.1') == {}
        assert geodata.get_location('80.8qeqw') == {}


def assert_location(location, detailed=False):
    assert 'city' in location
    assert 'country_id' in location
    assert 'country_iso' in location
    assert 'lon' in location
    assert 'lat' in location
    assert 'fips' in location
    assert 'region_id' in location

    assert location['city'] == 'Москва'
    assert location['country_id'] == 185
    assert location['country_iso'] == 'RU'
    assert location['lon'] == 37.61556
    assert location['lat'] == 55.75222
    assert location['fips'] == '0'

    if detailed:
        assert 'region' in location
        assert 'tz' in location
        assert location['region_id'] == 524894
        assert location['region'] == 'Москва'

    else:
        assert 'region' not in location
        assert 'tz' not in location
        assert location['region_id'] == 0


class TestGeoLocatorFileModeCheck:

    def test_location_basic(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        location = geodata.get_location(BASE_IP)
        assert_location(location)

    def test_location_detailed(self):
        geodata = pysyge.GeoLocator(DATABASE_CITY_FILE)
        location = geodata.get_location(BASE_IP, detailed=True)
        assert_location(location, detailed=True)

        locations = geodata.get_locations([BASE_IP, '100.20.30.40'])
        assert locations[0]['country_iso'] == 'RU'
        assert locations[1]['country_iso'] == 'US'


@pytest.mark.parametrize('mode', [pysyge.MODE_MEMORY, pysyge.MODE_BATCH])
def test_location_basic(mode):
    geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, mode)
    location = geodata.get_location(BASE_IP)
    assert_location(location)


@pytest.mark.parametrize('mode', [pysyge.MODE_MEMORY, pysyge.MODE_BATCH])
def test_location_detailed(mode):
    geodata = pysyge.GeoLocator(DATABASE_CITY_FILE, mode)
    location = geodata.get_location(BASE_IP, detailed=True)
    assert_location(location, detailed=True)
