from struct import unpack
from socket import inet_aton
from math import floor
from datetime import datetime


MODE_FILE = 0
MODE_MEMORY = 1
MODE_BATCH = 2


class GeoLocatorException(Exception):
    pass


class GeoLocator:
    _cc2iso = (
        '', 'AP', 'EU', 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AN', 'AO', 'AQ',
        'AR', 'AS', 'AT', 'AU', 'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH',
        'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA',
        'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU',
        'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG',
        'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'FX', 'GA', 'GB',
        'GD', 'GE', 'GF', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT',
        'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN',
        'IO', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM',
        'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
        'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN',
        'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA',
        'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA',
        'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY',
        'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI',
        'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD',
        'TF', 'TG', 'TH', 'TJ', 'TK', 'TM', 'TN', 'TO', 'TL', 'TR', 'TT', 'TV', 'TW',
        'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN',
        'VU', 'WF', 'WS', 'YE', 'YT', 'RS', 'ZA', 'ZM', 'ME', 'ZW', 'A1', 'A2', 'O1',
        'AX', 'GG', 'IM', 'JE', 'BL', 'MF'
        )
    _tz = (
        '',  'Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Algiers', 'Africa/Bamako', 'Africa/Banjul',
        'Africa/Blantyre', 'Africa/Brazzaville', 'Africa/Bujumbura', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta',
        'Africa/Conakry', 'Africa/Dakar', 'Africa/Dar_es_Salaam', 'Africa/Douala', 'Africa/Freetown', 'Africa/Gaborone',
        'Africa/Harare', 'Africa/Johannesburg', 'Africa/Kampala', 'Africa/Khartoum', 'Africa/Kigali', 'Africa/Kinshasa',
        'Africa/Lagos', 'Africa/Libreville', 'Africa/Luanda', 'Africa/Lubumbashi', 'Africa/Lusaka', 'Africa/Malabo',
        'Africa/Maputo', 'Africa/Maseru', 'Africa/Mbabane', 'Africa/Mogadishu', 'Africa/Monrovia', 'Africa/Nairobi',
        'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Nouakchott', 'Africa/Ouagadougou', 'Africa/Porto-Novo', 'Africa/Tripoli',
        'Africa/Tunis', 'Africa/Windhoek', 'America/Anchorage', 'America/Anguilla', 'America/Antigua', 'America/Araguaina',
        'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy',
        'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta',
        'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia',
        'America/Asuncion', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize',
        'America/Boa_Vista', 'America/Bogota', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Chicago',
        'America/Chihuahua', 'America/Costa_Rica', 'America/Cuiaba', 'America/Denver', 'America/Dominica', 'America/Edmonton',
        'America/El_Salvador', 'America/Fortaleza', 'America/Godthab', 'America/Grenada', 'America/Guatemala', 'America/Guayaquil',
        'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indianapolis', 'America/Iqaluit',
        'America/Jamaica', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Maceio', 'America/Managua',
        'America/Manaus', 'America/Matamoros', 'America/Mazatlan', 'America/Merida', 'America/Mexico_City', 'America/Moncton',
        'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Nassau', 'America/New_York', 'America/Ojinaga',
        'America/Panama', 'America/Paramaribo', 'America/Phoenix', 'America/Port_of_Spain', 'America/Port-au-Prince',
        'America/Porto_Velho', 'America/Recife', 'America/Regina', 'America/Rio_Branco', 'America/Santo_Domingo',
        'America/Sao_Paulo', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Vincent',
        'America/Tegucigalpa', 'America/Thule', 'America/Tijuana', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg',
        'America/Yellowknife', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Baghdad',
        'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Choibalsan', 'Asia/Chongqing',
        'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Harbin', 'Asia/Ho_Chi_Minh',
        'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul',
        'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kashgar', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching',
        'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk',
        'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Qatar', 'Asia/Qyzylorda', 'Asia/Riyadh',
        'Asia/Sakhalin', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran',
        'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk',
        'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde',
        'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Darwin', 'Australia/Hobart',
        'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Chile/Santiago', 'Europe/Amsterdam', 'Europe/Andorra',
        'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest',
        'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Helsinki', 'Europe/Istanbul',
        'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid',
        'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris',
        'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Simferopol',
        'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Uzhgorod', 'Europe/Vaduz',
        'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Yekaterinburg', 'Europe/Zagreb',
        'Europe/Zaporozhye', 'Europe/Zurich', 'Indian/Antananarivo', 'Indian/Comoro', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius',
        'Pacific/Auckland', 'Pacific/Chatham', 'Pacific/Efate', 'Pacific/Fiji', 'Pacific/Galapagos', 'Pacific/Guadalcanal', 'Pacific/Honolulu',
        'Pacific/Port_Moresby'
    )
    _batch_mode = False
    _memory_mode = False

    def __init__(self, db_file, mode=MODE_FILE):
        """Creates an interface to access Sypex Geo IP database data.

        :param db_file: A path to Sypex Geo IP database file.
        :param mode: Can be any of the following, or a combination:
            MODE_FILE - Seek data in database file on every IP request. Default.
            MODE_MEMORY - Read entire db into memory, an seek data there.
            MODE_BATCH - Create additional indexes to speed up batch IP requests.
        :raises: IOError, GeoLocatorException

        """
        self._fh = open(db_file, 'rb')

        header = self._fh.read(32)
        if header[:3] != 'SxG':
            raise GeoLocatorException('Unable open file %s' % db_file)

        prolog = dict(zip(
            ('ver', 'ts', 'type', 'charset', 'b_idx_len',
             'm_idx_len', 'range', 'db_items', 'id_len', 'max_region',
             'max_city', 'region_size', 'city_size'),
            unpack('>BLBBBHHLBHHLL', header[3:])))

        if prolog['b_idx_len'] * prolog['m_idx_len'] * prolog['range'] * prolog['db_items'] *\
           prolog['ts'] * prolog['id_len'] == 0:
            raise GeoLocatorException('Wrong file format %s' % db_file)

        self._b_idx_str = self._fh.read(prolog['b_idx_len'] * 4)
        self._b_idx_len = prolog['b_idx_len']
        self._m_idx_str = self._fh.read(prolog['m_idx_len'] * 4)
        self._m_idx_len = prolog['m_idx_len']
        self._db_items = prolog['db_items']
        self._db_begin = self._fh.tell()
        self._range = prolog['range']
        self._id_len = prolog['id_len']
        self._block_len = self._id_len + 3
        self._max_region = prolog['max_region']
        self._max_city = prolog['max_city']
        self._batch_mode = mode & MODE_BATCH
        self._memory_mode = mode & MODE_MEMORY
        self._db_ver = prolog['ver']
        self._db_ts = prolog['ts']

        if self._batch_mode:
            self._b_idx_set = unpack('>%dL' % self._b_idx_len, self._b_idx_str)
            del self._b_idx_str
            self._m_idx_set = [self._m_idx_str[i:i + 4] for i in range(0, len(self._m_idx_str), 4)]
            del self._m_idx_str

        if self._memory_mode:
            self._db = self._fh.read(self._db_items * self._block_len)
            self._db_regions = self._fh.read(prolog['region_size'])
            self._db_cities = self._fh.read(prolog['city_size'])
            self._fh.close()

        self._info = {'regions_begin': self._db_begin + self._db_items * self._block_len}
        self._info['cities_begin'] = self._info['regions_begin'] + prolog['region_size']


    def _search_idx(self, ipn, min, max):
        if self._batch_mode:
            while (max - min) > 8:
                offset = (min + max) >> 1
                if ipn > self._m_idx_set[offset]:
                    min = offset
                else:
                    max = offset

            while ipn > self._m_idx_set[min]:
                min += 1
                if min >= max:
                    break
        else:
            while (max - min) > 8:
                offset = (min + max) >> 1
                start = offset * 4
                if ipn > self._m_idx_str[start:start + 4]:
                    min = offset
                else:
                    max = offset

            start = min * 4
            while ipn > self._m_idx_str[start:start + 4]:
                min += 1
                start = min * 4
                if min >= max:
                    break
        return min

    def _search_db(self, str, ipn, min, max):
        if (max - min) > 0:
            ipn = ipn[1:]
            while (max - min) > 8:
                offset = (min + max) >> 1
                start = offset * self._block_len
                if ipn > str[start:start + 3]:
                    min = offset
                else:
                    max = offset

            start = min * self._block_len
            while ipn >= str[start:start + 3]:
                min += 1
                start = min * self._block_len
                if min >= max:
                    break
        else:
            start = min * self._block_len + 3
            return int(str[start:start + 3].encode('hex'), 16)

        start = min * self._block_len - self._id_len
        return int(str[start:start + self._id_len].encode('hex'), 16)

    def _get_pos(self, ip):
        ip1oct = int(ip.split('.', 1)[0])

        if ip1oct == 0 or ip1oct == 10 or ip1oct == 127 or ip1oct >= self._b_idx_len:
            return False

        try:
            ipn = inet_aton(ip)
        except Exception:
            return False

        if self._batch_mode:
            blocks = {'min': self._b_idx_set[ip1oct - 1], 'max': self._b_idx_set[ip1oct]}
        else:
            start = (ip1oct - 1) * 4
            blocks = dict(zip(('min', 'max'), unpack('>LL', self._b_idx_str[start:start + 8])))

        part = self._search_idx(ipn, int(floor(blocks['min'] / self._range)), int(floor(blocks['max'] / self._range) - 1))

        if part > 0:
            min = part * self._range
        else:
            min = 0

        if part > self._m_idx_len:
            max = self._db_items
        else:
            max = (part + 1) * self._range

        if min < blocks['min']:
            min = blocks['min']

        if max > blocks['max']:
            max = blocks['max']

        len = max - min

        if self._memory_mode:
            return self._search_db(self._db, ipn, min, max)
        else:
            self._fh.seek(self._db_begin + min * self._block_len)
            return self._search_db(self._fh.read(len * self._block_len), ipn, 0, len - 1)

    def _parse_location_details(self, city):
        region_seek = city['region_id']

        if region_seek > 0:
            if self._memory_mode:
                region = self._db_regions[region_seek:self._max_region + region_seek].split('\0')
            else:
                self._fh.seek(self._info['regions_begin'] + region_seek)
                region = self._fh.read(self._max_region).split('\0')
            city['region'] = region[0]
            city['tz'] = self._tz[int(region[1])]
        else:
            city['region'] = ''
            city['tz'] = ''
        return city

    def _parse_location(self, seek):
        if self._memory_mode:
            raw = self._db_cities[seek:self._max_city + seek]
        else:
            self._fh.seek(self._info['cities_begin'] + seek)
            raw = self._fh.read(self._max_city)

        city = dict(zip(('region_id', 'country_id', 'fips', 'lat', 'lon'), unpack('>LB2sLL', raw[:15])))
        city['country_iso'] = self._cc2iso[city['country_id']]
        city['lat'] /= float(1000000)
        city['lon'] /= float(1000000)
        city['city'] = raw[15:].split('\0', 2)[0]

        return city

    def get_db_version(self):
        return self._db_ver

    def get_db_date(self):
        return datetime.fromtimestamp(self._db_ts)

    def get_location(self, ip, detailed=False):
        """Returns a dictionary with location data or False on failure.
        Amount of information about IP contained in the dictionary depends
        upon `detailed` flag state.

        """
        seek = self._get_pos(ip)
        if seek > 0:
            location = self._parse_location(seek)
            if detailed:
                return self._parse_location_details(location)
            return location
        else:
            return False
