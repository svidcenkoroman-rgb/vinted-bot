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

# ═══════════════════════════════════════════════
# COOKIE — обновляется командой /updatecookie
# ═══════════════════════════════════════════════
COOKIE = "__ps_r=https://www.google.com/; __ps_lu=https://www.vinted.pl/; __ps_did=pscrb_e287bbdd-5a61-4eaa-efa0-ceeeda2769a3; __ps_fva=1757197538485; v_udt=UDdEZU55ZVR6bkZBaWdnOXo2TUpuQ2RCaFN3SC0tM1c4K0lGYW56SzhuWXF5My0tWlBQN25tdGdXNlJxbFRUYWhVOWZpUT09; anon_id=dc3d5138-f0e2-44b6-b322-67bac0ad7f0e; anonymous-locale=pl-fr; anonymous-iso-locale=pl-PL; domain_selected=true; consent_version=eu; v_uid=3172767044; v_sid=72d4e1e6-1785594286; user-iso-locale=pl-PL; cf_clearance=ciP2QbcUUpR6LZUJ_BHzHr4DKPsCpaymdMVyesMQdX0-1785678502-1.2.1.1-lJ_dBO_8D29X03CFtifGYlW5oHEzUDK2F7vveYTu9aSZo.5hp.kR2WOgAyTcg2qj47mVbpIXaFAq1ffV7w1OL9gWErz_rF_IHeAz_8baN.PlXUqe232F6VuhpPxuzTLlGaJVQKvANrj7xW365zpBK4mIh_e_7_SMSJyCkgXxdr34a9Fp.MEnCpW_nvIJNhU74ad5Z9LI3a55XZOrGpcU5FkhEct7m5dvGOc38cnF.mwrE_qdLQmGoFu4v45qtJ8.GHk9B3CwwzVUFI0gL.1LTI4T8oBQq_iteNpnufmRamPbvqjSp.OtvKqQVl_JwNd4K4U9gYmo3dWhqMPfxamn1bj1aEGu14_CKGMdycFrHo4GlOfoSGa3TdF8MxoBH7RbsFjN75EfUtbpnANCEVPbDYXYD5LQY6kxYkYQjmIXhA0naaJzf0fvjOvvR1GgoNLtGuR7HZkv53cwuvkNPwVNLQ; __cf_bm=vGsWINmmKUtE2iz1LbKLaLLkXjD6WDS2Pwvahrg9UEc-1785678502.8890758-1.0.1.1-oiHXACnIrHVhSasybT_B4jGqjH5O.4YQCnmm7SHw9zHrvlki2nI1z90z76UWU31Hy1Pr3KcuxJ.3AuObDmNNza0UMru3ZxfeMgqt0xfVaFTx7KBxQrq1A4XxVJZmxQ4njWr3mP8mEVM86igdKKaTBg; refresh_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg2MjgzMzAzLCJpYXQiOjE3ODU2Nzg1MDMsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJyZWZyZXNoIiwicm9sZXMiOiIiLCJzY29wZSI6InB1YmxpYyB1c2VyIiwic2lkIjoiNzJkNGUxZTYtMTc4NTU5NDI4NiIsInN1YiI6IjMxNzI3NjcwNDQiLCJjYyI6IlBMIiwiYW5pZCI6ImRjM2Q1MTM4LWYwZTItNDRiNi1iMzIyLTY3YmFjMGFkN2YwZSIsImFjdCI6eyJzdWIiOiIzMTcyNzY3MDQ0In19.mXYE34Jq-0SY1a2FmVQBNgNfeW0Rf5tCp0rB7K-aUcflCvVi5PmKpMj_D6FyFPoFGe3X6XF5drbPqdEntoW6mJlumHvNJHLwbIitMj0VBBKa1JXaSCHjXmSKZH_sIxjNX5YEcd22N0e4xqpyIfcV1XOuMlbuZv7tUi5wKNGmDX85g05iEdsLe9utx5xmSAwiAfsyp0ZCxu9mZ8Kqfp6VOAxVqaC4Obmxr_UrUNsvHix_y5EY2DXymPHdXC-7sbOvcKNrRymwXTw_9lHbFoPali1L-V_328-qD63MER1STCHBeHCHmdA0wRVPbKO0EJToSMaPuN3O1LIrWbZQO6s5WA; access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg1Njg1NzAzLCJpYXQiOjE3ODU2Nzg1MDMsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJhY2Nlc3MiLCJyb2xlcyI6IiIsInNjb3BlIjoicHVibGljIHVzZXIiLCJzaWQiOiI3MmQ0ZTFlNi0xNzg1NTk0Mjg2Iiwic3ViIjoiMzE3Mjc2NzA0NCIsImNjIjoiUEwiLCJhbmlkIjoiZGMzZDUxMzgtZjBlMi00NGI2LWIzMjItNjdiYWMwYWQ3ZjBlIiwiYWN0Ijp7InN1YiI6IjMxNzI3NjcwNDQifX0.V9YYQ7sX1yLjNNHlKL2mLNnUnCOU1-xpQFHZnSvPgOz5HZi3v5STtNwKvxQOA3ux80bcMas1Oc8skXtK-XABlSbBMZsRwRLljlwOPmgE4ViVToqujfomUG4eAVxWohL01Yc9HNA2Hxt_AfKTqVjoy8JhJcgRwanmf7NB3iP-dsQkr8GBKR_mPoRaSYjg9XCnxShjqLC-cdbsO5XH3uSSQMMsveaqstWrE-ImWIxz8Z5ZoNFbmC23T7KgZMaHmQZunitrcAJE5M1ulNFVHzGk3sXMYJWb_ZTMkHiNS70k7f_dBc0VSHkfZ6BZtXEiSg0bS9sKUkDsZ0RylJSKtd2SYw; seller_header_visits=3; viewport_size=150; banners_ui_state=SUCCESS; _vinted_fr_session=YVRoMW56Y2s5bWw2MHZoRkUzenF6N1lnbTBqQmlqWFJMTE5HMmNSQ0Z4dy9zdEVzOXNVVTlHTlJQSmp3anl2R2JqTjl2OUxKL0dVN3VaRE1IRDQ1TlRlWUFmRTQ0WUVjcVdoekdQdkM1K0dacnZndWRSdHkyWlZpZ0lGYnBHMHRlQkpmNzVLSjFlNDFSUVBPbmorMDYzajVKMDJ0TW5YNlpkYm1mZUt2SndyOGZOOFdacjBmVXFMa085YXVxMUJxZDhXeTRxeVlIM1poMmVUQjJzWVRuaE9hdEI4STJFcXVyT3Jhd3Y1U1NtcktPSEpuejF1Tkl3eVNuYVRPQ3hJSDBuWi94QWgvV0JOaWxjVFRzR2lyWUtFUzlOZ2hXeDBBdmpSWE4zRWtlTXRXTEYwQkNSL2VpVW93WVl1WGtDQWF2NWpEM1ljWG5zVjJTVnU2ekFnVGRzYzJXRklJL2d0Z1RHOEx6bkxFYTFPZnpqOTkrb0lwUVgyYk8vNktsSUJkZTNZZktJSzdvck1Ud0FKVGFsVDIzZzdYdmVtOVZYR3lUTSs2amFXNnV6eUNIZUE1TGNTQVRXQ2IycG9pMUV5Yy0tQWtFNWp3WGRLTlRGYTRrT3NrTjFndz09--ee1afeea6d2c4001069c42eae0cc540bf7c1d67c; datadome=BZBAyrq4O8_tunhH6X7f2tMypWTNGyJ6jbdbGeLP6X185CEd_JyT3DEKqVXUn1U5JyLIH3GvUACRuzJMyV50g74fExOd741gJ5Cv4_huZPG8cioRfSznuFA2w3fm0bQl"


