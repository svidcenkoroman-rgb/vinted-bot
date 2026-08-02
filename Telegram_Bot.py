import sqlite3
import requests
import time
import os
import re
import threading
from datetime import datetime
from telegram.ext import Updater, CommandHandler

TOKEN = '8734372802:AAF3KKneCCOEYdZz_Z6Zv4kx2nNo39NNgM0'
ADMIN_CHAT_ID = 7321242131

CATEGORIES = {
    'мужская обувь': 16, 'мужские кроссовки': 16, 'мужские куртки': 1231,
    'мужские штаны': 1224, 'мужские джинсы': 1224, 'мужские футболки': 1225,
    'мужские толстовки': 1228, 'мужские рубашки': 1226, 'мужские костюмы': 1232,
    'мужские шорты': 1227, 'мужские свитера': 1229, 'мужские аксессуары': 1241,
    'мужские шапки': 1241, 'мужские ремни': 1241,
    'женская обувь': 1037, 'женские кроссовки': 1037, 'женские куртки': 1143,
    'женские штаны': 1138, 'женские джинсы': 1138, 'женские футболки': 1132,
    'женские платья': 1235, 'женские юбки': 1136, 'женские толстовки': 1133,
    'женские блузки': 1131, 'женские свитера': 1134, 'женские сумки': 1245,
    'женские аксессуары': 1244, 'женские шапки': 1244, 'женское бельё': 1140,
    'женские купальники': 1141,
    'обувь': 16, 'кроссовки': 16, 'куртки': 1231, 'штаны': 1224,
    'джинсы': 1224, 'футболки': 1225, 'платья': 1235, 'сумки': 1245,
    'толстовки': 1228, 'рубашки': 1226, 'свитера': 1229, 'шорты': 1227,
    'аксессуары': 1241, 'шапки': 1241, 'ремни': 1241, 'часы': 1246,
    'очки': 1246, 'украшения': 1244, 'парфюм': 1260,
    'спортивная одежда': 1230, 'пальто': 1231, 'пиджаки': 1232,
    'носки': 1243, 'перчатки': 1241, 'шарфы': 1241,
}

