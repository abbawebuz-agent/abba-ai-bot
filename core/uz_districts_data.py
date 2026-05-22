"""Полный справочник туманов (районов) Узбекистана с координатами их административных центров.

Координаты — приблизительные (центр админ-центра/города), точность ±1–5 км.
Подходят для группировки/радиусов, не подходят для точной геокодинга.

Структура:
    UZ_DISTRICTS_DATA: dict[region_code -> list of district dicts]
        region_code: совпадает с UzRegion.code
        district dict keys:
            code: уникальный slug в пределах региона (matches UzDistrict.code)
            name_uz: название на узбекском (латиница)
            name_ru: название на русском
            lat: широта центра
            lon: долгота центра
"""

UZ_DISTRICTS_DATA = {
    # ───────────────────────── Tashkent (city) ─────────────────────────
    'tashkent_city': [
        {'code': 'bektemir',      'name_uz': 'Bektemir',        'name_ru': 'Бектемир',     'lat': 41.2197, 'lon': 69.3417},
        {'code': 'chilonzor',     'name_uz': "Chilonzor",       'name_ru': 'Чиланзар',     'lat': 41.2667, 'lon': 69.2050},
        {'code': 'mirobod',       'name_uz': 'Mirobod',         'name_ru': 'Мирабад',      'lat': 41.2840, 'lon': 69.2700},
        {'code': 'mirzo_ulugbek', 'name_uz': "Mirzo Ulug‘bek",  'name_ru': 'Мирзо-Улугбек','lat': 41.3300, 'lon': 69.3300},
        {'code': 'olmazor',       'name_uz': 'Olmazor',         'name_ru': 'Алмазар',      'lat': 41.3550, 'lon': 69.2300},
        {'code': 'sergeli',       'name_uz': "Sirg‘ali",        'name_ru': 'Сергели',      'lat': 41.2333, 'lon': 69.2167},
        {'code': 'shayxontohur',  'name_uz': 'Shayxontohur',    'name_ru': 'Шайхантахур',  'lat': 41.3250, 'lon': 69.2300},
        {'code': 'uchtepa',       'name_uz': 'Uchtepa',         'name_ru': 'Учтепа',       'lat': 41.2870, 'lon': 69.1750},
        {'code': 'yakkasaroy',    'name_uz': 'Yakkasaroy',      'name_ru': 'Яккасарай',    'lat': 41.2833, 'lon': 69.2500},
        {'code': 'yashnobod',     'name_uz': 'Yashnobod',       'name_ru': 'Яшнабад',      'lat': 41.3070, 'lon': 69.3300},
        {'code': 'yunusobod',     'name_uz': 'Yunusobod',       'name_ru': 'Юнусабад',     'lat': 41.3700, 'lon': 69.2880},
        {'code': 'yangihayot',    'name_uz': 'Yangihayot',      'name_ru': 'Янгихаёт',     'lat': 41.2100, 'lon': 69.2400},
    ],

    # ───────────────────────── Tashkent region ─────────────────────────
    'tashkent_region': [
        {'code': 'angren',          'name_uz': 'Angren',                 'name_ru': 'Ангрен',           'lat': 41.0167, 'lon': 70.1450},
        {'code': 'bekobod_shahri',  'name_uz': 'Bekobod shahri',         'name_ru': 'Бекабад (город)',  'lat': 40.2167, 'lon': 69.2667},
        {'code': 'bekobod_tumani',  'name_uz': 'Bekobod tumani',         'name_ru': 'Бекабадский район','lat': 40.2333, 'lon': 69.2500},
        {'code': 'boka',            'name_uz': "Bo‘ka",                  'name_ru': 'Бука',             'lat': 40.8167, 'lon': 69.2000},
        {'code': 'bostonliq',       'name_uz': "Bo‘stonliq",             'name_ru': 'Бостанлык',        'lat': 41.5500, 'lon': 70.0167},
        {'code': 'chinoz',          'name_uz': 'Chinoz',                 'name_ru': 'Чиназ',            'lat': 40.9333, 'lon': 68.7667},
        {'code': 'chirchiq',        'name_uz': 'Chirchiq',               'name_ru': 'Чирчик',           'lat': 41.4667, 'lon': 69.5833},
        {'code': 'qibray',          'name_uz': 'Qibray',                 'name_ru': 'Кибрай',           'lat': 41.3833, 'lon': 69.4333},
        {'code': 'ohangaron',       'name_uz': 'Ohangaron',              'name_ru': 'Ахангаран',        'lat': 40.9167, 'lon': 69.6333},
        {'code': 'olmaliq',         'name_uz': 'Olmaliq',                'name_ru': 'Алмалык',          'lat': 40.8500, 'lon': 69.5833},
        {'code': 'oqqorgon',       'name_uz': "Oqqo‘rg‘on",             'name_ru': 'Аккурган',         'lat': 40.8833, 'lon': 69.0833},
        {'code': 'parkent',         'name_uz': 'Parkent',                'name_ru': 'Паркент',          'lat': 41.2833, 'lon': 69.6833},
        {'code': 'piskent',         'name_uz': 'Piskent',                'name_ru': 'Пскент',           'lat': 40.8833, 'lon': 69.3833},
        {'code': 'quyichirchiq',    'name_uz': 'Quyichirchiq',           'name_ru': 'Куйичирчик',       'lat': 41.0833, 'lon': 69.3333},
        {'code': 'yangiyol',        'name_uz': "Yangiyo‘l",              'name_ru': 'Янгиюль',          'lat': 41.1167, 'lon': 69.0500},
        {'code': 'yuqorichirchiq',  'name_uz': 'Yuqorichirchiq',         'name_ru': 'Юкоричирчик',      'lat': 41.2167, 'lon': 69.7500},
        {'code': 'zangiota',        'name_uz': 'Zangiota',               'name_ru': 'Зангиата',         'lat': 41.2167, 'lon': 69.1500},
        {'code': 'toshkent_tumani', 'name_uz': 'Toshkent tumani',        'name_ru': 'Ташкентский район','lat': 41.3500, 'lon': 69.3500},
        {'code': 'nurafshon',       'name_uz': 'Nurafshon',              'name_ru': 'Нурафшан',         'lat': 41.0000, 'lon': 69.3333},
    ],

    # ───────────────────────── Andijon ─────────────────────────────────
    'andijan': [
        {'code': 'andijon_shahri',  'name_uz': 'Andijon shahri',         'name_ru': 'Андижан (город)',     'lat': 40.7821, 'lon': 72.3442},
        {'code': 'andijon_tumani',  'name_uz': 'Andijon tumani',         'name_ru': 'Андижанский район',   'lat': 40.7500, 'lon': 72.3667},
        {'code': 'asaka',           'name_uz': 'Asaka',                  'name_ru': 'Асака',               'lat': 40.6500, 'lon': 72.2333},
        {'code': 'baliqchi',        'name_uz': 'Baliqchi',               'name_ru': 'Балыкчи',             'lat': 40.8500, 'lon': 71.9000},
        {'code': 'boston',          'name_uz': "Bo‘ston",                'name_ru': 'Бустан',              'lat': 40.7333, 'lon': 71.8500},
        {'code': 'buloqboshi',      'name_uz': 'Buloqboshi',             'name_ru': 'Булакбаши',           'lat': 40.6167, 'lon': 72.4000},
        {'code': 'izboskan',        'name_uz': 'Izboskan',               'name_ru': 'Избаскан',            'lat': 40.9333, 'lon': 72.0833},
        {'code': 'jalaquduq',       'name_uz': 'Jalaquduq',              'name_ru': 'Джалакудук',          'lat': 40.7000, 'lon': 72.5667},
        {'code': 'xojaobod',        'name_uz': "Xo‘jaobod",              'name_ru': 'Ходжаабад',           'lat': 40.6833, 'lon': 72.5667},
        {'code': 'marhamat',        'name_uz': 'Marhamat',               'name_ru': 'Мархамат',            'lat': 40.5167, 'lon': 72.3167},
        {'code': 'oltinkol',        'name_uz': "Oltinko‘l",              'name_ru': 'Алтынкуль',           'lat': 40.8667, 'lon': 72.1667},
        {'code': 'paxtaobod',       'name_uz': 'Paxtaobod',              'name_ru': 'Пахтаабад',           'lat': 40.9000, 'lon': 72.5000},
        {'code': 'qorgontepa',     'name_uz': "Qo‘rg‘ontepa",          'name_ru': 'Кургантепа',          'lat': 40.7667, 'lon': 72.7833},
        {'code': 'shahrixon',       'name_uz': 'Shahrixon',              'name_ru': 'Шахрихан',            'lat': 40.7000, 'lon': 72.0500},
        {'code': 'ulugnor',         'name_uz': "Ulug‘nor",               'name_ru': 'Улугнар',             'lat': 40.8667, 'lon': 71.7333},
        {'code': 'xonobod',         'name_uz': 'Xonobod',                'name_ru': 'Ханабад',             'lat': 40.8167, 'lon': 72.9667},
    ],

    # ───────────────────────── Bukhara ─────────────────────────────────
    'bukhara': [
        {'code': 'buxoro_shahri',   'name_uz': 'Buxoro shahri',          'name_ru': 'Бухара (город)',      'lat': 39.7756, 'lon': 64.4286},
        {'code': 'buxoro_tumani',   'name_uz': 'Buxoro tumani',          'name_ru': 'Бухарский район',     'lat': 39.7833, 'lon': 64.4333},
        {'code': 'kogon_shahri',    'name_uz': 'Kogon shahri',           'name_ru': 'Каган (город)',       'lat': 39.7167, 'lon': 64.5500},
        {'code': 'kogon_tumani',    'name_uz': 'Kogon tumani',           'name_ru': 'Каганский район',     'lat': 39.7000, 'lon': 64.5500},
        {'code': 'gijduvon',        'name_uz': "G‘ijduvon",              'name_ru': 'Гиждуван',            'lat': 40.1000, 'lon': 64.6833},
        {'code': 'jondor',          'name_uz': 'Jondor',                 'name_ru': 'Жондор',              'lat': 39.7333, 'lon': 64.2167},
        {'code': 'olot',            'name_uz': 'Olot',                   'name_ru': 'Алат',                'lat': 39.4167, 'lon': 63.6833},
        {'code': 'peshku',          'name_uz': 'Peshku',                 'name_ru': 'Пешку',               'lat': 39.9167, 'lon': 64.2667},
        {'code': 'qorakol',         'name_uz': "Qorako‘l",               'name_ru': 'Каракуль',            'lat': 39.4833, 'lon': 63.8500},
        {'code': 'qorovulbozor',    'name_uz': 'Qorovulbozor',           'name_ru': 'Караулбазар',         'lat': 39.5000, 'lon': 64.7833},
        {'code': 'romitan',         'name_uz': 'Romitan',                'name_ru': 'Рамитан',             'lat': 39.9167, 'lon': 64.3833},
        {'code': 'shofirkon',       'name_uz': 'Shofirkon',              'name_ru': 'Шафиркан',            'lat': 40.0833, 'lon': 64.5000},
        {'code': 'vobkent',         'name_uz': 'Vobkent',                'name_ru': 'Вабкент',             'lat': 40.0167, 'lon': 64.5167},
    ],

    # ───────────────────────── Jizzakh ─────────────────────────────────
    'jizzakh': [
        {'code': 'jizzax_shahri',   'name_uz': 'Jizzax shahri',          'name_ru': 'Джизак (город)',      'lat': 40.1158, 'lon': 67.8422},
        {'code': 'arnasoy',         'name_uz': 'Arnasoy',                'name_ru': 'Арнасай',             'lat': 40.5500, 'lon': 67.7167},
        {'code': 'baxmal',          'name_uz': 'Baxmal',                 'name_ru': 'Бахмаль',             'lat': 39.8667, 'lon': 68.0000},
        {'code': 'dostlik',         'name_uz': "Do‘stlik",               'name_ru': 'Достлик',             'lat': 40.4667, 'lon': 68.0833},
        {'code': 'forish',          'name_uz': 'Forish',                 'name_ru': 'Фариш',               'lat': 40.6500, 'lon': 67.0833},
        {'code': 'gallaorol',       'name_uz': "G‘allaorol",             'name_ru': 'Галляарал',           'lat': 40.0167, 'lon': 67.5833},
        {'code': 'mirzachol',       'name_uz': "Mirzacho‘l",             'name_ru': 'Мирзачуль',           'lat': 40.5500, 'lon': 67.9000},
        {'code': 'paxtakor',        'name_uz': 'Paxtakor',               'name_ru': 'Пахтакор',            'lat': 40.3333, 'lon': 67.9500},
        {'code': 'sharof_rashidov', 'name_uz': 'Sharof Rashidov',        'name_ru': 'Шараф Рашидова',      'lat': 40.1000, 'lon': 67.8500},
        {'code': 'zomin',           'name_uz': 'Zomin',                  'name_ru': 'Заамин',              'lat': 39.9667, 'lon': 68.3833},
        {'code': 'zafarobod',       'name_uz': 'Zafarobod',              'name_ru': 'Зафарабад',           'lat': 40.6167, 'lon': 68.2167},
        {'code': 'zarbdor',         'name_uz': 'Zarbdor',                'name_ru': 'Зарбдар',             'lat': 40.4333, 'lon': 68.1833},
        {'code': 'yangiobod_j',     'name_uz': 'Yangiobod',              'name_ru': 'Янгиабад',            'lat': 40.0500, 'lon': 67.7500},
        {'code': 'gagarin',         'name_uz': 'Gagarin',                'name_ru': 'Гагарин',             'lat': 40.2500, 'lon': 67.9500},
    ],

    # ───────────────────────── Kashkadarya ─────────────────────────────
    'kashkadarya': [
        {'code': 'qarshi_shahri',   'name_uz': 'Qarshi shahri',          'name_ru': 'Карши (город)',       'lat': 38.8606, 'lon': 65.7892},
        {'code': 'qarshi_tumani',   'name_uz': 'Qarshi tumani',          'name_ru': 'Каршинский район',    'lat': 38.8500, 'lon': 65.8000},
        {'code': 'chiroqchi',       'name_uz': 'Chiroqchi',              'name_ru': 'Чиракчи',             'lat': 39.0500, 'lon': 66.5500},
        {'code': 'dehqonobod',      'name_uz': 'Dehqonobod',             'name_ru': 'Дехканабад',          'lat': 38.3833, 'lon': 66.7333},
        {'code': 'guzor',           'name_uz': "G‘uzor",                 'name_ru': 'Гузар',               'lat': 38.6167, 'lon': 66.2500},
        {'code': 'kasbi',           'name_uz': 'Kasbi',                  'name_ru': 'Касби',               'lat': 38.7500, 'lon': 65.6000},
        {'code': 'kitob',           'name_uz': 'Kitob',                  'name_ru': 'Китаб',               'lat': 39.1167, 'lon': 66.8833},
        {'code': 'koson',           'name_uz': 'Koson',                  'name_ru': 'Касан',               'lat': 39.0500, 'lon': 65.5833},
        {'code': 'mirishkor',       'name_uz': 'Mirishkor',              'name_ru': 'Миришкор',            'lat': 38.7500, 'lon': 65.1833},
        {'code': 'muborak',         'name_uz': 'Muborak',                'name_ru': 'Мубарек',             'lat': 39.2667, 'lon': 65.1667},
        {'code': 'nishon',          'name_uz': 'Nishon',                 'name_ru': 'Нишан',               'lat': 38.6667, 'lon': 65.6333},
        {'code': 'qamashi',         'name_uz': 'Qamashi',                'name_ru': 'Камаши',              'lat': 38.8167, 'lon': 66.4500},
        {'code': 'shahrisabz_sh',   'name_uz': 'Shahrisabz shahri',      'name_ru': 'Шахрисабз (город)',   'lat': 39.0500, 'lon': 66.8333},
        {'code': 'shahrisabz_t',    'name_uz': 'Shahrisabz tumani',      'name_ru': 'Шахрисабзский район', 'lat': 39.0667, 'lon': 66.8333},
        {'code': 'yakkabog',        'name_uz': "Yakkabog‘",              'name_ru': 'Яккабаг',             'lat': 38.9667, 'lon': 66.6500},
    ],

    # ───────────────────────── Navoiy ──────────────────────────────────
    'navoi': [
        {'code': 'navoiy_shahri',   'name_uz': 'Navoiy shahri',          'name_ru': 'Навои (город)',       'lat': 40.0844, 'lon': 65.3792},
        {'code': 'karmana',         'name_uz': 'Karmana',                'name_ru': 'Кармана',             'lat': 40.1500, 'lon': 65.3667},
        {'code': 'konimex',         'name_uz': 'Konimex',                'name_ru': 'Канимех',             'lat': 40.2667, 'lon': 65.1833},
        {'code': 'navbahor',        'name_uz': 'Navbahor',               'name_ru': 'Навбахор',            'lat': 40.0000, 'lon': 65.1000},
        {'code': 'nurota',          'name_uz': 'Nurota',                 'name_ru': 'Нурата',              'lat': 40.5667, 'lon': 65.6833},
        {'code': 'qiziltepa',       'name_uz': 'Qiziltepa',              'name_ru': 'Кызылтепа',           'lat': 40.0333, 'lon': 64.8500},
        {'code': 'tomdi',           'name_uz': 'Tomdi',                  'name_ru': 'Тамды',               'lat': 41.7833, 'lon': 64.6333},
        {'code': 'uchquduq',        'name_uz': 'Uchquduq',               'name_ru': 'Учкудук',             'lat': 42.1500, 'lon': 63.5500},
        {'code': 'xatirchi',        'name_uz': 'Xatirchi',               'name_ru': 'Хатырчи',             'lat': 40.1500, 'lon': 65.9167},
        {'code': 'zarafshon',       'name_uz': 'Zarafshon',              'name_ru': 'Зарафшан',            'lat': 41.5667, 'lon': 64.2000},
    ],

    # ───────────────────────── Namangan ────────────────────────────────
    'namangan': [
        {'code': 'namangan_shahri', 'name_uz': 'Namangan shahri',        'name_ru': 'Наманган (город)',    'lat': 40.9983, 'lon': 71.6726},
        {'code': 'namangan_tumani', 'name_uz': 'Namangan tumani',        'name_ru': 'Наманганский район',  'lat': 41.0167, 'lon': 71.6667},
        {'code': 'chortoq',         'name_uz': 'Chortoq',                'name_ru': 'Чартак',              'lat': 41.0667, 'lon': 71.8167},
        {'code': 'chust',           'name_uz': 'Chust',                  'name_ru': 'Чуст',                'lat': 41.0167, 'lon': 71.2333},
        {'code': 'kosonsoy',        'name_uz': 'Kosonsoy',               'name_ru': 'Касансай',            'lat': 41.2500, 'lon': 71.5500},
        {'code': 'mingbuloq',       'name_uz': 'Mingbuloq',              'name_ru': 'Мингбулак',           'lat': 40.8500, 'lon': 71.4000},
        {'code': 'norin',           'name_uz': 'Norin',                  'name_ru': 'Нарын',               'lat': 40.9167, 'lon': 71.5667},
        {'code': 'pop',             'name_uz': 'Pop',                    'name_ru': 'Пап',                 'lat': 40.8667, 'lon': 71.1000},
        {'code': 'toraqorgon',     'name_uz': "To‘raqo‘rg‘on",         'name_ru': 'Туракурган',          'lat': 41.0500, 'lon': 71.5167},
        {'code': 'uchqorgon',      'name_uz': "Uchqo‘rg‘on",            'name_ru': 'Учкурган',            'lat': 41.1000, 'lon': 72.0833},
        {'code': 'uychi',           'name_uz': 'Uychi',                  'name_ru': 'Уйчи',                'lat': 41.0833, 'lon': 71.7833},
        {'code': 'yangiqorgon',    'name_uz': "Yangiqo‘rg‘on",          'name_ru': 'Янгикурган',          'lat': 41.1833, 'lon': 71.6667},
    ],

    # ───────────────────────── Samarkand ───────────────────────────────
    'samarkand': [
        {'code': 'samarqand_sh',    'name_uz': 'Samarqand shahri',       'name_ru': 'Самарканд (город)',   'lat': 39.6542, 'lon': 66.9597},
        {'code': 'samarqand_t',     'name_uz': 'Samarqand tumani',       'name_ru': 'Самаркандский район', 'lat': 39.6800, 'lon': 67.0000},
        {'code': 'bulungur',        'name_uz': 'Bulungur',               'name_ru': 'Булунгур',            'lat': 39.7667, 'lon': 67.2667},
        {'code': 'ishtixon',        'name_uz': 'Ishtixon',               'name_ru': 'Иштыхан',             'lat': 39.9667, 'lon': 66.4833},
        {'code': 'jomboy',          'name_uz': 'Jomboy',                 'name_ru': 'Джамбай',             'lat': 39.7167, 'lon': 67.1500},
        {'code': 'kattaqorgon_sh', 'name_uz': "Kattaqo‘rg‘on shahri",   'name_ru': 'Каттакурган (город)', 'lat': 39.9000, 'lon': 66.2500},
        {'code': 'kattaqorgon_t',  'name_uz': "Kattaqo‘rg‘on tumani",   'name_ru': 'Каттакурганский район','lat': 39.9167, 'lon': 66.2667},
        {'code': 'qoshrabot',       'name_uz': "Qo‘shrabot",             'name_ru': 'Кушрабат',            'lat': 40.2167, 'lon': 66.7500},
        {'code': 'narpay',          'name_uz': 'Narpay',                 'name_ru': 'Нарпай',              'lat': 39.8167, 'lon': 66.3333},
        {'code': 'nurobod',         'name_uz': 'Nurobod',                'name_ru': 'Нурабад',             'lat': 39.6000, 'lon': 66.6333},
        {'code': 'oqdaryo',         'name_uz': 'Oqdaryo',                'name_ru': 'Акдарья',             'lat': 39.7500, 'lon': 66.7833},
        {'code': 'paxtachi',        'name_uz': 'Paxtachi',               'name_ru': 'Пахтачи',             'lat': 39.7833, 'lon': 66.4333},
        {'code': 'pastdargom',     'name_uz': "Pastdarg‘om",            'name_ru': 'Пастдаргом',          'lat': 39.5333, 'lon': 66.8500},
        {'code': 'payariq',         'name_uz': 'Payariq',                'name_ru': 'Пайарык',             'lat': 39.9333, 'lon': 66.6167},
        {'code': 'tayloq',          'name_uz': 'Tayloq',                 'name_ru': 'Тайлак',              'lat': 39.5833, 'lon': 67.0667},
        {'code': 'urgut',           'name_uz': 'Urgut',                  'name_ru': 'Ургут',               'lat': 39.4000, 'lon': 67.2500},
    ],

    # ───────────────────────── Surkhandarya ────────────────────────────
    'surkhandarya': [
        {'code': 'termiz_shahri',   'name_uz': 'Termiz shahri',          'name_ru': 'Термез (город)',      'lat': 37.2242, 'lon': 67.2783},
        {'code': 'termiz_tumani',   'name_uz': 'Termiz tumani',          'name_ru': 'Термезский район',    'lat': 37.3000, 'lon': 67.3167},
        {'code': 'angor',           'name_uz': 'Angor',                  'name_ru': 'Ангор',               'lat': 37.4833, 'lon': 67.0833},
        {'code': 'boysun',          'name_uz': 'Boysun',                 'name_ru': 'Байсун',              'lat': 38.2000, 'lon': 67.2000},
        {'code': 'denov_shahri',    'name_uz': 'Denov shahri',           'name_ru': 'Денау (город)',       'lat': 38.2667, 'lon': 67.9000},
        {'code': 'denov_tumani',    'name_uz': 'Denov tumani',           'name_ru': 'Денауский район',     'lat': 38.2667, 'lon': 67.9000},
        {'code': 'jarqorgon',      'name_uz': "Jarqo‘rg‘on",            'name_ru': 'Джаркурган',          'lat': 37.5000, 'lon': 67.4167},
        {'code': 'muzrabot',        'name_uz': 'Muzrabot',               'name_ru': 'Музрабат',            'lat': 37.3500, 'lon': 66.9333},
        {'code': 'oltinsoy',        'name_uz': 'Oltinsoy',               'name_ru': 'Алтынсай',            'lat': 38.1167, 'lon': 67.8833},
        {'code': 'qiziriq',         'name_uz': 'Qiziriq',                'name_ru': 'Кызырык',             'lat': 37.5500, 'lon': 67.1667},
        {'code': 'qumqorgon',      'name_uz': "Qumqo‘rg‘on",            'name_ru': 'Кумкурган',           'lat': 37.7833, 'lon': 67.5500},
        {'code': 'sariosiyo',       'name_uz': 'Sariosiyo',              'name_ru': 'Сариасия',            'lat': 38.4167, 'lon': 67.9167},
        {'code': 'sherobod',        'name_uz': 'Sherobod',               'name_ru': 'Шерабад',             'lat': 37.6667, 'lon': 67.0167},
        {'code': 'shorchi',         'name_uz': "Sho‘rchi",               'name_ru': 'Шурчи',               'lat': 37.9833, 'lon': 67.7833},
        {'code': 'uzun',            'name_uz': 'Uzun',                   'name_ru': 'Узун',                'lat': 38.4500, 'lon': 68.0000},
    ],

    # ───────────────────────── Syrdarya ────────────────────────────────
    'syrdarya': [
        {'code': 'guliston_sh',     'name_uz': 'Guliston shahri',        'name_ru': 'Гулистан (город)',    'lat': 40.4889, 'lon': 68.7842},
        {'code': 'guliston_t',      'name_uz': 'Guliston tumani',        'name_ru': 'Гулистанский район',  'lat': 40.5000, 'lon': 68.7833},
        {'code': 'boyovut',         'name_uz': 'Boyovut',                'name_ru': 'Баяут',               'lat': 40.5167, 'lon': 68.9667},
        {'code': 'mirzaobod',       'name_uz': 'Mirzaobod',              'name_ru': 'Мирзаабад',           'lat': 40.6333, 'lon': 68.7000},
        {'code': 'oqoltin',         'name_uz': 'Oqoltin',                'name_ru': 'Акалтын',             'lat': 40.5667, 'lon': 68.9333},
        {'code': 'sayxunobod',      'name_uz': 'Sayxunobod',             'name_ru': 'Сайхунабад',          'lat': 40.7167, 'lon': 68.5500},
        {'code': 'sardoba',         'name_uz': 'Sardoba',                'name_ru': 'Сардоба',             'lat': 40.6500, 'lon': 68.5167},
        {'code': 'sirdaryo',        'name_uz': 'Sirdaryo',               'name_ru': 'Сырдарья',            'lat': 40.8500, 'lon': 68.6667},
        {'code': 'xovos',           'name_uz': 'Xovos',                  'name_ru': 'Хаваст',              'lat': 40.2167, 'lon': 68.7833},
        {'code': 'yangiyer',        'name_uz': 'Yangiyer',               'name_ru': 'Янгиер',              'lat': 40.2667, 'lon': 68.8333},
    ],

    # ───────────────────────── Fergana ─────────────────────────────────
    'fergana': [
        {'code': 'fargona_sh',      'name_uz': "Farg‘ona shahri",        'name_ru': 'Фергана (город)',     'lat': 40.3842, 'lon': 71.7842},
        {'code': 'fargona_t',       'name_uz': "Farg‘ona tumani",        'name_ru': 'Ферганский район',    'lat': 40.4000, 'lon': 71.7833},
        {'code': 'oltiariq',        'name_uz': 'Oltiariq',               'name_ru': 'Алтыарык',            'lat': 40.3667, 'lon': 71.2500},
        {'code': 'bagdod',          'name_uz': "Bag‘dod",                'name_ru': 'Багдад',              'lat': 40.4000, 'lon': 71.0833},
        {'code': 'beshariq',        'name_uz': 'Beshariq',               'name_ru': 'Бешарык',             'lat': 40.4333, 'lon': 70.6000},
        {'code': 'buvayda',         'name_uz': 'Buvayda',                'name_ru': 'Бувайда',             'lat': 40.5500, 'lon': 71.2333},
        {'code': 'dangara_f',       'name_uz': "Dang‘ara",               'name_ru': 'Дангара',             'lat': 40.4500, 'lon': 70.6500},
        {'code': 'furqat',          'name_uz': 'Furqat',                 'name_ru': 'Фуркат',              'lat': 40.5000, 'lon': 70.9500},
        {'code': 'qoqon',           'name_uz': "Qo‘qon",                 'name_ru': 'Коканд',              'lat': 40.5286, 'lon': 70.9425},
        {'code': 'qoshtepa',        'name_uz': "Qo‘shtepa",              'name_ru': 'Куштепа',             'lat': 40.3000, 'lon': 71.7000},
        {'code': 'margilon',        'name_uz': "Marg‘ilon",              'name_ru': 'Маргилан',            'lat': 40.4711, 'lon': 71.7247},
        {'code': 'quva',            'name_uz': 'Quva',                   'name_ru': 'Кува',                'lat': 40.5167, 'lon': 72.0667},
        {'code': 'rishton',         'name_uz': 'Rishton',                'name_ru': 'Риштан',              'lat': 40.3500, 'lon': 71.2833},
        {'code': 'sox',             'name_uz': "So‘x",                   'name_ru': 'Сох',                 'lat': 40.0167, 'lon': 71.1333},
        {'code': 'toshloq',         'name_uz': 'Toshloq',                'name_ru': 'Ташлак',              'lat': 40.4500, 'lon': 71.8667},
        {'code': 'uzbekiston_t',    'name_uz': 'O‘zbekiston',            'name_ru': 'Узбекистан',          'lat': 40.5333, 'lon': 71.4167},
        {'code': 'uchkoprik',      'name_uz': "Uchko‘prik",             'name_ru': 'Учкуприк',            'lat': 40.5500, 'lon': 71.0833},
        {'code': 'yozyovon',        'name_uz': 'Yozyovon',               'name_ru': 'Язъяван',             'lat': 40.6000, 'lon': 71.6500},
    ],

    # ───────────────────────── Khorezm ─────────────────────────────────
    'khorezm': [
        {'code': 'urganch_sh',      'name_uz': 'Urganch shahri',         'name_ru': 'Ургенч (город)',      'lat': 41.5500, 'lon': 60.6333},
        {'code': 'urganch_t',       'name_uz': 'Urganch tumani',         'name_ru': 'Ургенчский район',    'lat': 41.5667, 'lon': 60.6500},
        {'code': 'bogot',           'name_uz': "Bog‘ot",                 'name_ru': 'Багат',               'lat': 41.5333, 'lon': 60.8833},
        {'code': 'gurlan',          'name_uz': 'Gurlan',                 'name_ru': 'Гурлен',              'lat': 41.7500, 'lon': 60.6667},
        {'code': 'hazorasp',        'name_uz': 'Hazorasp',               'name_ru': 'Хазарасп',            'lat': 41.3167, 'lon': 61.0833},
        {'code': 'xonqa',           'name_uz': 'Xonqa',                  'name_ru': 'Ханка',               'lat': 41.4833, 'lon': 60.7833},
        {'code': 'xiva_sh',         'name_uz': 'Xiva shahri',            'name_ru': 'Хива (город)',        'lat': 41.3833, 'lon': 60.3667},
        {'code': 'xiva_t',          'name_uz': 'Xiva tumani',            'name_ru': 'Хивинский район',     'lat': 41.4000, 'lon': 60.3667},
        {'code': 'qoshkopir',      'name_uz': "Qo‘shko‘pir",            'name_ru': 'Кушкупир',            'lat': 41.6000, 'lon': 60.4833},
        {'code': 'shovot',          'name_uz': 'Shovot',                 'name_ru': 'Шават',               'lat': 41.6500, 'lon': 60.3667},
        {'code': 'tuproqqala',     'name_uz': "Tuproqqal‘a",            'name_ru': 'Тупраккала',          'lat': 41.5500, 'lon': 60.9667},
        {'code': 'yangiariq',       'name_uz': 'Yangiariq',              'name_ru': 'Янгиарык',            'lat': 41.3000, 'lon': 60.5500},
        {'code': 'yangibozor',      'name_uz': 'Yangibozor',             'name_ru': 'Янгибазар',           'lat': 41.6667, 'lon': 60.5167},
    ],

    # ───────────────────────── Karakalpakstan ──────────────────────────
    'karakalpakstan': [
        {'code': 'nukus_shahri',    'name_uz': 'Nukus shahri',           'name_ru': 'Нукус (город)',       'lat': 42.4531, 'lon': 59.6103},
        {'code': 'nukus_tumani',    'name_uz': 'Nukus tumani',           'name_ru': 'Нукусский район',     'lat': 42.4500, 'lon': 59.6000},
        {'code': 'amudaryo',        'name_uz': 'Amudaryo',               'name_ru': 'Амударья',            'lat': 42.0167, 'lon': 60.5167},
        {'code': 'beruniy',         'name_uz': 'Beruniy',                'name_ru': 'Беруни',              'lat': 41.6833, 'lon': 60.7500},
        {'code': 'chimboy',         'name_uz': 'Chimboy',                'name_ru': 'Чимбай',              'lat': 42.9500, 'lon': 59.7667},
        {'code': 'ellikqala',      'name_uz': "Ellikqal‘a",             'name_ru': 'Элликкала',           'lat': 41.9167, 'lon': 60.7833},
        {'code': 'kegeyli',         'name_uz': 'Kegeyli',                'name_ru': 'Кегейли',             'lat': 42.7667, 'lon': 59.7500},
        {'code': 'moynaq',          'name_uz': "Mo‘ynoq",                'name_ru': 'Муйнак',              'lat': 43.7667, 'lon': 59.0167},
        {'code': 'qonlikol',       'name_uz': "Qonliko‘l",              'name_ru': 'Канлыкуль',           'lat': 42.9333, 'lon': 59.3833},
        {'code': 'qongirot',       'name_uz': "Qo‘ng‘irot",             'name_ru': 'Кунград',             'lat': 43.0500, 'lon': 58.8500},
        {'code': 'qoraozak',       'name_uz': "Qorao‘zak",              'name_ru': 'Караузяк',            'lat': 42.9000, 'lon': 60.0667},
        {'code': 'shumanay',        'name_uz': 'Shumanay',               'name_ru': 'Шуманай',             'lat': 42.6167, 'lon': 58.8833},
        {'code': 'taxiatosh',       'name_uz': 'Taxiatosh',              'name_ru': 'Тахиаташ',            'lat': 42.3333, 'lon': 59.6167},
        {'code': 'taxtakopir',     'name_uz': "Taxtako‘pir",            'name_ru': 'Тахтакупыр',          'lat': 43.0167, 'lon': 60.3000},
        {'code': 'tortkol',        'name_uz': "To‘rtko‘l",              'name_ru': 'Турткуль',            'lat': 41.5500, 'lon': 61.0000},
        {'code': 'xojayli',         'name_uz': 'Xo‘jayli',               'name_ru': 'Ходжейли',            'lat': 42.4000, 'lon': 59.4500},
    ],
}


def get_all_districts_flat():
    """Возвращает плоский список всех туманов с region_code в каждом dict."""
    out = []
    for region_code, districts in UZ_DISTRICTS_DATA.items():
        for d in districts:
            entry = dict(d)
            entry['region_code'] = region_code
            out.append(entry)
    return out