def get_current_cookie():
    if os.path.exists('cookie.txt'):
        try:
            with open('cookie.txt', 'r') as f:
                saved = f.read().strip()
            if saved:
                return saved
        except Exception:
            pass
    return COOKIE.strip()


def build_headers(cookie):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie.strip(),
        'referer': 'https://www.vinted.pl/catalog',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        'x-anon-id': 'dc3d5138-f0e2-44b6-b322-67bac0ad7f0e',
    }


def notify_cookie_expired():
    try:
        from telegram import Bot
        Bot(token=TOKEN).send_message(
            chat_id=ADMIN_CHAT_ID,
            text=('⚠️ Cookie истекли!\n\n'
                  '1. Открой vinted.pl в Chrome\n'
                  '2. F12 → Network → Fetch/XHR\n'
                  '3. Прокрути страницу вниз\n'
                  '4. Правая кнопка на запрос → Copy as cURL\n'
                  '5. Напиши мне: /updatecookie [вставь cURL]')
        )
    except Exception:
        pass


def hex_to_color_name(hex_color):
    if not hex_color:
        return None
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        if r < 50 and g < 50 and b < 50:
            return '⚫ Чёрный'
        if r > 200 and g > 200 and b > 200:
            return '⚪ Белый'
        if r > 180 and g > 180 and b > 180:
            return '🔘 Светло-серый'
        if r > 150 and g < 80 and b < 80:
            return '🔴 Красный'
        if r < 80 and g < 80 and b > 150:
            return '🔵 Синий'
        if r < 80 and g > 150 and b < 80:
            return '🟢 Зелёный'
        if r > 180 and g > 100 and b < 50:
            return '🟠 Оранжевый'
        if r > 200 and g > 200 and b < 80:
            return '🟡 Жёлтый'
        if r > 100 and g < 60 and b > 100:
            return '🟣 Фиолетовый'
        if r > 100 and g < 60 and b < 60:
            return '🟤 Коричневый'
        if r > 180 and g < 100 and b > 150:
            return '🩷 Розовый'
        if r > 150 and g > 150 and b < 80:
            return '🫒 Хаки'
        if r < 80 and g > 100 and b > 100:
            return '🩵 Голубой'
        if r > 100 and g > 100 and b > 100:
            return '🔘 Серый'
        return '🔘 Серый'
    except Exception:
        return None