# ═══════════════════════════════════
# COOKIE — обновляй здесь когда истекут
# ═══════════════════════════════════
COOKIE = '__ps_r=https://www.google.com/; __ps_lu=https://www.vinted.pl/; __ps_did=pscrb_e287bbdd-5a61-4eaa-efa0-ceeeda2769a3; __ps_fva=1757197538485; v_udt=UDdEZU55ZVR6bkZBaWdnOXo2TUpuQ2RCaFN3SC0tM1c4K0lGYW56SzhuWXF5My0tWlBQN25tdGdXNlJxbFRUYWhVOWZpUT09; anon_id=dc3d5138-f0e2-44b6-b322-67bac0ad7f0e; anonymous-locale=pl-fr; anonymous-iso-locale=pl-PL; non_dot_com_www_domain_cookie_buster=1; is_shipping_fees_applied_info_banner_dismissed=false; OptanonAlertBoxClosed=2026-07-13T10:27:44.764Z; eupubconsent-v2=CQnSI_AQnSI_AAcABBPLCnFgAAAAAEPgAAwIAAAWZABMNDogjLIgECBQEAIEACgrCACgQBAAAkBRAQAmDAhyBgAusIkAIAUAAQQAgABBgACAAASABCIAIACAQAgQCBQABgAQBAQAMDAAGAChEAgABAdAxSAggECwASIwoDBAhAASCAlsqEEgCBBXCFIscAggREwUAACIABQAAAB4WAhJKCViQQBcQXQAIAAAAUQIMCKQswBRQGQLQVgScBkaYAkeYJEkOgiAJghIyDIhNUEg8UxRAAAA.YAAACHwAAAAA.ILNtR_G__bXlv-Tb36bpkeYxf99hr7sQxBgbIsm4FzLvW7JwC32EbJEyatiIKmRIAu3TBIQNtHIjURUChKIgVrzDsaEyUoTtKJ-BkiDMRY2JQCFhum4pjWQCZYur_50d0mR-N7dr-2dzyy5hnv3a9fuS1UJicKYetHfn8ZBKS-_IU9_x-_4v4_MbpEm8eSVv9tGtt43c64tP6dpuxt-Tyffyfv_f72fe7X__c__33_-qXX_r764A; OTAdditionalConsentString=2~~dv.20.43.55.57.61.70.83.89.93.108.117.122.124.135.143.144.147.149.159.161.184.192.196.211.228.230.236.239.255.259.266.272.286.291.311.313.314.320.322.323.327.358.367.370.371.385.407.415.424.429.430.436.445.469.486.491.494.495.522.523.540.550.560.568.574.576.587.591.621.723.737.797.798.803.820.827.839.864.899.904.922.938.955.959.979.981.985.986.1003.1027.1031.1033.1046.1047.1048.1051.1053.1067.1092.1095.1097.1099.1107.1109.1126.1135.1143.1149.1152.1162.1166.1186.1188.1192.1205.1215.1220.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1329.1342.1345.1356.1365.1403.1415.1416.1419.1421.1423.1440.1449.1455.1495.1512.1514.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1598.1603.1616.1638.1651.1653.1659.1660.1667.1677.1678.1682.1697.1699.1712.1716.1720.1721.1725.1732.1735.1745.1750.1753.1782.1786.1800.1808.1810.1825.1827.1832.1838.1840.1843.1845.1859.1870.1878.1880.1882.1889.1898.1911.1917.1928.1929.1942.1944.1958.1962.1963.1964.1967.1968.1969.1978.1985.1987.2003.2027.2035.2038.2039.2044.2047.2052.2056.2064.2068.2069.2072.2074.2084.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2141.2147.2156.2166.2177.2186.2205.2213.2216.2219.2220.2222.2223.2224.2225.2227.2234.2251.2253.2271.2275.2279.2282.2295.2299.2309.2312.2316.2322.2325.2328.2331.2335.2336.2343.2354.2358.2359.2370.2373.2376.2377.2400.2403.2405.2406.2410.2411.2414.2415.2416.2418.2425.2427.2440.2447.2453.2461.2465.2468.2472.2477.2484.2486.2488.2498.2506.2510.2517.2526.2527.2531.2534.2535.2542.2552.2559.2564.2567.2568.2569.2571.2572.2575.2577.2579.2583.2584.2589.2595.2596.2604.2605.2609.2610.2612.2614.2621.2624.2627.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2689.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2778.2784.2787.2791.2792.2798.2801.2805.2812.2813.2814.2816.2817.2821.2822.2824.2827.2830.2831.2832.2833.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2872.2874.2875.2878.2880.2881.2882.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2916.2917.2918.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2972.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3001.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3023.3028.3031.3034.3038.3043.3051.3052.3053.3055.3058.3059.3063.3066.3070.3073.3074.3075.3076.3077.3089.3090.3093.3094.3095.3097.3099.3100.3106.3107.3109.3112.3117.3119.3126.3127.3128.3130.3133.3135.3136.3137.3145.3149.3151.3153.3155.3165.3167.3169.3172.3173.3177.3182.3184.3185.3186.3187.3188.3189.3190.3194.3196.3200.3201.3209.3210.3213.3214.3215.3217.3218.3222.3223.3225.3226.3227.3228.3230.3231.3233.3235.3236.3237.3238.3240.3244.3250.3251.3253.3254.3257.3260.3266.3270.3272.3286.3288.3289.3290.3292.3293.3296.3299.3300.3306.3307.3309.3314.3315.3316.3318.3323.3324.3328.3330.3331.3531.3631.3731.3831.4131.4531.4631.4731.4831.5231.6931.7131.7235.7831.7931.8931.10231.10631.10831.11031.11531.11631.13431.13632.14034.14133.14237.15731.16831.16931.21233.21731.23031.25131.25931.26031.26631.27731.27831.28031.28332.28731.29631.30331.30532.30732.32531.33931.34231.34631.34731.36831.39131.39531.40632.41131.41531.43631.43731.43831.45931.47232.47531.48131.49231.49332.49431.50831.52831.54231.56831.56931.57131.57231.57531; domain_selected=true; v_sid=3732dc8f-1783673146; consent_version=eu; v_uid=3172767044; v_sid=72d4e1e6-1785594286; user-iso-locale=pl-PL; ad_blocker_detected=true; cf_clearance=ciP2QbcUUpR6LZUJ_BHzHr4DKPsCpaymdMVyesMQdX0-1785678502-1.2.1.1-lJ_dBO_8D29X03CFtifGYlW5oHEzUDK2F7vveYTu9aSZo.5hp.kR2WOgAyTcg2qj47mVbpIXaFAq1ffV7w1OL9gWErz_rF_IHeAz_8baN.PlXUqe232F6VuhpPxuzTLlGaJVQKvANrj7xW365zpBK4mIh_e_7_SMSJyCkgXxdr34a9Fp.MEnCpW_nvIJNhU74ad5Z9LI3a55XZOrGpcU5FkhEct7m5dvGOc38cnF.mwrE_qdLQmGoFu4v45qtJ8.GHk9B3CwwzVUFI0gL.1LTI4T8oBQq_iteNpnufmRamPbvqjSp.OtvKqQVl_JwNd4K4U9gYmo3dWhqMPfxamn1bj1aEGu14_CKGMdycFrHo4GlOfoSGa3TdF8MxoBH7RbsFjN75EfUtbpnANCEVPbDYXYD5LQY6kxYkYQjmIXhA0naaJzf0fvjOvvR1GgoNLtGuR7HZkv53cwuvkNPwVNLQ; __cf_bm=vGsWINmmKUtE2iz1LbKLaLLkXjD6WDS2Pwvahrg9UEc-1785678502.8890758-1.0.1.1-oiHXACnIrHVhSasybT_B4jGqjH5O.4YQCnmm7SHw9zHrvlki2nI1z90z76UWU31Hy1Pr3KcuxJ.3AuObDmNNza0UMru3ZxfeMgqt0xfVaFTx7KBxQrq1A4XxVJZmxQ4njWr3mP8mEVM86igdKKaTBg; refresh_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg2MjgzMzAzLCJpYXQiOjE3ODU2Nzg1MDMsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJyZWZyZXNoIiwicm9sZXMiOiIiLCJzY29wZSI6InB1YmxpYyB1c2VyIiwic2lkIjoiNzJkNGUxZTYtMTc4NTU5NDI4NiIsInN1YiI6IjMxNzI3NjcwNDQiLCJjYyI6IlBMIiwiYW5pZCI6ImRjM2Q1MTM4LWYwZTItNDRiNi1iMzIyLTY3YmFjMGFkN2YwZSIsImFjdCI6eyJzdWIiOiIzMTcyNzY3MDQ0In19.mXYE34Jq-0SY1a2FmVQBNgNfeW0Rf5tCp0rB7K-aUcflCvVi5PmKpMj_D6FyFPoFGe3X6XF5drbPqdEntoW6mJlumHvNJHLwbIitMj0VBBKa1JXaSCHjXmSKZH_sIxjNX5YEcd22N0e4xqpyIfcV1XOuMlbuZv7tUi5wKNGmDX85g05iEdsLe9utx5xmSAwiAfsyp0ZCxu9mZ8Kqfp6VOAxVqaC4Obmxr_UrUNsvHix_y5EY2DXymPHdXC-7sbOvcKNrRymwXTw_9lHbFoPali1L-V_328-qD63MER1STCHBeHCHmdA0wRVPbKO0EJToSMaPuN3O1LIrWbZQO6s5WA; access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg1Njg1NzAzLCJpYXQiOjE3ODU2Nzg1MDMsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJhY2Nlc3MiLCJyb2xlcyI6IiIsInNjb3BlIjoicHVibGljIHVzZXIiLCJzaWQiOiI3MmQ0ZTFlNi0xNzg1NTk0Mjg2Iiwic3ViIjoiMzE3Mjc2NzA0NCIsImNjIjoiUEwiLCJhbmlkIjoiZGMzZDUxMzgtZjBlMi00NGI2LWIzMjItNjdiYWMwYWQ3ZjBlIiwiYWN0Ijp7InN1YiI6IjMxNzI3NjcwNDQifX0.V9YYQ7sX1yLjNNHlKL2mLNnUnCOU1-xpQFHZnSvPgOz5HZi3v5STtNwKvxQOA3ux80bcMas1Oc8skXtK-XABlSbBMZsRwRLljlwOPmgE4ViVToqujfomUG4eAVxWohL01Yc9HNA2Hxt_AfKTqVjoy8JhJcgRwanmf7NB3iP-dsQkr8GBKR_mPoRaSYjg9XCnxShjqLC-cdbsO5XH3uSSQMMsveaqstWrE-ImWIxz8Z5ZoNFbmC23T7KgZMaHmQZunitrcAJE5M1ulNFVHzGk3sXMYJWb_ZTMkHiNS70k7f_dBc0VSHkfZ6BZtXEiSg0bS9sKUkDsZ0RylJSKtd2SYw; seller_header_visits=3; viewport_size=150; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Aug+02+2026+15%3A49%3A00+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202602.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=3172767044&identifierType=Cookie+Unique+Id&isAnonUser=1&hosts=&interactionCount=2&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0005%3A0%2CV2STACK42%3A0%2CC0035%3A0%2CC0038%3A0&genVendors=V5%3A0%2CV2%3A0%2CV1%3A0%2C&crTime=1783938465116&AwaitingReconsent=false&intType=2&geolocation=PL%3B14; banners_ui_state=SUCCESS; _vinted_fr_session=RjFNTHZPakROMEpoUFhwQnhRQnpkOUd3Yk5NRm1CRlU3NGh2UWpCRXhCeTRzRWJRZlRiYVpjRklkTmo2bCtUbXJKZkdYUWVWMlg3QWtQUG5UUXpncXhLc0tLeUJmMUFOendRbkJEVi8yTWpNT2cyV2x5VXBTT3duUUVkMTdPZVRVMTRlQnYwcTRka0QxYkdUR2F1OWh0ZUFLTjAxWXNGQmNzS0pRZ0JBREJZdnpjejBocHA1WDZqN2EvQmRvNm9udUI4VG1TUlZuQ1poc0Jka1lmdWJmNHNCd0R2R3ZuU3FMOEpRd1RNV29qb1FYWHZuQm5IOUV4VDBiS0ZtUGRjc1BqTmxESk1GejlBcld1QkV3M0hjVDZmRmJJaGZxZXpFUHV3b3g2dGs3Q0FwNmpZWXpBNTFsQzMvL3RMelg3aEluWUt4cHRsRVJjazFjSDNrVmdUVzkwajJndnRCM0hYS216VGpaeEZENk9MS2ZiMHVHZERXaVFiV0Q1SXF5cHkyZGJ4YjN6SUt0ZU1YZEJsRVBjS0lWUWEveG44cEdiRUZ3NzJGQUhGVEU0eUd6dzlsMnk3dHdGS0oxTmczcWxudC0tbmlMeC9ubVpYdURYQXdnMFVnMkZJQT09--160434e76e8d57e35eafeaa49cddabc04e8b7643; datadome=jbHibD8hzSMBXjmoJjklD3nSKfguWn6ae2MIgdn6Sxqt10pzuU0G_SaIbb9AwRwYxmE4bSSwz14e_ORxDK4PBv2_buv7PR02ETsq9XsQSmWvOOQNQwi3~fFHa1eUHk0a'

