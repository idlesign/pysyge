from binascii import hexlify
from datetime import datetime
from math import floor
from socket import inet_aton
from struct import unpack
from typing import Union, List, Dict, Any

TypeGeoDict = Dict[str, Any]

MODE_FILE = 0
MODE_MEMORY = 1
MODE_BATCH = 2


def chr_(val: Union[int, bytes]):
    try:
        return chr(val)

    except TypeError:
        pass

    return val


class GeoLocatorException(Exception):
    """Basic pysyge GeoLocator exception."""


class GeoLocator:

    _cc2iso = (
        '', 'AP', 'EU', 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'CW', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU',
        'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS',
        'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
        'CO', 'CR', 'CU', 'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG',
        'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'SX', 'GA', 'GB', 'GD', 'GE', 'GF',
        'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN',
        'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE',
        'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR',
        'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP',
        'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI',
        'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN',
        'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG',
        'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD', 'TF',
        'TG', 'TH', 'TJ', 'TK', 'TM', 'TN', 'TO', 'TL', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM',
        'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'RS', 'ZA',
        'ZM', 'ME', 'ZW', 'A1', 'XK', 'O1', 'AX', 'GG', 'IM', 'JE', 'BL', 'MF', 'BQ', 'SS'
    )
    _batch_mode = False
    _memory_mode = False

    _TYPE_COUNTRY = 0
    _TYPE_REGION = 1
    _TYPE_CITY = 2

    def __init__(self, db_file: str, mode: int = MODE_FILE):
        """Creates an interface to access Sypex Geo IP database data.

        :param db_file: A path to Sypex Geo IP database file.

        :param mode: Can be any of the following, or a combination:
            MODE_FILE - Seek data in database file on every IP request. Default.
            MODE_MEMORY - Read entire db into memory, an seek data there.
            MODE_BATCH - Create additional indexes to speed up batch IP requests.

        :raises: IOError, GeoLocatorException

        """
        self._fh = open(db_file, 'rb')

        header = self._fh.read(40)

        if header[:3] != b'SxG':
            raise GeoLocatorException('Unable open file %s' % db_file)

        prolog = dict(zip(
            ('ver', 'ts', 'type', 'charset', 'b_idx_len',
             'm_idx_len', 'range', 'db_items', 'id_len', 'max_region',
             'max_city', 'region_size', 'city_size', 'max_country',
             'country_size', 'pack_size'),
            unpack('>BLBBBHHLBHHLLHLH', header[3:])))

        if prolog['b_idx_len'] * prolog['m_idx_len'] * prolog['range'] * prolog['db_items'] * \
                prolog['ts'] * prolog['id_len'] == 0:
            raise GeoLocatorException('Wrong file format %s' % db_file)

        self._b_idx_len = prolog['b_idx_len']
        self._m_idx_len = prolog['m_idx_len']
        self._db_items = prolog['db_items']
        self._range = prolog['range']
        self._id_len = prolog['id_len']
        self._block_len = self._id_len + 3
        self._max_region = prolog['max_region']
        self._max_city = prolog['max_city']
        self._max_country = prolog['max_country']
        self._country_size = prolog['country_size']
        self._batch_mode = mode & MODE_BATCH
        self._memory_mode = mode & MODE_MEMORY
        self._db_ver = prolog['ver']
        self._db_ts = prolog['ts']

        self._pack = self._fh.read(prolog['pack_size']).split(b'\0') if prolog['pack_size'] else ''

        self._b_idx_str = self._fh.read(prolog['b_idx_len'] * 4)
        self._m_idx_str = self._fh.read(prolog['m_idx_len'] * 4)
        self._db_begin = self._fh.tell()

        if self._batch_mode:
            self._b_idx_set = unpack('>%dL' % self._b_idx_len, self._b_idx_str)
            del self._b_idx_str
            self._m_idx_set = [self._m_idx_str[i:i + 4] for i in range(0, len(self._m_idx_str), 4)]
            del self._m_idx_str

        if self._memory_mode:
            self._db = self._fh.read(self._db_items * self._block_len)
            self._db_regions = ''
            self._db_cities = ''

            if prolog['region_size']:
                self._db_regions = self._fh.read(prolog['region_size'])

            if prolog['city_size']:
                self._db_cities = self._fh.read(prolog['city_size'])

            self._fh.close()

        self._info = {'regions_begin': self._db_begin + self._db_items * self._block_len}
        self._info['cities_begin'] = self._info['regions_begin'] + prolog['region_size']

    def _search_idx(self, ipn: bytes, min_: int, max_: int) -> int:

        if self._batch_mode:
            m_idx = self._m_idx_set

            while (max_ - min_) > 8:

                offset = (min_ + max_) >> 1

                if ipn > m_idx[offset]:
                    min_ = offset

                else:
                    max_ = offset

            while ipn > m_idx[min_]:

                min_ += 1

                if min_ >= max_:
                    break

        else:
            m_idx = self._m_idx_str

            while (max_ - min_) > 8:

                offset = (min_ + max_) >> 1
                start = offset * 4

                if ipn > m_idx[start:start + 4]:
                    min_ = offset

                else:
                    max_ = offset

            start = min_ * 4

            while ipn > m_idx[start:start + 4]:

                min_ += 1
                start = min_ * 4

                if min_ > max_:
                    break

        return min_

    def _search_db(self, str_: bytes, ipn: bytes, min_: int, max_: int) -> int:

        len_block = self._block_len

        if (max_ - min_) > 1:

            ipn = ipn[1:]

            while (max_ - min_) > 8:
                offset = (min_ + max_) >> 1
                start = offset * len_block

                if ipn > str_[start:start + 3]:
                    min_ = offset

                else:
                    max_ = offset

            start = min_ * len_block

            while ipn >= str_[start:start + 3]:
                min_ += 1
                start = min_ * len_block

                if min_ >= max_:
                    break

        else:
            min_ += 1

        len_id = self._id_len
        start = min_ * len_block - len_id

        return int(hexlify(str_[start:start + len_id]), 16)

    def _get_pos(self, ip: str) -> int:

        ip1oct = int(ip.split('.', 1)[0])

        if ip1oct in {0, 10, 127} or ip1oct >= self._b_idx_len:
            return 0

        try:
            ipn = inet_aton(ip)

        except OSError:
            return 0

        if self._batch_mode:
            blocks = {
                'min': self._b_idx_set[ip1oct-1],
                'max': self._b_idx_set[ip1oct]
            }

        else:
            start = (ip1oct - 1) * 4
            blocks = dict(zip(('min', 'max'), unpack('>LL', self._b_idx_str[start:start + 8])))

        range_ = self._range

        if blocks['max'] - blocks['min'] > range_:

            part = self._search_idx(
                ipn,
                int(floor(blocks['min'] / range_)),
                int(floor(blocks['max'] / range_) - 1)
            )

            min_ = part * range_ if part > 0 else 0
            max_ = self._db_items if part > self._m_idx_len else (part + 1) * range_

            if min_ < blocks['min']:
                min_ = blocks['min']

            if max_ > blocks['max']:
                max_ = blocks['max']

        else:
            min_ = blocks['min']
            max_ = blocks['max']

        length = max_ - min_

        if self._memory_mode:
            return self._search_db(self._db, ipn, min_, max_)

        self._fh.seek(self._db_begin + min_ * self._block_len)

        return self._search_db(self._fh.read(length * self._block_len), ipn, 0, length - 1)

    def _read_data_chunk(self, data_type: int, start_pos: int, max_read: int) -> TypeGeoDict:

        raw = b''

        if start_pos and max_read:

            if self._memory_mode:
                src = self._db_cities

                if data_type == self._TYPE_REGION:
                    src = self._db_regions

                raw = src[start_pos:start_pos+max_read]

            else:
                boundary_key = 'cities_begin'

                if data_type == self._TYPE_REGION:
                    boundary_key = 'regions_begin'

                self._fh.seek(self._info[boundary_key]+start_pos)
                raw = self._fh.read(max_read)

        return self._parse_pack(self._pack[data_type], raw)

    def _parse_location(self, start_pos: int, detailed: bool = False) -> TypeGeoDict:

        if not self._pack:
            return {}

        country_only = False

        if start_pos < self._country_size:
            country = self._read_data_chunk(self._TYPE_COUNTRY, start_pos, self._max_country)
            city = self._parse_pack(self._pack[2])
            country_only = True
            city['lat'] = country['lat']
            city['lon'] = country['lon']

        else:
            city = self._read_data_chunk(self._TYPE_CITY, start_pos, self._max_city)
            country = {
                'id': city['country_id'],
                'iso': self._cc2iso[city['country_id']]
            }

        region = None

        if detailed:
            region = self._read_data_chunk(self._TYPE_REGION, city['region_seek'], self._max_region)

            if not country_only:
                country = self._read_data_chunk(self._TYPE_COUNTRY, region['country_seek'], self._max_country)

        return self._structure_location_data(city, country, region)

    @staticmethod
    def _structure_location_data(city: TypeGeoDict, country: TypeGeoDict, region) -> TypeGeoDict:

        del city['country_id']
        del city['region_seek']

        doc = {
            'country_id': country['id'],
            'country_iso': country['iso'],

            'region_id': 0,

            'city': city['name_ru'],
            'lon': city['lon'],
            'lat': city['lat'],
            'fips': '0',  # For backward compatibility. Dropped in SypexGeo 2.2.

            'info': {
                'city': city,
                'region': region,
                'country': country
            }
        }

        if region is not None:
            del region['country_seek']
            doc['region'] = region['name_ru']
            doc['region_id'] = region['id']
            doc['tz'] = region.get('timezone', '')

        return doc

    @staticmethod
    def _parse_pack(pack: bytes, item: bytes = b'') -> TypeGeoDict:

        result = {}
        start_pos = 0
        empty = not item

        map_len = {
            't': 1, 'T': 1,
            's': 2, 'S': 2, 'n': 2,
            'm': 3, 'M': 3,
            'd': 8,
            'c': lambda: int(chr_(chunk_type[1:])),
            'b': lambda: item.find(b'\0', start_pos) - start_pos
        }
        map_val = {
            't': lambda: unpack('b', val),
            'T': lambda: unpack('B', val),
            's': lambda: unpack('h', val),
            'S': lambda: unpack('H', val),
            'm': lambda: unpack('i', val),  # TODO unpack('i', val + (ord(val[2]) >> 7 ? '\xff' : '\0'))
            'M': lambda: unpack('I', val + b'\0'),
            'i': lambda: unpack('i', val),
            'I': lambda: unpack('I', val),
            'f': lambda: unpack('f', val),
            'd': lambda: unpack('d', val),
            'n': lambda: unpack('h', val)[0] / pow(10, int(chr_(chunk_type[1]))),
            'N': lambda: unpack('i', val)[0] / pow(10, int(chr_(chunk_type[1]))),
            'c': lambda: val.rstrip(b' '),
        }

        for chunk in pack.split(b'/'):

            chunk_type, chunk_name = chunk.split(b':')
            chunk_name = chunk_name.decode()
            type_letter = chr_(chunk_type[0])

            if empty:
                result[chunk_name] = '' if type_letter in {'b', 'c'} else 0
                continue

            length = map_len.get(type_letter, 4)
            chars = type_letter in {'c', 'b'}

            if chars:
                length = length()

            end_pos = start_pos+length
            val: bytes = item[start_pos:end_pos]
            val_real = map_val.get(type_letter)

            if val_real is None:  # case `b`
                val_real = val
                length += 1

            else:
                val_real = val_real()

            start_pos += length

            if chars:
                val_real = val_real.decode()

            result[chunk_name] = val_real

            if isinstance(val_real, tuple):
                result[chunk_name] = val_real[0]

        return result

    def get_db_version(self) -> int:
        """Returns database version number."""
        return self._db_ver

    def get_db_date(self) -> datetime:
        """Returns database creation datetime."""
        return datetime.fromtimestamp(self._db_ts)

    def get_location(self, ip: str, detailed: bool = False) -> TypeGeoDict:
        """Returns a dictionary with location data or False on failure.

        :param ip:

        :param detailed: Amount of information about IP contained
            in the dictionary depends upon `detailed` flag state.

        """
        seek = self._get_pos(ip)

        if seek > 0:
            return self._parse_location(seek, detailed=detailed)

        return {}

    def get_locations(self, ip: Union[List[str], str], detailed: bool = False) -> List[TypeGeoDict]:
        """Returns a list of dictionaries with location data.

        :param ip: Argument `ip` must be an iterable object.

        :param detailed: Amount of information about IP contained
            in the dictionary depends upon `detailed` flag state.

        """
        if isinstance(ip, str):
            ip = [ip]
            
        return [
            self._parse_location(pos, detailed=detailed) if pos > 0 else {}
            for pos in map(self._get_pos, ip)
        ]