def get_color(item):
    photos = item.get('photos', [])
    if photos:
        c = hex_to_color_name(photos[0].get('dominant_color', ''))
        if c:
            return c
    return 'N/A'


def create_database():
    conn = sqlite3.connect('vinted.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY, title TEXT, brand TEXT, price REAL,
        currency TEXT, size TEXT, color TEXT, likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0, url TEXT, first_seen TEXT, last_seen TEXT,
        sold INTEGER DEFAULT 0, days_to_sell REAL DEFAULT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS item_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER,
        price REAL, likes INTEGER, views INTEGER, recorded_at TEXT)''')
    conn.commit()
    conn.close()
    print("База данных создана ✅")


def get_items_from_vinted(query, pages=5, category_id=None):
    all_items = []
    cookie = get_current_cookie()
    hdrs = build_headers(cookie)
    print("=" * 40)
    print(f"ЗАПРОС: {query}")
    print(f"Длина cookie: {len(cookie)}")
    print(f"Cookie начало: {cookie[:40]}")
    print("=" * 40)

    session = requests.Session()

    for page in range(1, pages + 1):
        url = 'https://www.vinted.pl/api/v2/catalog/items'
        params = {'search_text': query, 'per_page': 96,
                  'page': page, 'order': 'newest_first'}
        if category_id:
            params['catalog_ids[]'] = category_id
        try:
            resp = session.get(url, headers=hdrs, params=params, timeout=30)
        except Exception as e:
            print(f"Сетевая ошибка: {e}")
            break

        print(f"Страница {page}: статус {resp.status_code}")

        if resp.status_code != 200:
            print(f"Тело ошибки: {resp.text[:200]}")
            if resp.status_code in (401, 403):
                notify_cookie_expired()
            break

        try:
            items = resp.json().get('items', [])
        except Exception as e:
            print(f"Не JSON: {e}")
            break

        print(f"Найдено: {len(items)}")
        if not items:
            break
        all_items.extend(items)
        time.sleep(2)

    return all_items


def save_items(items):
    conn = sqlite3.connect('vinted.db')
    cur = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_count = 0
    upd_count = 0
    for item in items:
        try:
            pd = item.get('price', {}) or {}
            price = float(pd.get('amount', 0) or 0)
            likes = item.get('favourite_count', 0) or 0
            views = item.get('view_count', 0) or 0
            iid = item.get('id')
            color = get_color(item)
            cur.execute('SELECT id FROM items WHERE id = ?', (iid,))
            if cur.fetchone():
                cur.execute(
                    'UPDATE items SET likes=?,views=?,last_seen=?,price=?,color=? WHERE id=?',
                    (likes, views, now, price, color, iid))
                upd_count += 1
            else:
                cur.execute(
                    'INSERT INTO items (id,title,brand,price,currency,size,color,'
                    'likes,views,url,first_seen,last_seen,sold) '
                    'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0)',
                    (iid, item.get('title'), item.get('brand_title'), price,
                     pd.get('currency_code', 'PLN'), item.get('size_title', 'N/A'),
                     color, likes, views,
                     "https://www.vinted.pl/items/" + str(iid), now, now))
                new_count += 1
            cur.execute(
                'INSERT INTO item_history (item_id,price,likes,views,recorded_at) '
                'VALUES (?,?,?,?,?)', (iid, price, likes, views, now))
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    conn.commit()
    conn.close()
    return new_count, upd_count


def calculate_analytics(items):
    prices = []
    for i in items:
        pd = i.get('price', {}) or {}
        try:
            p = float(pd.get('amount', 0) or 0)
        except Exception:
            p = 0
        if p > 0:
            prices.append(p)
    if not prices:
        return None

    likes_list = [i.get('favourite_count', 0) or 0 for i in items]
    avg = sum(prices) / len(prices)
    median = sorted(prices)[len(prices) // 2]
    std = (sum((p - avg) ** 2 for p in prices) / len(prices)) ** 0.5
    avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    demand = avg_likes / len(items) if items else 0

    sizes, colors, brands = {}, {}, {}
    for i in items:
        s = i.get('size_title')
        if s and s != 'N/A':
            sizes[s] = sizes.get(s, 0) + 1
        c = get_color(i)
        if c and c != 'N/A':
            colors[c] = colors.get(c, 0) + 1
        b = i.get('brand_title')
        if b and b != 'N/A':
            brands[b] = brands.get(b, 0) + 1

    score = 5.0
    if demand > 10:
        score += 2
    elif demand > 5:
        score += 1
    if std < avg * 0.3:
        score += 1
    if len(items) > 200:
        score += 1
    if avg_likes > 15:
        score += 1
    score = min(10, max(1, score))

    def sort_top(d, n):
        return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

    def price_of(x):
        pd = x.get('price', {}) or {}
        try:
            return float(pd.get('amount', 999) or 999)
        except Exception:
            return 999

    return {
        'total': len(items),
        'avg_price': round(avg, 2),
        'median': round(median, 2),
        'min_price': round(min(prices), 2),
        'max_price': round(max(prices), 2),
        'std_dev': round(std, 2),
        'avg_likes': round(avg_likes, 1),
        'demand_index': round(demand, 3),
        'cheap': len([p for p in prices if p < avg * 0.7]),
        'mid': len([p for p in prices if avg * 0.7 <= p <= avg * 1.3]),
        'expensive': len([p for p in prices if p > avg * 1.3]),
        'top_sizes': sort_top(sizes, 5),
        'top_colors': sort_top(colors, 5),
        'top_brands': sort_top(brands, 3),
        'score': round(score, 1),
        'cheapest': sorted(items, key=price_of)[:3],
        'optimal_buy': round(avg * 0.65, 2),
        'optimal_sell': round(avg * 0.9, 2),
    }


def start(update, context):
    update.message.reply_text(
        "👋 Vinted Analytics Bot\n\n"
        "📊 Команды:\n"
        "/item [бренд] | [категория] — полный анализ\n"
        "/analyze [бренд] — анализ бренда\n"
        "/categories — список категорий\n"
        "/sold [запрос] — статистика продаж\n"
        "/updatecookie [cURL] — обновить cookie\n"
        "/testcookie — проверить cookie\n\n"
        "Примеры:\n"
        "/item Nike | мужские кроссовки\n"
        "/item Zara | женские платья")


def categories(update, context):
    msg = "📋 КАТЕГОРИИ\n\n👨 МУЖСКОЕ:\n"
    for k in CATEGORIES:
        if 'мужск' in k:
            msg += "  • " + k + "\n"
    msg += "\n👩 ЖЕНСКОЕ:\n"
    for k in CATEGORIES:
        if 'женск' in k:
            msg += "  • " + k + "\n"
    msg += "\n👕 УНИСЕКС:\n"
    for k in CATEGORIES:
        if 'мужск' not in k and 'женск' not in k:
            msg += "  • " + k + "\n"
    update.message.reply_text(msg)


def testcookie(update, context):
    cookie = get_current_cookie()
    hdrs = build_headers(cookie)
    try:
        r = requests.get('https://www.vinted.pl/api/v2/catalog/items',
                         headers=hdrs,
                         params={'search_text': 'Nike', 'per_page': 1},
                         timeout=30)
        src = 'файл cookie.txt' if os.path.exists('cookie.txt') else 'код'
        update.message.reply_text(
            "🔎 ПРОВЕРКА COOKIE\n\n"
            "Источник: " + src + "\n"
            "Длина: " + str(len(cookie)) + "\n"
            "Начало: " + cookie[:40] + "\n"
            "Статус ответа: " + str(r.status_code) + "\n\n"
            + ("✅ Cookie рабочие" if r.status_code == 200 else "❌ " + r.text[:150]))
    except Exception as e:
        update.message.reply_text("Ошибка проверки: " + str(e))


def item_analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /item Nike | мужские кроссовки')
        return

    full = ' '.join(context.args)
    if '|' in full:
        parts = full.split('|')
        query = parts[0].strip()
        cat_name = parts[1].strip().lower()
        cat_id = CATEGORIES.get(cat_name)
        if not cat_id:
            update.message.reply_text(
                '❌ Категория "' + cat_name + '" не найдена.\nНапиши /categories')
            return
    else:
        query = full
        cat_name = None
        cat_id = None

    t = '🔍 Анализирую: ' + query
    if cat_name:
        t += '\n📂 Категория: ' + cat_name
    t += '\n⏳ Подожди ~30 секунд...'
    update.message.reply_text(t)

    items = get_items_from_vinted(query, pages=5, category_id=cat_id)
    if not items:
        update.message.reply_text(
            '❌ Ничего не найдено для ' + query +
            '\n\nПроверь cookie: /testcookie')
        return

    new, upd = save_items(items)
    d = calculate_analytics(items)
    if not d:
        update.message.reply_text('❌ Ошибка при анализе')
        return

    bar = '█' * int(d['score']) + '░' * (10 - int(d['score']))
    cat_line = ("\n📂 Категория: " + cat_name) if cat_name else ""

    msg = ("🎓 HARVARD ANALYTICS: " + query + cat_line + "\n\n"
           "📦 ПРЕДЛОЖЕНИЕ:\n"
           "  Объявлений: " + str(d['total']) + "\n"
           "  Новых: " + str(new) + " / Обновлено: " + str(upd) + "\n\n"
           "💰 ЦЕНОВОЙ АНАЛИЗ:\n"
           "  Средняя: " + str(d['avg_price']) + " PLN\n"
           "  Медиана: " + str(d['median']) + " PLN\n"
           "  Мин: " + str(d['min_price']) + " PLN\n"
           "  Макс: " + str(d['max_price']) + " PLN\n"
           "  Отклонение: ±" + str(d['std_dev']) + " PLN\n\n"
           "❤️ ИНДЕКС СПРОСА:\n"
           "  Среднее лайков: " + str(d['avg_likes']) + "\n"
           "  Лайков/Предложений: " + str(d['demand_index']) + "\n\n"
           "📊 РАСПРЕДЕЛЕНИЕ ЦЕН:\n"
           "  🟢 Дёшево: " + str(d['cheap']) + " шт\n"
           "  🟡 Средне: " + str(d['mid']) + " шт\n"
           "  🔴 Дорого: " + str(d['expensive']) + " шт\n\n"
           "📐 ТОП РАЗМЕРЫ:")
    for s, c in d['top_sizes']:
        msg += "\n  • " + str(s) + " — " + str(c) + " шт"

    msg += "\n\n🎨 ТОП ЦВЕТА:"
    if d['top_colors']:
        for col, c in d['top_colors']:
            msg += "\n  • " + str(col) + " — " + str(c) + " шт"
    else:
        msg += "\n  • Данные недоступны"

    msg += "\n\n🏆 ТОП БРЕНДЫ:"
    for b, c in d['top_brands']:
        msg += "\n  • " + str(b) + " — " + str(c) + " шт"

    msg += ("\n\n📈 СКОРИНГ: " + bar + " " + str(d['score']) + "/10\n\n"
            "💡 РЕКОМЕНДАЦИЯ:\n"
            "  Покупай до: " + str(d['optimal_buy']) + " PLN\n"
            "  Продавай за: " + str(d['optimal_sell']) + " PLN\n"
            "  Потенциал: +" + str(round(d['optimal_sell'] - d['optimal_buy'], 2)) + " PLN\n\n"
            "🏷 САМЫЕ ДЕШЁВЫЕ:")
    for it in d['cheapest']:
        pd = it.get('price', {}) or {}
        msg += ("\n  • " + str(it.get('title', 'N/A'))[:25] +
                " (" + str(it.get('size_title', '')) + ") — " +
                str(pd.get('amount', 'N/A')) + " PLN\n    " +
                "https://www.vinted.pl/items/" + str(it.get('id')))

    update.message.reply_text(msg)


def analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /analyze Nike')
        return
    brand = ' '.join(context.args)
    update.message.reply_text('🔍 Анализирую ' + brand + '...')
    items = get_items_from_vinted(brand, pages=3)
    if not items:
        update.message.reply_text('❌ Ничего не найдено\nПроверь: /testcookie')
        return
    save_items(items)
    d = calculate_analytics(items)
    if not d:
        update.message.reply_text('❌ Ошибка')
        return
    update.message.reply_text(
        "📊 АНАЛИЗ: " + brand + "\n"
        "📦 Объявлений: " + str(d['total']) + "\n"
        "💰 Средняя: " + str(d['avg_price']) + " PLN\n"
        "📉 Мин: " + str(d['min_price']) + " PLN\n"
        "📈 Макс: " + str(d['max_price']) + " PLN\n"
        "❤️ Лайков: " + str(d['avg_likes']) + "\n"
        "📈 Скоринг: " + str(d['score']) + "/10")


def check_sold_items():
    conn = sqlite3.connect('vinted.db')
    cur = conn.cursor()
    cur.execute("""SELECT id FROM items
        WHERE sold = 0 AND first_seen < datetime('now', '-6 hours')
        AND last_seen > datetime('now', '-7 days')""")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("Нет товаров для проверки")
        return
    print("Проверяю " + str(len(rows)) + " товаров...")
    hdrs = build_headers(get_current_cookie())
    session = requests.Session()
    sold = 0
    for (iid,) in rows:
        try:
            r = session.get('https://www.vinted.pl/api/v2/items/' + str(iid),
                            headers=hdrs, timeout=20)
            if r.status_code == 404:
                conn = sqlite3.connect('vinted.db')
                cur = conn.cursor()
                cur.execute('SELECT first_seen FROM items WHERE id = ?', (iid,))
                row = cur.fetchone()
                if row:
                    fs = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    days = (datetime.now() - fs).total_seconds() / 86400
                    cur.execute('UPDATE items SET sold=1, days_to_sell=? WHERE id=?',
                                (round(days, 2), iid))
                    conn.commit()
                    sold += 1
                conn.close()
            time.sleep(0.5)
        except Exception as e:
            print("Ошибка проверки: " + str(e))
    print("Продано: " + str(sold))


def get_sell_stats(query):
    conn = sqlite3.connect('vinted.db')
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*), AVG(days_to_sell), MIN(days_to_sell), MAX(days_to_sell)
        FROM items WHERE sold = 1 AND title LIKE ?""", ('%' + query + '%',))
    row = cur.fetchone()
    conn.close()
    return row


def monitor_loop():
    while True:
        print("🔍 Мониторинг продаж...")
        try:
            check_sold_items()
        except Exception as e:
            print("Ошибка мониторинга: " + str(e))
        print("⏰ Следующая проверка через 1 час")
        time.sleep(3600)


def sold_stats(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /sold Nike')
        return
    query = ' '.join(context.args)
    row = get_sell_stats(query)
    if not row or not row[0]:
        update.message.reply_text('❌ Нет данных для ' + query + '\nПопробуй завтра!')
        return
    update.message.reply_text(
        "⚡️ ПРОДАЖИ: " + query + "\n"
        "✅ Продано: " + str(row[0]) + "\n"
        "⏱ Среднее время: " + str(round(row[1], 1)) + " дней\n"
        "🚀 Быстрейшая: " + str(round(row[2], 1)) + " дней\n"
        "🐌 Дольше всего: " + str(round(row[3], 1)) + " дней")


def update_cookie(update, context):
    if not context.args:
        update.message.reply_text(
            '📋 Как обновить cookie:\n\n'
            '1. Открой vinted.pl в Chrome\n'
            '2. F12 → Network → Fetch/XHR\n'
            '3. Прокрути страницу вниз\n'
            '4. Правая кнопка на запрос → Copy as cURL\n'
            '5. Напиши: /updatecookie [вставь cURL]\n\n'
            'Можно также вставить просто строку cookie целиком.')
        return

    raw = update.message.text
    raw = raw.split(' ', 1)[1] if ' ' in raw else ''

    m = re.search(r"-b '([^']+)'", raw)
    if not m:
        m = re.search(r'-b "([^"]+)"', raw)
    if not m:
        m = re.search(r"-H 'cookie: ([^']+)'", raw, re.IGNORECASE)
    if not m:
        m = re.search(r'-H "cookie: ([^"]+)"', raw, re.IGNORECASE)

    new_cookie = m.group(1).strip() if m else raw.strip()
    new_cookie = new_cookie.replace('\n', '').replace('\r', '').strip()

    if 'cf_clearance' not in new_cookie and 'access_token_web' not in new_cookie:
        update.message.reply_text(
            '❌ Не похоже на cookie.\n'
            'Нужен текст с cf_clearance или access_token_web')
        return

    with open('cookie.txt', 'w') as f:
        f.write(new_cookie)

    try:
        r = requests.get('https://www.vinted.pl/api/v2/catalog/items',
                         headers=build_headers(new_cookie),
                         params={'search_text': 'Nike', 'per_page': 1},
                         timeout=30)
        if r.status_code == 200:
            update.message.reply_text(
                '✅ Cookie обновлены и работают!\nДлина: ' + str(len(new_cookie)))
        else:
            update.message.reply_text(
                '⚠️ Cookie сохранены, но статус ' + str(r.status_code) +
                '\n' + r.text[:150])
    except Exception as e:
        update.message.reply_text('⚠️ Сохранено, но ошибка проверки: ' + str(e))


create_database()

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('analyze', analyze))
dp.add_handler(CommandHandler('item', item_analyze))
dp.add_handler(CommandHandler('categories', categories))
dp.add_handler(CommandHandler('sold', sold_stats))
dp.add_handler(CommandHandler('updatecookie', update_cookie))
dp.add_handler(CommandHandler('testcookie', testcookie))

print('🤖 Бот запущен!')
print('Длина COOKIE в коде: ' + str(len(COOKIE)))

threading.Thread(target=monitor_loop, daemon=True).start()
print("⏰ Мониторинг запущен!")

updater.start_polling(drop_pending_updates=True)
updater.idle()