def get_current_cookie():
    """Возвращает актуальный cookie"""
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', 'r') as f:
            saved = f.read().strip()
            if saved:
                print("Cookie из файла ✅")
                return saved
    print("Cookie из кода")
    return COOKIE.strip()

def build_headers(cookie):
    return {
        'accept': 'application/json,text/plain,*/*',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie,
        'locale': 'pl-PL',
        'referer': 'https://www.vinted.pl/catalog?search_text=Nike',
        'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        'x-anon-id': 'dc3d5138-f0e2-44b6-b322-67bac0ad7f0e',
        'x-csrf-token': '75f6c9fa-dc8e-4e52-a000-e09dd4084b3e',
    }

def hex_to_color_name(hex_color):
    if not hex_color:
        return None
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        if r < 50 and g < 50 and b < 50: return '⚫ Чёрный'
        elif r > 200 and g > 200 and b > 200: return '⚪ Белый'
        elif r > 180 and g > 180 and b > 180: return '🔘 Светло-серый'
        elif r > 100 and g > 100 and b > 100: return '🔘 Серый'
        elif r > 150 and g < 80 and b < 80: return '🔴 Красный'
        elif r < 80 and g < 80 and b > 150: return '🔵 Синий'
        elif r < 80 and g > 150 and b < 80: return '🟢 Зелёный'
        elif r > 180 and g > 100 and b < 50: return '🟠 Оранжевый'
        elif r > 200 and g > 200 and b < 80: return '🟡 Жёлтый'
        elif r > 100 and g < 60 and b > 100: return '🟣 Фиолетовый'
        elif r > 100 and g < 60 and b < 60: return '🟤 Коричневый'
        elif r > 180 and g < 100 and b > 150: return '🩷 Розовый'
        elif r > 150 and g > 150 and b < 80: return '🫒 Хаки'
        elif r < 80 and g > 100 and b > 100: return '🩵 Голубой'
        else: return '🔘 Серый'
    except: return None

def get_color(item):
    photos = item.get('photos', [])
    if photos:
        color = hex_to_color_name(photos[0].get('dominant_color', ''))
        if color: return color
    return 'N/A'

def create_database():
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY, title TEXT, brand TEXT, price REAL,
        currency TEXT, size TEXT, color TEXT, likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0, url TEXT, first_seen TEXT, last_seen TEXT,
        sold INTEGER DEFAULT 0, days_to_sell REAL DEFAULT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS item_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER,
        price REAL, likes INTEGER, views INTEGER, recorded_at TEXT)''')
    conn.commit()
    conn.close()
    print("База данных создана ✅")

def get_items_from_vinted(query, pages=5, category_id=None):
    all_items = []
    session = requests.Session()
    current_cookie = get_current_cookie()
    current_headers = build_headers(current_cookie)
    print(f"Cookie первые 30 символов: '{current_cookie[:30]}'")

    for page in range(1, pages + 1):
        url = 'https://www.vinted.pl/api/v2/catalog/items'
        params = {'search_text': query, 'per_page': 96, 'page': page, 'order': 'newest_first'}
        if category_id:
            params['catalog_ids[]'] = category_id

        response = session.get(url, headers=current_headers, params=params)
        print(f"Страница {page}: статус {response.status_code}")

        if response.status_code != 200:
            print(f"Ошибка: {response.text[:200]}")
            if response.status_code == 401:
                try:
                    from telegram import Bot
                    Bot(token=TOKEN).send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text='⚠️ Cookie истекли!\n\n'
                             '1. Открой vinted.pl в Chrome\n'
                             '2. F12 → Network → Fetch/XHR\n'
                             '3. Прокрути страницу вниз\n'
                             '4. Правая кнопка → Copy as cURL\n'
                             '5. Напиши: /updatecookie [cURL]'
                    )
                except: pass
            break

        items = response.json().get('items', [])
        print(f"Найдено: {len(items)}")
        if not items: break
        all_items.extend(items)
        time.sleep(2)
    return all_items

def save_items(items):
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_count = updated_count = 0
    for item in items:
        try:
            price_data = item.get('price', {})
            price = float(price_data.get('amount', 0))
            likes = item.get('favourite_count', 0)
            views = item.get('view_count', 0)
            item_id = item.get('id')
            color = get_color(item)
            cursor.execute('SELECT id FROM items WHERE id = ?', (item_id,))
            if cursor.fetchone():
                cursor.execute('UPDATE items SET likes=?,views=?,last_seen=?,price=?,color=? WHERE id=?',
                    (likes, views, now, price, color, item_id))
                updated_count += 1
            else:
                cursor.execute('INSERT INTO items (id,title,brand,price,currency,size,color,likes,views,url,first_seen,last_seen,sold) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0)',
                    (item_id, item.get('title'), item.get('brand_title'), price,
                     price_data.get('currency_code', 'PLN'), item.get('size_title', 'N/A'),
                     color, likes, views, f"https://www.vinted.pl/items/{item_id}", now, now))
                new_count += 1
            cursor.execute('INSERT INTO item_history (item_id,price,likes,views,recorded_at) VALUES (?,?,?,?,?)',
                (item_id, price, likes, views, now))
        except Exception as e:
            print(f"Ошибка: {e}")
    conn.commit()
    conn.close()
    return new_count, updated_count

def calculate_analytics(query, items):
    prices = [float(i.get('price', {}).get('amount', 0)) for i in items if i.get('price')]
    prices = [p for p in prices if p > 0]
    if not prices: return None
    likes_list = [i.get('favourite_count', 0) for i in items]
    avg_price = sum(prices) / len(prices)
    median = sorted(prices)[len(prices) // 2]
    std_dev = (sum((p - avg_price) ** 2 for p in prices) / len(prices)) ** 0.5
    avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    demand_index = avg_likes / len(items) if items else 0
    sizes = {}
    for i in items:
        s = i.get('size_title', 'N/A')
        if s and s != 'N/A': sizes[s] = sizes.get(s, 0) + 1
    colors = {}
    for i in items:
        c = get_color(i)
        if c and c != 'N/A': colors[c] = colors.get(c, 0) + 1
    brands = {}
    for i in items:
        b = i.get('brand_title', 'N/A')
        if b and b != 'N/A': brands[b] = brands.get(b, 0) + 1
    score = 5.0
    if demand_index > 10: score += 2
    elif demand_index > 5: score += 1
    if std_dev < avg_price * 0.3: score += 1
    if len(items) > 200: score += 1
    if avg_likes > 15: score += 1
    return {
        'total': len(items), 'avg_price': round(avg_price, 2),
        'median': round(median, 2), 'min_price': round(min(prices), 2),
        'max_price': round(max(prices), 2), 'std_dev': round(std_dev, 2),
        'avg_likes': round(avg_likes, 1), 'demand_index': round(demand_index, 3),
        'cheap': len([p for p in prices if p < avg_price * 0.7]),
        'mid': len([p for p in prices if avg_price * 0.7 <= p <= avg_price * 1.3]),
        'expensive': len([p for p in prices if p > avg_price * 1.3]),
        'top_sizes': sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:5],
        'top_colors': sorted(colors.items(), key=lambda x: x[1], reverse=True)[:5],
        'top_brands': sorted(brands.items(), key=lambda x: x[1], reverse=True)[:3],
        'score': round(min(10, max(1, score)), 1),
        'cheapest': sorted(items, key=lambda x: float(x.get('price', {}).get('amount', 999)))[:3],
        'optimal_buy': round(avg_price * 0.65, 2),
        'optimal_sell': round(avg_price * 0.9, 2),
    }

def start(update, context):
    update.message.reply_text("""👋 Привет! Я Vinted Analytics Bot!

📊 Команды:
/item [бренд] | [категория] — полный анализ
/analyze [бренд] — анализ бренда
/categories — список категорий
/sold [запрос] — статистика продаж
/updatecookie [cURL] — обновить cookie

Примеры:
/item Nike | мужские кроссовки
/item Zara | женские платья""")

def categories(update, context):
    msg = "📋 КАТЕГОРИИ:\n\n👨 МУЖСКОЕ:\n"
    for k in CATEGORIES:
        if 'мужск' in k: msg += f"  • {k}\n"
    msg += "\n👩 ЖЕНСКОЕ:\n"
    for k in CATEGORIES:
        if 'женск' in k: msg += f"  • {k}\n"
    msg += "\n👕 УНИСЕКС:\n"
    for k in CATEGORIES:
        if 'мужск' not in k and 'женск' not in k: msg += f"  • {k}\n"
    update.message.reply_text(msg)

def item_analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /item Nike | мужские кроссовки')
        return
    full_query = ' '.join(context.args)
    if '|' in full_query:
        parts = full_query.split('|')
        query = parts[0].strip()
        category_name = parts[1].strip().lower()
        category_id = CATEGORIES.get(category_name)
        if not category_id:
            update.message.reply_text(f'❌ Категория "{category_name}" не найдена.\nНапиши /categories')
            return
    else:
        query = full_query
        category_name = None
        category_id = None

    msg_text = f'🔍 Анализирую: {query}'
    if category_name: msg_text += f'\n📂 Категория: {category_name}'
    msg_text += '\n⏳ Подожди ~30 секунд...'
    update.message.reply_text(msg_text)

    items = get_items_from_vinted(query, pages=5, category_id=category_id)
    if not items:
        update.message.reply_text(f'❌ Ничего не найдено для {query}')
        return

    new, updated = save_items(items)
    data = calculate_analytics(query, items)
    if not data:
        update.message.reply_text('❌ Ошибка при анализе')
        return

    bar = '█' * int(data['score']) + '░' * (10 - int(data['score']))
    cat_line = f"\n📂 Категория: {category_name}" if category_name else ""
    msg = f"""🎓 HARVARD ANALYTICS: {query}{cat_line}

📦 ПРЕДЛОЖЕНИЕ:
  Объявлений: {data['total']}
  Новых: {new} / Обновлено: {updated}

💰 ЦЕНОВОЙ АНАЛИЗ:
  Средняя: {data['avg_price']} PLN
  Медиана: {data['median']} PLN
  Мин: {data['min_price']} PLN
  Макс: {data['max_price']} PLN
  Отклонение: ±{data['std_dev']} PLN

❤️ ИНДЕКС СПРОСА:
  Среднее лайков: {data['avg_likes']}
  Лайков/Предложений: {data['demand_index']}

📊 РАСПРЕДЕЛЕНИЕ ЦЕН:
  🟢 Дёшево: {data['cheap']} шт
  🟡 Средне: {data['mid']} шт
  🔴 Дорого: {data['expensive']} шт

📐 ТОП РАЗМЕРЫ:"""
    for s, c in data['top_sizes']: msg += f"\n  • {s} — {c} шт"
    msg += "\n\n🎨 ТОП ЦВЕТА:"
    if data['top_colors']:
        for col, c in data['top_colors']: msg += f"\n  • {col} — {c} шт"
    else: msg += "\n  • Данные недоступны"
    msg += "\n\n🏆 ТОП БРЕНДЫ:"
    for b, c in data['top_brands']: msg += f"\n  • {b} — {c} шт"
    msg += f"""

📈 СКОРИНГ: {bar} {data['score']}/10

💡 РЕКОМЕНДАЦИЯ:
  Покупай до: {data['optimal_buy']} PLN
  Продавай за: {data['optimal_sell']} PLN
  Потенциал: +{round(data['optimal_sell'] - data['optimal_buy'], 2)} PLN

🏷 САМЫЕ ДЕШЁВЫЕ:"""
    for item in data['cheapest']:
        price = item.get('price', {}).get('amount', 'N/A')
        title = str(item.get('title', 'N/A'))[:25]
        size = item.get('size_title', '')
        msg += f"\n  • {title} ({size}) — {price} PLN\n    https://www.vinted.pl/items/{item.get('id')}"
    update.message.reply_text(msg)

def analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /analyze Nike')
        return
    brand = ' '.join(context.args)
    update.message.reply_text(f'🔍 Анализирую {brand}...')
    items = get_items_from_vinted(brand, pages=3)
    if not items:
        update.message.reply_text('❌ Ничего не найдено')
        return
    save_items(items)
    data = calculate_analytics(brand, items)
    if not data:
        update.message.reply_text('❌ Ошибка')
        return
    update.message.reply_text(f"""📊 АНАЛИЗ: {brand}
📦 Объявлений: {data['total']}
💰 Средняя: {data['avg_price']} PLN
📉 Мин: {data['min_price']} PLN
📈 Макс: {data['max_price']} PLN
❤️ Лайков: {data['avg_likes']}
📈 Скоринг: {data['score']}/10""")

def check_sold_items():
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, first_seen, last_seen FROM items
        WHERE sold = 0 AND first_seen < datetime('now', '-6 hours')
        AND last_seen > datetime('now', '-7 days')''')
    items_to_check = cursor.fetchall()
    conn.close()
    if not items_to_check:
        print("Нет товаров для проверки")
        return
    print(f"Проверяю {len(items_to_check)} товаров...")
    current_headers = build_headers(get_current_cookie())
    session = requests.Session()
    sold_count = 0
    for item_id, first_seen, last_seen in items_to_check:
        try:
            response = session.get(
                f'https://www.vinted.pl/api/v2/items/{item_id}',
                headers=current_headers)
            if response.status_code == 404:
                conn = sqlite3.connect('vinted.db')
                cursor = conn.cursor()
                cursor.execute('SELECT first_seen FROM items WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                if row:
                    days = (datetime.now() - datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')).total_seconds() / 86400
                    cursor.execute('UPDATE items SET sold=1, days_to_sell=? WHERE id=?',
                        (round(days, 2), item_id))
                    conn.commit()
                    sold_count += 1
                conn.close()
            time.sleep(0.5)
        except Exception as e:
            print(f"Ошибка: {e}")
    print(f"Продано: {sold_count}")

def get_sell_stats(query):
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*), AVG(days_to_sell), MIN(days_to_sell), MAX(days_to_sell)
        FROM items WHERE sold = 1 AND title LIKE ?''', (f'%{query}%',))
    row = cursor.fetchone()
    conn.close()
    return row

def monitor_loop():
    while True:
        print("🔍 Запускаю мониторинг продаж...")
        try: check_sold_items()
        except Exception as e: print(f"Ошибка: {e}")
        print("⏰ Следующая проверка через 1 час")
        time.sleep(3600)

def sold_stats(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /sold Nike')
        return
    query = ' '.join(context.args)
    row = get_sell_stats(query)
    if not row or row[0] == 0:
        update.message.reply_text(f'❌ Нет данных для {query}\nПопробуй завтра!')
        return
    update.message.reply_text(f"""⚡️ ПРОДАЖИ: {query}
✅ Продано: {row[0]}
⏱ Среднее время: {round(row[1], 1)} дней
🚀 Быстрейшая: {round(row[2], 1)} дней
🐌 Дольше всего: {round(row[3], 1)} дней""")

def update_cookie(update, context):
    if not context.args:
        update.message.reply_text(
            '📋 Как обновить cookie:\n\n'
            '1. Открой vinted.pl в Chrome\n'
            '2. F12 → Network → Fetch/XHR\n'
            '3. Прокрути страницу вниз\n'
            '4. Правая кнопка → Copy as cURL\n'
            '5. Напиши: /updatecookie [cURL]'
        )
        return
    curl_text = ' '.join(context.args)
    cookie_match = re.search(r"-b '([^']+)'", curl_text) or re.search(r'-b "([^"]+)"', curl_text)
    if not cookie_match:
        update.message.reply_text('❌ Не могу найти cookie. Скопируй "Copy as cURL"')
        return
    new_cookie = cookie_match.group(1).strip()
    with open('cookie.txt', 'w') as f:
        f.write(new_cookie)
    session = requests.Session()
    test_headers = build_headers(new_cookie)
    response = session.get('https://www.vinted.pl/api/v2/catalog/items',
        headers=test_headers, params={'search_text': 'Nike', 'per_page': 1})
    if response.status_code == 200:
        update.message.reply_text('✅ Cookie обновлены! Бот работает.')
    else:
        update.message.reply_text(f'⚠️ Статус {response.status_code}. Попробуй /item Nike')

create_database()

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('analyze', analyze))
dp.add_handler(CommandHandler('item', item_analyze))
dp.add_handler(CommandHandler('categories', categories))
dp.add_handler(CommandHandler('sold', sold_stats))
dp.add_handler(CommandHandler('updatecookie', update_cookie))

print('🤖 Бот запущен!')
monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
monitor_thread.start()
print("⏰ Мониторинг запущен!")

updater.start_polling()
updater.idle()
